import pytest
import ipytest

import pandas as pd
from tqdm import tqdm
import numpy as np
import urllib
from datetime import date, timedelta,datetime
from itertools import permutations
import string
from IPython.core.display import display, HTML
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from IPython.display import Image
from IPython import get_ipython
import html2text
import torch
import datasets
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer,pipeline
# import wandb
import re
import pickle
import os
from os.path import exists
import boto3
from cloudpathlib import CloudPath
from cloudpathlib import S3Client
from io import StringIO

from transformers.utils.dummy_pt_objects import TRANSFO_XL_PRETRAINED_MODEL_ARCHIVE_LIST


def get_root_path(read_from='s3',override_path=None):
    
    if override_path is not None and override_path!='':
        return override_path

    if read_from == 'local-drive':
        root_path = '/Volumes/GoogleDrive/My Drive/'
    elif read_from == 'gdrive':
        root_path = '/content/drive/MyDrive/'
    elif read_from == 's3':
        root_path = 'koya/'
    else:
        raise ValueError(f'The value ({read_from}) is invalid. Options are: local-drive, gdrive and s3')

    return root_path

def get_project_path(read_from='s3',override_path=None,project=None):

    if override_path is not None and override_path!='':
        return override_path

    root_path = get_root_path(read_from=read_from)
    
    project_path = root_path+'Data Science/Projects/'

    if project == 'vivian_health':
        project_path += 'Vivian-Health/'
    else:
        raise ValueError('project is not defined')

    return project_path


def get_output_data_path(read_from='s3',override_path=None,project=None):

    if override_path is not None and override_path!='':
        return override_path

    project_path = get_project_path(read_from=read_from,override_path=override_path,project=project)

    return project_path+'data/output/'

def get_artifact_path(read_from='s3',override_path=None,project=None,run_name=None):

    if override_path is not None and override_path!='':
        return override_path

    project_path = get_project_path(read_from=read_from,override_path=override_path,project=project)

    output_path = project_path+'artifacts/'
    if run_name is not None:
        artifact_path = output_path+f'{run_name}'
    else:
        artifact_path = None

    return output_path,artifact_path


def remove_html_tags(string):
    text_maker = html2text.HTML2Text()
    return text_maker.handle(string)


def concatenate_title_with_description(row,
                                       title_col = 'job_title',
                                       description_col = 'description'):
    """Concatenates job title with the description, also removes HTML tags from description"""
    if pd.notnull(row[title_col]) and pd.notnull(row[description_col]):
        concatenated = f"""title: {row[title_col]}
        description: {remove_html_tags(row[description_col])}""".strip()
    elif pd.notnull(row[title_col]):
        concatenated = f"title: {row[title_col]}"
    elif pd.notnull(row[description_col]):
        concatenated = f"description: {remove_html_tags(row[description_col])}"
    else:
        concatenated = None
    return concatenated

def preprocess(data_df, text_column_name):
    data_df[text_column_name] = data_df.apply(concatenate_title_with_description, axis=1)
    return data_df


def fetch_label_mapping(y_data):
    id2label = {i: name for i, name in enumerate(y_data.names)}
    label2id = {name: i for i, name in enumerate(y_data.names)}
    return id2label, label2id

def split(data, x_col_name, y_col_name, test_size=.33, random_state=42):
    label_is_not_null = data[y_col_name].notnull()
    labelled_data = data.loc[label_is_not_null, [x_col_name, y_col_name]]
    train_df, test_df = train_test_split(labelled_data,
                                         test_size=test_size,
                                         random_state=random_state)

    # Need to see the exact same classes in the train and test.
    assert set(train_df[y_col_name] == set(test_df[y_col_name]))

    dataset = datasets.DatasetDict({'train': datasets.Dataset.from_pandas(train_df),
                                'test': datasets.Dataset.from_pandas(test_df)
                                })
    
    dataset = dataset.rename_column(y_col_name, 'label')
    dataset = dataset.class_encode_column('label')

    id2label, label2id = fetch_label_mapping(dataset['train'].features['label'])

    return dataset, id2label, label2id

def get_tokenizer(pretrained_model_name):
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    return tokenizer

def get_wrapped_tokenizer(tokenizer, max_sequence_length=512, tokenizer_kwargs={},text_column_name='title_description'):
    def tokenize_data(examples):
        if max_sequence_length is not None:
            encoding = tokenizer(examples[text_column_name], **tokenizer_kwargs)
        else:
            encoding = tokenizer(examples[text_column_name], **tokenizer_kwargs)
        encoding['token_count'] = [np.sum(x) for x in encoding['attention_mask']]
        if max_sequence_length is not None:
            encoding['is_max_count'] = [x == max_sequence_length for x in encoding['token_count']]
        return encoding
    return tokenize_data


def initialize_pretrained_model(pretrained_model_name, device,
                                id2label, label2id):
    model = AutoModelForSequenceClassification\
        .from_pretrained(pretrained_model_name,
                            num_labels=len(id2label),
                            id2label=id2label,
                            label2id=label2id)\
        .to(device)
    return model


def compute_accuracy(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy_metric = datasets.load_metric('accuracy')
    return accuracy_metric.compute(predictions=predictions, references=labels)

def preds_to_fake_probs(preds):
    ilogit_preds = 1 / (1 + np.exp(-preds))
    ilogit_preds_normalized = ilogit_preds / np.sum(ilogit_preds, axis=1)[:, None]
    return ilogit_preds_normalized


def compute_auc(eval_pred):
    logits, labels = eval_pred
    scores = preds_to_fake_probs(logits)
    auc_multiclass_metric = datasets.load_metric('roc_auc', 'multiclass')
    return auc_multiclass_metric.compute(prediction_scores=scores, references=labels, multi_class='ovr')


def train_model(dataset, pretrained_model_name, device, id2label, label2id, tokenizer,
                artifact_dir, compute_metrics, model_kwargs={}, training_kwargs={}, trainer_kwargs={}):
    
    model = initialize_pretrained_model(pretrained_model_name, device,
                                id2label, label2id)

    training_args = TrainingArguments(output_dir=artifact_dir, **training_kwargs)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        tokenizer = tokenizer,
        compute_metrics=compute_metrics,
    )

    return trainer

def get_predictions(trainer, data):
    predictions, label_ids, metrics = trainer.predict(data)
    return predictions, label_ids, metrics


def threshold_curve(preds, label_ids, n_ntiles=10):
    correct = np.argmax(preds, axis=1) == label_ids
    fake_probs = preds_to_fake_probs(preds)
    confidences = np.max(fake_probs, axis=1)
    ntile, bins = pd.qcut(confidences, n_ntiles, labels=False, retbins=True)

    results = []
    for i in range(n_ntiles):
        count = np.sum(ntile >= i)
        accuracy = np.mean(correct[ntile >= i])
        results.append({'ntile': i,
                      'proportion': count / len(preds),
                      'accuracy': accuracy})
    return pd.DataFrame(results)

def clean_text(text,max_lenght=250):
    text_maker = html2text.HTML2Text()
    text = text_maker.handle(text)
    text = truncate_words(text,max_lenght)
    return [text]

def get_wandb_runs(entity_name
                    ,project_name
                    ,read_from='local-drive'
                    ,path=None
                    ,filename=None
                    ,metric_name='best_accuracy'
                    ,metric_name_show='accuracy'
                    ,filters={'state':'finished'}
                    ,drop_on_metric=True
                    ,update_file=False
                    ,update_method=None
                    ,path_save=None):

    
    if read_from=='local-drive':
        runs_df = pd.read_csv(path+filename)
    elif read_from=='s3':
        idx = path.find('/')
        path_s3 = path[:idx]
        filename_s3 = path[idx+1:]+filename
        
        # Creating the low level functional client
        client = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

        # Create the S3 object
        obj = client.get_object(
            Bucket = path_s3,
            Key = filename_s3
        )

        filepath = obj['Body']
        runs_df = pd.read_csv(filepath)
    elif read_from=='api':
        api = wandb.Api()

        runs = api.runs(path=f'{entity_name}/{project_name}',filters=filters)

        summary_list, name_list, id_list = [], [] ,[]
        for run in runs:
            
            # .summary contains the output keys/values for metrics like accuracy.
            #  We call ._json_dict to omit large files 
            summary_list.append(run.summary._json_dict)
            ss=[]
            for s in summary_list:
                if metric_name in s:
                    ss.append(s[metric_name])
                else:
                    ss.append(None)
                    
            #attribute
            aa=[]
            for a in summary_list:
                if 'attribute' in a:
                    aa.append(a['attribute'])
                else:
                    aa.append(None)
            

            # .name is the human-readable name of the run.
            name_list.append(run.name)
            id_list.append(run.id)
        
        runs_df = pd.DataFrame({
            "run_id":id_list
            ,"run_name": name_list
            ,metric_name_show: ss
            ,'attribute':aa
            })

        if drop_on_metric:
            runs_df = runs_df.dropna(subset=[metric_name_show])

        if update_file:
            if update_method=='local-drive':
                runs_df.to_csv(path_save+filename,index=False)
            elif update_method=='s3':
                path=path_save
                idx = path.find('/')
                path_s3 = path[:idx]
                filename_s3 = path[idx+1:]+filename
                
                # Creating the low level functional client
                s3_resource = boto3.resource('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

                bucket = path_s3
                csv_buffer = StringIO()
                runs_df.to_csv(csv_buffer,index=False)
                s3_resource.Object(bucket,filename_s3).put(Body=csv_buffer.getvalue())
            else:
                raise ValueError('update_method is not valid')
        
    return runs_df

def from_json_to_pandas(d,id_name='job_id',probabilities=True):
    key_list = list(d.keys())
    att_list = list(d[list(d.keys())[0]].keys())
    newd={}
    newd[id_name] = key_list
    for att in att_list:
        label_list, score_list = [],[]
        for k,v in d.items():
            label_list.append(v[att]['label'])
            if probabilities:
                score_list.append(v[att]['score'])

        newd[f'{att}-label']=label_list

        if probabilities:
            newd[f'{att}-score']=score_list

    data=pd.DataFrame(newd).set_index(id_name)
    
    return data,att_list

def from_raw_pandas_to_json(data,attributes,probabilities=True):
    d={}
    for index,row in data.iterrows():
        temp_col={}
        for col in attributes:
            if not probabilities:
                temp_col[col]={'label':row[col]['label']}
            else:
                temp_col[col]=row[col]
        d[index]=temp_col
    return d

def get_clean_dataframe(d,probabilities=True):
    data,att_list = from_json_to_pandas(d,probabilities=probabilities)
    for att in att_list:
        data=data.rename(columns={f'{att}-label':att})

    if not probabilities:
        data=data[att_list]
    return data

def process_acronym(text,category,dict_acronym=None,format_dict=True):

    if dict_acronym is None:
        dict_acronym = get_dict_acronym()
    
    if category not in dict_acronym.keys():
        return text
    
    if format_dict:
        dict_acronym_formatted = {}

        for k,v in dict_acronym[category].items():
            dict_acronym_formatted[k] = f' {k} [{v}] '
    else:
        dict_acronym_formatted=dict_acronym[category]

    for k in dict_acronym[category]:
        pattern = r'(^|\(|\s)'+k+r'(\)|\s|\,|\-|\/|$)'
        if re.search(pattern,text):
            text = text.replace(k,dict_acronym_formatted[k])
    return text

def get_dict_acronym():

    dict_acronym = {
        'RN':{
            'ED':'ED - Emergency Department'
            ,'Emergency Room':'ED - Emergency Department'
            ,'ER':'ED - Emergency Department'
            ,'Emergency Dept':'ED - Emergency Department'
            ,'Emergency Department':'ED - Emergency Department'


            ,'ICU':'ICU - Intensive Care Unit'
            ,'Intensive Care Unit':'ICU - Intensive Care Unit'

            ,'PACU':'PACU - Post Anesthetic Care'
            ,'Post Anesthetic Care':'PACU - Post Anesthetic Care'

            ,'OR':'OR - Operating Room'
            ,'Operating Room':'OR - Operating Room'

            ,'L&D':'Labor and Delivery'
            ,'Labor & Delivery':'Labor and Delivery'

            ,'PCU':'Progressive Care Unit'

            ,'NICU':'NICU - Neonatal Intensive Care'
            ,'Neonatal Intensive Care':'NICU - Neonatal Intensive Care'

            ,'MedSurg':'Med Surg'
            ,'Med Surge':'Med Surg'
            ,'Medsurg':'Med Surg'
            ,'Medical Surgical':'Med Surg'
            ,'Med/Surg':'Med Surg'
            ,'Med/surg':'Med Surg'

            ,'Rehab':'Rehabilitation'
        }
        ,'Allied Health Professional':{
            'Radiology Tech':'Radiology Technologist'
        }
        ,'CNA':{
            'Certified Nursing Assistant':'CNA'
            ,'Certified Nurse Assistant':'CNA'
            ,'Personal Care Aide':'CNA'
            ,'Patient Care Technician':'CNA'
            ,'PCT':'CNA'
            ,'Patient Care Assistant':'CNA'
            ,'PCA':'CNA'
            ,'Patient Care':'CNA'
            ,'Care Assistant':'CNA'
            ,'CNA':'CNA'
            ,'Certified Nursing Assistants':'CNA'
            ,'Certified Nursing Asst':'CNA'
            ,'CERTIFIED NURSING':'CNA'
            ,'CERTIFIED NURSE':'CNA'
            ,'Certified Nursing':'CNA'
            ,'Certified Nurse':'CNA'
        }
        ,'LPN / LVN':{
            'LPN/LVN':'LPN / LVN'
            ,'LPN':'LPN / LVN'
            ,'LVN':'LPN / LVN'
            ,'LPN / LVN':'LPN / LVN'
            ,'Licensed Practical Nurse':'LPN / LVN'
            ,'LICENSED PRACTICAL NURSE':'LPN / LVN'
            ,'Licensed Vocational Nurse':'LPN / LVN'
            ,'Practical Nurse':'LPN / LVN'
            ,'Licensed Practical Vocational Nurse':'LPN / LVN'
            ,'Licensed Practical or Vocational Nurse':'LPN / LVN'
        }
        ,'CMA':{
            'Certified Medical Assistant':'CMA'
            ,'CMA':'CMA'
            ,'Medical Assistant':'CMA'
            ,'MEDICAL ASSISTANT':'CMA'
            ,'Certified Medical':'CMA'
            ,'Medical Asst':'CMA'
            ,'Medical Asst Cert':'CMA'
            ,'Medical Asst Certified':'CMA'
        }
    }
    
    return dict_acronym

def preprocess_data_specialty(data,col_category,x_col,col_text_raw):
    categories = data[col_category].unique()
    data[x_col]=None

    for category in tqdm(categories):
        sub_data = data[data[col_category]==category].copy(deep=True)
        sub_data[x_col] = data[col_text_raw].apply(lambda x: process_acronym(x,category))
        data[x_col]=data[x_col].fillna(sub_data[x_col])
    return data

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

def write_results_wandb(run):

    run_name = f'predictions__filename_[{output_filename}]'
    run = wandb.init(project=params['project']['project_name']
                 , entity=params['project']['entity_name']
                 , name=run_name
                 ,reinit=True)

    for k in params.keys():
        run.summary[k] = str(params[k])
    run.finish()

def get_device_type():
    if torch.backends.mps.is_available():
        device_type = "mps"
    elif torch.cuda.is_available():
        device_type = "cuda"
    else:
        device_type = "cpu"
    return device_type

def uploadDirectory(path_local,bucketname,path_bucket):
    s3C = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
    for root,dirs,files in tqdm(os.walk(path_local)):
        for file in files:
            built = os.path.join(root,file)
            out = path_bucket+file
            s3C.upload_file(Filename=built,Bucket=bucketname,Key=out)

def get_language_models_pipeline(read_from='s3',use_local=True,run_name=None,path_artifact=None,path_s3=None,device_type=None):

    if not exists('temp/'):
        os.mkdir('temp/')

    if read_from=='s3':
        path_artifact = f'temp/{run_name}/'
        if not exists(path_artifact) or use_local==False:
            print('downloading artifact from S3')
            client = S3Client(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
            cp = CloudPath(f"s3://{path_s3}{run_name}/",client=client)
            cp.download_to(path_artifact)
        else:
            print('loading artifact from local folder')

    #load the pretrained model
    model = AutoModelForSequenceClassification.from_pretrained(path_artifact)

    #load the pretrained tokenizer
    tokenizer = AutoTokenizer.from_pretrained(path_artifact)

    #create the pipeline using the model and tokenizer
    if device_type=='cpu':
        pipe = pipeline(task="text-classification",model=model, tokenizer=tokenizer, return_all_scores=False)
    else:
        pipe = pipeline(task="text-classification",model=model, tokenizer=tokenizer, return_all_scores=False,device=0)

    return pipe

def batch_predict(models,data,col_category,x_col,use_tags=False):
    data['pred'] = None
    categories = data[col_category].unique()

    for category in tqdm(categories):

        if not pd.isnull(category):

            sub_data = data[data[col_category]==category].copy(deep=True)

            model = models[category]

            if use_tags:
                sub_data['pred'] = sub_data[x_col].apply(model.get_tags)
            else:
                sub_data['pred'] = sub_data[x_col].apply(model.predict)

        data['pred']=data['pred'].fillna(sub_data['pred'])
    return data

def validate_bool_variable(x):
    try:
        x=x.lower()
        if x =='true':
            return True
        elif x=='false':
            return False
        raise ValueError('variable not a valid boolean')
    except:
        raise ValueError('variable not a valid boolean')

def preprocess_data_bonus(data,col_text_raw,x_col):
    data[x_col]=data[col_text_raw]
    return data

class InferenceParamsAPI:
    
    def __init__(self,external_params,inference_context,inference_type):
        self.inference_context = inference_context
        self.inference_type = inference_type
        self.external_params  =external_params
        self.params = self.get_params()
        
    def get_params(self):
        
        update_internal_params = self.get_update_internal_params()        
        internal_params = self.load_internal_params(update_internal_params=update_internal_params)
        sub = {"external_params":self.external_params}
        internal_params.update(sub)
        internal_params['inference_type']=self.inference_type
        self.params = internal_params
        self.params = self.check_params()
        return self.params
           
    def get_update_internal_params(self):
        if "update_internal_params" in self.external_params:
            update_internal_params = self.external_params["update_internal_params"]
        else:
            update_internal_params = None
            
        return update_internal_params

    def load_internal_params(self,update_internal_params=None):

        internal_params = {    
                "data":{
                    "data_method":"s3" #the method to read the input data
                    ,"random_state":"2" #the random_state to use
                    ,"read_data_from":"s3"
                    ,"keep_original_labels":"False"
                }
                ,"project":{
                    "project_name_wandb":"vivian-health" #project name to be tracked in weights and biases
                    ,"entity_name_wandb":"koya-test2" #the entity name to be tracked in weights and biases
                    ,"project_name":"vivian_health"
                }
                ,"run":{
                    "output_format":"json_prob" #options: json, pandas_clean, pandas_raw
                    ,"output_format_csv":"pandas_prob" #options: json, pandas_clean, pandas_raw
                }
                ,"model":{
                    "read_model_from":"s3"
                    ,"read_model_metrics_from":"s3"
                    ,"use_local_model":"True"
                    ,"model_metrics_filename":"model_metrics.csv"
                    ,"path_model_s3":'koya/Data Science/Projects/Vivian-Health/artifacts/'
                }
                ,"labels_params":{
                    "shift":{
                        "x_col":"title_description" #the column that contains the input data - it will be used for preprocessing
                    }
                    ,"discipline":{
                        "x_col":"title_description" #the column that contains the input data - it will be used for preprocessing
                    }
                    ,"employment_type":{
                        "x_col":"title_description" #the column that contains the input data - it will be used for preprocessing
                    }
                    ,"specialty":{
                        "x_col":"job_title_processed"
                        ,"col_category":"discipline"
                        ,"col_text_raw":"job_title"
                        ,"x_col_discipline":"title_description" #the column that contains the input data - it will be used for preprocessing
                        ,"drop_category_col":"False"
                        ,"use_tags":"True"
                    }
                    ,"bonus":{
                       "x_col":"job_title_processed"
                       ,"col_text_raw":"job_title"
                    }
                }
                ,"output":{}
                ,"inference_context":self.inference_context
            }

        #TODO: check if the input from the update parameters are different from the actual params (example use_local and use_local_model)
        #TODO: update internal params to more than 2 levels (example: labels_params)
        if self.inference_context=='internal' and update_internal_params is not None:
            for k,v in internal_params.items():
                if k in update_internal_params:
                    for k2,v2 in update_internal_params[k].items():
                        internal_params[k][k2]=update_internal_params[k][k2]

        return internal_params
        
    def check_params(self):
        params=self.params
        if self.inference_type=='batch':

            path_input_data = params['external_params']['path_input_data']
            #TODO: check if the data exists in local and in s3

            input_filename = params['external_params']['input_filename']
            if input_filename is None or input_filename=='':
                raise ValueError('the parameter filename is invalid')
            #TODO: check if the data exists in local and in s3


            index_column = params['external_params']['index_column']
            if index_column is None or index_column=='':
                raise ValueError('the parameter index_column is invalid')
            #TODO: check if index column exists in the data

            data_sample_size = params['external_params']['data_sample_size']

            if data_sample_size is not None and data_sample_size not in ['','full','all']:
                try:
                    data_sample_size = int(data_sample_size)
                except:
                    raise ValueError('the parameter data_sample_size is invalid')

            save_output_csv = params['external_params']['save_output_csv']
            if save_output_csv is None or save_output_csv.lower() not in ['true','false']:
                raise ValueError('the parameter save_output_csv is invalid')
            try:
                save_output_csv = bool(save_output_csv)
            except:
                raise ValueError('the parameter save_output_csv is invalid')

            path_output_data = params['external_params']['path_output_data']
            #TODO: check if the data exists in local and in s3

            output_filename = params['external_params']['output_filename']
            if output_filename is None:
                output_filename = ''
            elif '.csv' not in output_filename and output_filename!='':
                output_filename+='.csv'
            #TODO: full control on the name of the file (only one .csv)

            labels = params['external_params']['labels']
            if labels is None or labels=='':
                raise ValueError('the parameter labels is invalid')
            if type(labels)==list:
                if len(labels)==0:
                    raise ValueError('the parameter labels is invalid')
                #TODO: check for the right labels in the list
            #TODO: check for list of labels if the input is a string with labels separated with comma

            return_json = params['external_params']['return_json']
            if return_json is None or return_json.lower() not in ['true','false']:
                raise ValueError('the parameter return_json is invalid')
            try:
                return_json = bool(return_json)
            except:
                raise ValueError('the parameter return_json is invalid')

            ext_dict = {}
            for k,v in params['external_params'].items():
                if k!='update_internal_params':
                    ext_dict[k]=eval(k)
            ext_dict['update_internal_params']=params['external_params']['update_internal_params']
            params['external_params'] = ext_dict


            ## Internal parameters:

            random_state = params['data']['random_state']
            if random_state is not None and random_state!='':
                try:
                    random_state = int(random_state)
                except:
                    raise ValueError('the parameter random_state is invalid')
            else:
                random_state=1

            params['data']['random_state']=random_state

        return params
    
class InferenceDataAPI:
    
    def __init__(self,params,data=None):
        self.params = params
        self.data = self.get_data(data)
        
    def retrieve_data(self,path
                        ,filename
                        ,drop_null_index=False
                        ,index_column=None
                        ,method='filepath'
                        ,use_cache=False
                        ,save_file=False
                        ,aws_credentials=None):


        if use_cache:
            if exists('temp_data/'+filename):
                method ='filepath'
                path='temp_data/'
            else:
                print('No file to read, defaulting to method')

        if method=='filepath':
            filepath = path+filename
        elif method=='s3':

            idx = path.find('/')
            path_s3 = path[:idx]
            filename_s3 = path[idx+1:]+filename

            # Creating the low level functional client
            if aws_credentials is not None:
                aws_access_key_id,aws_secret_access_key = credentials
            else:
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY')
                aws_secret_access_key=os.getenv('AWS_SECRET_KEY')

            client = boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)

            # Create the S3 object
            obj = client.get_object(
                Bucket = path_s3,
                Key = filename_s3
            )

            filepath = obj['Body']

        data = pd.read_csv(filepath)

        if save_file:
            if not exists('temp_data/'):
                os.mkdir('temp_data/')
            data.to_csv('temp_data/'+filename,index=False)

        if drop_null_index:
            if index_column is None:
                raise ValueError('index column to drop cannot be None')
            data = data.dropna(subset=[index_column])

        data.set_index(index_column)

        return data
        
    def get_data_path(self,read_from='s3',override_path=None,project=None):

        if override_path is not None and override_path!='':
            return override_path

        project_path = get_project_path(read_from=read_from,override_path=override_path,project=project)

        return project_path+'data/'
        
    def load_data_single(self):
        params = self.params
        job_id = params['external_params']['id']
        description = params['external_params']['description']
        title = params['external_params']['title']

        data = pd.DataFrame({
            'job_id':[job_id],
            'description':[description],
            'job_title':[title]
        })

        return data

    def load_data_batch(self):

        params = self.params
        path_input_data = params['external_params']['path_input_data']
        input_filename = params['external_params']['input_filename']
        index_column = params['external_params']['index_column']
        random_state = params['data']['random_state']


        data_sample_size = params['external_params']['data_sample_size']
        read_data_from=params['data']['read_data_from']
        project_name=params['project']['project_name']

        path_input_data = params['external_params']['path_input_data']
        if path_input_data is not None or path_input_data!='':
            override_data_path = path_input_data
        else:
            override_data_path=None

        path_input_data = self.get_data_path(read_from=read_data_from,override_path=override_data_path,project=project_name)

        path_input_datafile = path_input_data+input_filename
        print(f"input file to load: {path_input_datafile}",'\n')

        print('load data')
        #retrieve data
        data = self.retrieve_data(path=path_input_data
                                      ,filename=input_filename
                                      ,drop_null_index=True
                                      ,index_column=index_column
                                      ,method=params['data']['data_method']
                                      ,save_file=True
                                      ,use_cache=True)

        if isinstance(data_sample_size, int):
            data=data.sample(data_sample_size,random_state=random_state)

        print('data size',data.shape)

        return data
        
    def get_data(self,data):
        params = self.params
        labels=params['external_params']['labels']
        keep_original_labels = validate_bool_variable(params['data']['keep_original_labels'])
        
        if data is not None:
            return data
        
        if params['inference_type']=='batch':
            data=self.load_data_batch()
        elif params['inference_type']=='single':
            data=self.load_data_single()

        if keep_original_labels is False:
            for label in labels:
                if label in data.columns:
                    data=data.drop([label],axis=1)
                
        return data

class InferenceAPI:
    
    def __init__(self,params,data):
        self.params = params
        self.data_input = data
        self.data_output = None
    
    def inference(self):
        self.data_output = self.inference_run()
        return self.data_output

    def inference_run(self):
        
        params = self.params
        data = self.data_input

        project_name_wandb=params['project']['project_name_wandb']
        entity_name_wandb = params['project']['entity_name_wandb']
        project = params['project']['project_name']

        index_column = params['external_params']['index_column']
        labels=params['external_params']['labels']

        if params['inference_type']=='batch':
            save_output_csv = params['external_params']['save_output_csv']

        path_model_s3 = params['model']['path_model_s3']
        read_model_from = params['model']['read_model_from']
        read_model_metrics_from = params['model']['read_model_metrics_from']
        use_local_model = bool(params['model']['use_local_model'])
        model_metrics_filename = params['model']['model_metrics_filename']
        device_type = get_device_type()

        #get the paths for the artifacts
        path_output, path_artifact = get_artifact_path(read_from=read_model_metrics_from,override_path=None,project=project)

        #get best results
        runs_df = get_wandb_runs(entity_name=entity_name_wandb
                                 ,project_name=project_name_wandb
                                 ,read_from=read_model_metrics_from
                                 ,path=path_output
                                 ,filename=model_metrics_filename)

        #define attributes to infer
        attributes = labels.copy()
        attributes_original = labels.copy()


        log_models={}

        tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}

        data_input = data.copy(deep=True)

        #make inference
        for att in attributes_original:

            print(f'Infering attribute: {att}')

            if att not in ['specialty','bonus']:

                #get the best model
                run_name = (runs_df[runs_df['attribute']==att]
                             .sort_values(by='accuracy',ascending=False)
                             .iloc[0]['run_name'])

                log_models[att]=run_name

                print(f'Experiments are located at: {run_name}')

                x_col = params['labels_params'][att]['x_col']

                print('preprocess data')

                data = preprocess(data,text_column_name=x_col)

                print('loading artifacts')
                path_output, path_artifact = get_artifact_path(read_from=read_model_from,run_name=run_name,project=project)

                pipe = get_language_models_pipeline(read_from=read_model_from
                                                        ,use_local=use_local_model
                                                        ,run_name=run_name
                                                        ,path_artifact=path_artifact
                                                        ,path_s3=path_model_s3
                                                        ,device_type=device_type)


                print('make predictions')
                #infer the attribute using the inference pipeline
                data[f'{att}'] = data[x_col].apply(lambda x: pipe(x,**tokenizer_kwargs)[0])

            if att=='specialty':

                print('\n----\n','predict discipline for specialty','\n----\n')

                #get the best model
                run_name = (runs_df[runs_df['attribute']=='discipline']
                             .sort_values(by='accuracy',ascending=False)
                             .iloc[0]['run_name'])

                log_models['discipline_specialty']=run_name

                print(f'Experiments are located at: {run_name}')

                x_col = params['labels_params'][att]['x_col_discipline']
                print('preprocess data')

                data = preprocess(data,text_column_name=x_col)

                print('loading artifacts')
                path_output, path_artifact = get_artifact_path(read_from=read_model_from,run_name=run_name,project=project)

                pipe = get_language_models_pipeline(read_from=read_model_from
                                            ,use_local=use_local_model
                                            ,run_name=run_name
                                            ,path_artifact=path_artifact
                                            ,path_s3=path_model_s3
                                            ,device_type=device_type)

                #infer the attribute using the inference pipeline
                print('make predictions')

                #TODO: vectorize to make it run faster
                discipline_pred=[]
                for x in tqdm(data[x_col]):
                    discipline_pred.append(pipe(x,**tokenizer_kwargs)[0])
                data[params['labels_params'][att]['col_category']] = [k['label'] for k in discipline_pred]


                print('\n----\n','predict specialty','\n----\n')

                #get the best model
                run_name = (runs_df[runs_df['attribute']==att]
                             .sort_values(by='accuracy',ascending=False)
                             .iloc[0]['run_name'])

                log_models[att]=run_name

                print(f'Experiments are located at: {run_name}')

                print('preprocess data')

                col_category = params['labels_params'][att]['col_category']
                col_text_raw = params['labels_params'][att]['col_text_raw']
                data = preprocess_data_specialty(data,col_category,x_col,col_text_raw)

                print('loading artifacts')
                path_output, path_artifact = get_artifact_path(read_from=read_model_from,run_name=run_name,project=project)

                if read_model_from=='s3':
                    path_artifact = f'temp/{run_name}/'
                    if not exists(path_artifact) or use_local_model==False:
                        print('downloading artifact from S3')
                        client = S3Client(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
                        cp = CloudPath(f"s3://{path_model_s3}{run_name}/",client=client)
                        cp.download_to(path_artifact)
                    else:
                        print('loading artifact from local folder')

                #load the pretrained model
                models=pickle.load(open(f'{path_artifact}/model.pkl', 'rb'))

                use_tags = validate_bool_variable(params['labels_params']['specialty']['use_tags'])
                data=batch_predict(models,data,col_category,x_col,use_tags=use_tags)
                data[f'{att}'] = [{'label':k,'score':.99} for k in data['pred']]
                data=data.drop(['pred'],axis=1)

                if params['labels_params'][att]['drop_category_col']=='True':
                    data=data.drop([params['labels_params'][att]['col_category']],axis=1)
                else:
                    data[params['labels_params'][att]['col_category']] = discipline_pred
                    if 'discipline' not in attributes_original:
                        attributes+=['discipline']

            if att=='bonus':

                print('\n----\n','predict bonus','\n----\n')

                #get the best model
                run_name = (runs_df[runs_df['attribute']==att]
                             .sort_values(by='accuracy',ascending=False)
                             .iloc[0]['run_name'])

                log_models[att]=run_name

                print(f'Experiments are located at: {run_name}')

                print('preprocess data')

                col_text_raw = params['labels_params'][att]['col_text_raw']
                x_col = params['labels_params'][att]['x_col']
                data = preprocess_data_bonus(data,col_text_raw,x_col).copy(deep=True)

                print('loading artifacts')
                path_output, path_artifact = get_artifact_path(read_from=read_model_from,run_name=run_name,project=project)

                if read_model_from=='s3':
                    path_artifact = f'temp/{run_name}/'
                    if not exists(path_artifact) or use_local_model==False:
                        print('downloading artifact from S3')
                        client = S3Client(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
                        cp = CloudPath(f"s3://{path_model_s3}{run_name}/",client=client)
                        cp.download_to(path_artifact)
                    else:
                        print('loading artifact from local folder')

                #load the pretrained model
                model=pickle.load(open(f'{path_artifact}/model.pkl', 'rb'))

                data=model.predict(data,x_col)
                
                for l in ['sign_on_bonus_available','completion_bonus_available','bonus_value']:
                    data[l] = [{'label':k,'score':.99} for k in data[l]]

            print('\n----\n')

        if 'bonus' in attributes_original:
            attributes += ['completion_bonus_available', 'sign_on_bonus_available', 'bonus_value']
            attributes.remove('bonus')


        #save csv
        if params['inference_type']=='batch' and save_output_csv:
            self.save_inference_output(data,attributes)

        #return data
        data=self.return_inference_output(data,attributes)

        return data

    def return_inference_output(self,data,attributes):
        
        params = self.params
        data_input = self.data_input

        output_format = params['run']['output_format']
        #x_col = params['labels_params']['discipline']['x_col']
        x_col='job_title'
        index_column = params['external_params']['index_column']

        if params['inference_context']=='external':

            if params['inference_type']=='single':
                output_format = 'json_no_prob'
            elif params['inference_type']=='batch' and params['external_params']['return_json']=='True':
                output_format = 'json_no_prob'
            else:
                output_format=''

        if params['inference_context']=='external':
            if params['inference_type']=='batch' and params['external_params']['save_output_csv']=='True':
                output_format_csv = 'pandas_no_prob'
            else:
                output_format_csv=''

        if output_format=='pandas_raw':
            return data
        elif output_format=='pandas_clean':
            data_json=from_raw_pandas_to_json(data,attributes,probabilities=True)
            data_clean,att_list = from_json_to_pandas(data_json)
            data_clean[x_col] = data[x_col]

            data_clean[index_column] = data_input.loc[data_clean.index][index_column]
            data_clean = data_clean.set_index(index_column).reset_index()

            return data_clean
        elif output_format=='json_no_prob':
            data_json=from_raw_pandas_to_json(data,attributes,probabilities=False)
            return data_json
        elif output_format=='json_prob':
            data_json=from_raw_pandas_to_json(data,attributes,probabilities=True)
            return data_json
        elif output_format=='None':
            return None

        raise ValueError('the parameter output_format is invalid')
        
    def save_inference_output(self,data,attributes):
        
        params = self.params
        data_input = self.data_input

        output_format_csv = params['run']['output_format_csv']
        path_output_data = params['external_params']['path_output_data']
        project = params['project']['project_name']
        read_data_from=params['data']['read_data_from']
        output_filename = params['external_params']['output_filename']
        index_column = params['external_params']['index_column']

        now = datetime.now() 
        round_time = ceil_dt(now, timedelta(minutes=30)).strftime("%d_%m_%Y__%H_%M")


        if path_output_data is None or path_output_data=='':
            path_output_data = get_output_data_path(read_from=read_data_from,override_path=None,project=project)


        d=None
        if output_format_csv=='pandas_prob':
            d=from_raw_pandas_to_json(data,attributes,probabilities=True)
            d=get_clean_dataframe(d,probabilities=True)
        elif output_format_csv=='pandas_no_prob':
            d=from_raw_pandas_to_json(data,attributes,probabilities=False)
            d=get_clean_dataframe(d,probabilities=False)

        d[index_column] = data_input.loc[d.index][index_column]
        d = d.set_index(index_column).reset_index()

        if output_filename=='':
            input_filename = params['external_params']['input_filename']
            output_filename = input_filename.replace('.csv','')+f'_predictions_{round_time}.csv'


        path_output_datafile = f'{path_output_data}{output_filename}'

        d.to_csv(path_output_datafile,index=False)

        print(f'saving csv file to {path_output_datafile}')

class RegexModelSpecialty:
    def __init__(self):
        self.patterns = []
        self.default = None
        self.use_default = False

    def get_specialty_in_job_titles(self,data,col_pred,col_text):
        '''
        Check which specialty are actually described in the job title and can be directly catched with regex
        '''
        l=[]
        for index,row in data.iterrows():
            jt = str(row[col_text]).strip()
            sp = str(row[col_pred]).strip()
            if sp in jt:
                l.append(sp)
        return list(set(l))

    def get_patterns(self,patterns=[],data=None,col_pred=None,col_text=None):

        if data is not None:
            l=self.get_specialty_in_job_titles(data,col_pred,col_text)
            patterns+=l

        patterns = [r'((^|\s|\[)'+p+r'(\]|\s|\,|$))' for p in patterns]
        
        return patterns
        
    def fit(self,patterns,data,col_pred,col_text,evaluate=False,evaluate_tag=False,use_default=False):
        
        self.patterns=self.get_patterns(patterns,data,col_pred,col_text)
        
        if use_default:
            self.default = data[col_pred].value_counts().index[0]
            self.use_default=True
        
        if evaluate:
            r=self.evaluate(data,col_text,col_pred)
        if evaluate_tag:
            r=self.evaluate_tags(data,col_text,col_pred)
        
    def predict(self,text,current_value=None):
        
        for p in self.patterns:
            result = re.search(p,text)
            if result is not None:
                return result.group(1).strip().strip('[').strip(']').strip(',')
        
        if self.use_default:
            return self.default
        
        return current_value

    def get_tags(self,text,current_value=None):
        tags=[]
        for p in self.patterns:
            result = re.search(p,text)
            if result is not None:
                tags.append(result.group(1).strip().strip('[').strip(']').strip(','))
        if len(tags)==0:
            if self.use_default:
                return [self.default]
            return [current_value]
        return tags
    
    def evaluate(self,data,col_text,col_pred,make_pred=True,total_data=None,col_predictions='pred'):
        
        if make_pred:
            predictions=data[col_text].apply(self.predict)
        else:
            predictions = data[col_predictions]

        if total_data is None:
            total_data=len(data)

        if predictions.isnull().sum()!=0:
            print("None values in pred")
            drop = predictions.isnull().sum()
        else:
            drop = 0

        acc = (predictions == data[col_pred]).sum()/total_data
        coverage = (total_data - drop)/total_data
        print(f'accuracy on data: {round(acc,2)}')
        print(f'coverage on data: {round(coverage,2)}')
        
        return acc,coverage
        
    def evaluate_tags(self,data,col_text,col_pred,make_pred=True,total_data=None,col_tags='tags'):
        
        if make_pred:
            tags=data[col_text].apply(self.get_tags)
            data['tags']=tags
        else:
            data['tags'] = data[col_tags]

        if total_data is None:
            total_data=len(data)

        if data['tags'].isnull().sum()!=0:
            print("None values in pred")
            drop = data['pred'].isnull().sum()
            data=data.dropna(subset=['tags'])
        else:
            drop = 0


        data['result_tags']=data[[col_pred,'tags']].apply(lambda x: x[0] in x[1] if x[1] is not None else False,axis=1)
        
        acc = data['result_tags'].sum()/len(data)
        coverage = (total_data - drop)/total_data
        print(f'tags accuracy on data: {round(acc,2)}')
        print(f'tags coverage on data: {round(coverage,2)}')
        
        return acc,coverage

class RegexModelBonus:
    
    def __init__(self):
        self.patterns = []
        
    def get_patterns(self,extra_patterns=None):
        
        patterns={
            'bonus_available': {
                'sign_on':[
                    r'([S|s]ign(\s|\-|)[O|o]n [b|B]onus)'
                    ,r'(sign-on/referral bonus)'
                    ,r'([S|s]ign[\s|\.][O|o]n)'
                ]
                ,'completion': [
                    r'(completion bonus)'
                    ,r'(bonus at end of term)'
                    ,r'(end of term bonus)'
                    ,r'(bonus after)'
                ]
            }
            ,'bonus_value':[
                    r'(\$.*)[\s|\.][S|s]ign[\s|\-][O|o]n [b|B]onus'

                    ,r'(\d+[k|K])[\s|\.][S|s]ign[\s|\-][O|o]n [b|B]onus'

                    ,r'(\d+,\d+)[\s|\.][S|s]ign[\s|\-][O|o]n [b|B]onus'

                    ,r'[\s|\.][S|s]ign[\s|\.][O|o]n [b|B]onus[\s|](\$\d+(\,|)\d+)'

                    ,r'\$(.*)bonus'

                    ,r'(\d+[k|K])[\s|\.][S|s]ign[\s|\-][O|o]n/referral bonus'
                ]
        }
        
        if extra_patterns is not None:
            patterns['extra'] = extra_patterns
        
        return patterns
    
    def convert_money_str_to_num(self,text):
        
        if pd.isnull(text):
            return text
        
        p=r'(\d+)[k|K]'
        n=re.search(p,text)
        if n is not None:
            return float(n.group(1))*1000

        p=r'(\d+(\,|)\d+)'
        n=re.search(p,text)
        if n is not None:
            return float(n.group(1).replace(',',''))
        
        

        return 'NA'
        
    def get_sign_on_available(self,data,col_text):
        
        patterns_exist_completion_bonus = self.patterns['bonus_available']['completion']
        data['completion_bonus_available_text'] = data[col_text].apply(lambda x: self.search_patterns(x,patterns_exist_completion_bonus))
        data['completion_bonus_available'] =  [None if pd.isnull(k) else bool(k) for k in data['completion_bonus_available_text']]

        
        patterns_exist_sign_on_bonus = self.patterns['bonus_available']['sign_on']
        data['sign_on_bonus_available_text'] = data[col_text].apply(lambda x: self.search_patterns(x,patterns_exist_sign_on_bonus))
        data['sign_on_bonus_available'] =  [None if pd.isnull(k) else bool(k) for k in data['sign_on_bonus_available_text']]
        temp = pd.Series([None if pd.isnull(k) else not k for k in data['completion_bonus_available']],index=data.index)
        data['sign_on_bonus_available'] = data['sign_on_bonus_available'].fillna(temp)
        
        return data
    
    def get_bonus_value(self,data,col_text):
        
        patterns_bonus_value = self.patterns['bonus_value']
        data['bonus_value_text'] = data[col_text].apply(lambda x: self.search_patterns(x,patterns_bonus_value))
        data['bonus_value'] = data['bonus_value_text'].apply(self.convert_money_str_to_num)
        
        return data
    
    def search_patterns(self,text,patterns,group_number=1,current=None):
        if pd.isnull(text):
            return text
        for p in patterns:
            r=re.search(p,text)
            if r is not None:
                return r.group(group_number).strip()
        return current
    
    def fit(self,extra_patterns=None):
        
        self.patterns = self.get_patterns(extra_patterns)
        
    def predict(self,data,col_text):
        
        if self.patterns==[]:
            raise ValueError('model is not fitted')
            
        data=self.get_sign_on_available(data,col_text)
        data=self.get_bonus_value(data,col_text)
        data=data.drop(['sign_on_bonus_available_text','completion_bonus_available_text','bonus_value_text'],axis=1)
        
        return data

## Upload models from local to S3
# read_from = 'local'
# path_data,path_output,path_artifact = get_datapath(read_from=read_from,run_name=None,override_path=None)
# runs_df = get_wandb_runs(entity_name=params['project']['entity_name']
#                          ,project_name=params['project']['project_name']
#                          ,read_from='local'
#                          ,path=path_output
#                          ,filename='model_metrics.csv')
# path_local = path_output

# path_data,path_output,path_artifact = get_datapath(read_from='s3',run_name=None,override_path=None)
# path = path_output
# idx = path.find('/')
# bucketname = path[:idx]
# path_bucket = path[idx+1:]

# path_local,path_bucket

# ids=[]
# attributes = runs_df['attribute'].unique()
# attributes = ['specialty']
# for att in attributes:
#     if not pd.isnull(att):
#         aux=runs_df[runs_df['attribute']==att]
#         ids.append(aux.sort_values(by='accuracy',ascending=False).iloc[0,0])
# aux=runs_df[runs_df['run_id'].isin(ids)]

# for run_name in aux['run_name']:
#     full_path_local = path_local+run_name
#     full_path_bucket = path_bucket+run_name+'/'
#     r=uploadDirectory(full_path_local,bucketname,full_path_bucket)
