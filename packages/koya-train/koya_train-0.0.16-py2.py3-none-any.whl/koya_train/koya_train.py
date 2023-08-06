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

from transformers.utils.dummy_pt_objects import TRANSFO_XL_PRETRAINED_MODEL_ARCHIVE_LIST


def get_datapath(read_from='s3',run_name=None,override_path=None):
    
    if read_from == 'local':
        path_root = '/Volumes/GoogleDrive/My Drive/'
    elif read_from == 'gdrive':
        path_root = '/content/drive/MyDrive/'
    elif read_from == 's3':
        path_root = 'koya/'
    
    if override_path is not None:
        path_project = override_path
    else:
        path_project = path_root+'Data Science/Projects/Vivian-Health/'
    
    path_data = path_project+'data/'
    path_output = path_project+'artifacts/'

    if run_name is None:
        path_artifact = None
    else:
        path_artifact = path_output+f'{run_name}'

    return path_data,path_output,path_artifact


def retrieve_data(path,filename,drop_null_index=False,index_column=None,method='filepath',use_cache=False,save_file=False):
    
    
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
        client = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

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


#TO_DO figure out how to truncate using the tokenizer and execute this in the pipeline
def truncate_words(text,max_lenght=510,opt='right'):
    if len(text.split())<=max_lenght:
        return text
    else:
        return ' '.join(text.split()[:max_lenght])

def clean_text(text,max_lenght=250):
    text_maker = html2text.HTML2Text()
    text = text_maker.handle(text)
    text = truncate_words(text,max_lenght)
    return [text]

def get_wandb_runs(entity_name
                    ,project_name
                    ,read_from='local'
                    ,path=None
                    ,filename=None
                    ,metric_name='best_accuracy'
                    ,metric_name_show='accuracy'
                    ,filters={'state':'finished'}
                    ,drop_on_metric=True):

    
    if read_from=='local':
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
    else:
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

def batch_predict(models,data,col_category,x_col):
    data['pred'] = None
    categories = data[col_category].unique()

    for category in tqdm(categories):

        if not pd.isnull(category):

            sub_data = data[data[col_category]==category].copy(deep=True)

            model = models[category]

            sub_data['pred'] = sub_data[x_col].apply(model.predict)

        data['pred']=data['pred'].fillna(sub_data['pred'])
    return data

def preprocess_data_specialty(data,col_category,x_col,col_text_raw):
    categories = data[col_category].unique()
    data[x_col]=None

    for category in tqdm(categories):
        if not pd.isnull(category):
            sub_data = data[data[col_category]==category].copy(deep=True)
            sub_data[x_col] = data[col_text_raw].apply(lambda x: process_acronym(x,category))
            data[x_col]=data[x_col].fillna(sub_data[x_col])
    return data


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
                return result.group(1).strip().strip('[').strip(']')
        
        if self.use_default:
            return self.default
        
        return current_value

    def get_tags(self,text,current_value=None):
        tags=[]
        for p in self.patterns:
            result = re.search(p,text)
            if result is not None:
                tags.append(result.group(1).strip())
        if len(tags)==0:
            return current_value
        return tags
    
    def evaluate(self,data,col_text,col_pred):
        
        predictions=data[col_text].apply(self.predict)
        acc = (predictions == data[col_pred]).sum()/len(data)
        coverage = (len(predictions) - predictions.isnull().sum())/len(predictions)
        print(f'accuracy on data: {round(acc,2)}')
        print(f'coverage on data: {round(coverage,2)}')
        
        return acc,coverage
        
    def evaluate_tags(self,data,col_text,col_pred):
        
        tags=data[col_text].apply(self.get_tags)
        data['tags']=tags
        data['result_tags']=data[[col_pred,'tags']].apply(lambda x: x[0] in x[1] if x[1] is not None else False,axis=1)
        
        acc = data['result_tags'].sum()/len(data)
        coverage = (len(tags) - tags.isnull().sum())/len(tags)
        print(f'tags accuracy on data: {round(acc,2)}')
        print(f'tags coverage on data: {round(coverage,2)}')
        
        return acc,coverage

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

def load_internal_params(inference_context,update_internal_params=None):

    internal_params = {    
            "data":{
                "data_method":"s3" #the method to read the input data
                ,"random_state":"2" #the random_state to use
            }
            ,"project":{
                "project_name":"vivian-health" #project name to be tracked in weights and biases
                ,"entity_name":"koya-test2" #the entity name to be tracked in weights and biases
                ,'read_from':'local'
            }
            ,"run":{
                "output_format":"json_prob" #options: json, pandas_clean, pandas_raw
                ,"output_format_csv":"pandas_prob" #options: json, pandas_clean, pandas_raw
                ,"read_from":"s3"
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
                }
            }
            ,"output":{}
            ,"inference_context":inference_context
        }

    if inference_context=='internal' and update_internal_params is not None:
        for k,v in internal_params.items():
            if k in update_internal_params:
                for k2,v2 in update_internal_params[k].items():
                    internal_params[k][k2]=update_internal_params[k][k2]

    return internal_params

def load_data_single(params):
    #load Data
    job_id = params['external_params']['id']
    description = params['external_params']['description']
    title = params['external_params']['title']

    data = pd.DataFrame({
        'job_id':[job_id],
        'description':[description],
        'job_title':[title]
    })

    return data

def load_data_batch(params):

    #load Data
    path_input_data = params['external_params']['path_input_data']
    input_filename = params['external_params']['input_filename']
    index_column = params['external_params']['index_column']
    data_sample_size = params['external_params']['data_sample_size']
    read_from  =params['run']['read_from']
    override_project_path = params['external_params']['override_project_path']
    if override_project_path == 'None':
        override_project_path = None

    if path_input_data=="":
        path_input_data,path_output,path_artifact = get_datapath(read_from=read_from,run_name=None,override_path=override_project_path)
    
    path_input_datafile = path_input_data+input_filename
    print(f"input file to load: {path_input_datafile}",'\n')
    
    print('load data')
    #retrieve data
    data = retrieve_data(path=path_input_data
                                  ,filename=input_filename
                                  ,drop_null_index=True
                                  ,index_column=index_column
                                  ,method=params['data']['data_method']
                                  ,save_file=True
                                  ,use_cache=True)
    
    if params['data']['random_state'] != '':
        random_state = int(params['data']['random_state'])
    else:
        random_state=1
    
    if data_sample_size != '':
        size = int(data_sample_size)
        data=data.sample(size,random_state=random_state)

    return data

def inference(params):

    context = params['context']

    now = datetime.now() 
    round_time = ceil_dt(now, timedelta(minutes=30)).strftime("%d_%m_%Y__%H_%M")
    index_column = params['external_params']['index_column']
    labels=params['external_params']['labels']

    if params['inference_type']=='batch':
        path_input_data = params['external_params']['path_input_data']
        input_filename = params['external_params']['input_filename']
        index_column = params['external_params']['index_column']
        data_sample_size = params['external_params']['data_sample_size']
        save_output_csv = params['external_params']['save_output_csv']
        path_output_data = params['external_params']['path_output_data']
        output_filename = params['external_params']['output_filename']
        override_project_path=params['external_params']['override_project_path']
        if override_project_path =='' or override_project_path=='None':
            override_project_path = None
    else:
        override_project_path = None

    output_format_csv = params['run']['output_format_csv']
    output_format = params['run']['output_format']
    read_from = params['run']['read_from']





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

    #get the paths for the artifacts
    path_data,path_output,path_artifact = get_datapath(read_from=read_from,run_name=None,override_path=override_project_path)

    #get best results
    runs_df = get_wandb_runs(entity_name=params['project']['entity_name']
                             ,project_name=params['project']['project_name']
                             ,read_from=read_from
                             ,path=path_output
                             ,filename='model_metrics.csv')

    #define attributes to infer
    attributes = labels
    attributes_original = labels

    log_models={}

    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}

    #load data
    data=None
    if params['inference_type']=='batch':
        data=load_data_batch(params)
    elif params['inference_type']=='single':
        data=load_data_single(params)

    for att in attributes:
        if att in data.columns:
            data=data.drop([att],axis=1)

    if torch.backends.mps.is_available():
        device_type = "mps"
    elif torch.cuda.is_available():
        device_type = "cuda"
    else:
        device_type = "cpu"

    #make inference
    for att in attributes_original:

        print(f'Infering attribute: {att}')

        if att!='specialty':

            #get the best model
            run_name = (runs_df[runs_df['attribute']==att]
                         .sort_values(by='accuracy',ascending=False)
                         .iloc[0]['run_name'])

            log_models[att]=run_name

            print(f'Experiments are located at: {run_name}')

            #get the paths for the artifacts
            path_data,path_output,path_artifact = get_datapath(read_from=read_from,run_name=run_name,override_path=override_project_path)

            x_col = params['labels_params'][att]['x_col']

            print('preprocess data')

            data = preprocess(data,text_column_name=x_col)

            print('loading artifacts')

            if read_from=='s3':
                path_artifact = f'temp/{run_name}/'
                if not exists(path_artifact):
                    if not exists('temp/'):
                        os.mkdir('temp/')
                    client = S3Client(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
                    cp = CloudPath(f"s3://koya/Data Science/Projects/Vivian-Health/artifacts/{run_name}/",client=client)
                    cp.download_to(path_artifact)


            #load the pretrained model
            model = AutoModelForSequenceClassification.from_pretrained(path_artifact)

            #load the pretrained tokenizer
            tokenizer = AutoTokenizer.from_pretrained(path_artifact)

            #create the pipeline using the model and tokenizer
            if device_type=='cpu':
                pipe = pipeline(task="text-classification",model=model, tokenizer=tokenizer, return_all_scores=False)
            else:
                pipe = pipeline(task="text-classification",model=model, tokenizer=tokenizer, return_all_scores=False,device=0)


            #infer the attribute using the inference pipeline
            #data[f'pred-{att}'] = data[text_column_name].apply(lambda x: pipe(clean_text(x)))
            l=[]
            for x in tqdm(data[x_col]):
                l.append(pipe(x,**tokenizer_kwargs)[0])
            data[f'{att}'] = l

        else:

            print('\n----\n','predict discipline for specialty','\n----\n')

            #get the best model
            run_name = (runs_df[runs_df['attribute']=='discipline']
                         .sort_values(by='accuracy',ascending=False)
                         .iloc[0]['run_name'])

            log_models['discipline_specialty']=run_name

            print(f'Experiments are located at: {run_name}')

            #get the paths for the artifacts
            path_data,path_output,path_artifact = get_datapath(read_from=read_from,run_name=run_name,override_path=override_project_path)

            x_col = params['labels_params'][att]['x_col_discipline']

            print('preprocess data')

            data = preprocess(data,text_column_name=x_col)

            print('loading artifacts')

            if read_from=='s3':
                path_artifact = f'temp/{run_name}/'
                if not exists(path_artifact):
                    if not exists('temp/'):
                        os.mkdir('temp/')
                    client = S3Client(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
                    cp = CloudPath(f"s3://koya/Data Science/Projects/Vivian-Health/artifacts/{run_name}/",client=client)
                    cp.download_to(path_artifact)

            #load the pretrained model
            model = AutoModelForSequenceClassification.from_pretrained(path_artifact)

            #load the pretrained tokenizer
            tokenizer = AutoTokenizer.from_pretrained(path_artifact)

            #create the pipeline using the model and tokenizer
            if device_type=='cpu':
                pipe = pipeline(task="text-classification",model=model, tokenizer=tokenizer, return_all_scores=False)
            else:
                pipe = pipeline(task="text-classification",model=model, tokenizer=tokenizer, return_all_scores=False,device=0)

            #infer the attribute using the inference pipeline
            #data[f'pred-{att}'] = data[text_column_name].apply(lambda x: pipe(clean_text(x)))
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

            #get the paths for the artifacts
            path_data,path_output,path_artifact = get_datapath(read_from=read_from,run_name=run_name,override_path=override_project_path)


            print('preprocess data')

            col_category = params['labels_params'][att]['col_category']
            col_text_raw = params['labels_params'][att]['col_text_raw']
            data = preprocess_data_specialty(data,col_category,x_col,col_text_raw)

            print('loading artifacts')

            if read_from=='s3':
                path_artifact = f'temp/{run_name}/'
                if not exists(path_artifact):
                    if not exists('temp/'):
                        os.mkdir('temp/')
                    client = S3Client(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
                    cp = CloudPath(f"s3://koya/Data Science/Projects/Vivian-Health/artifacts/{run_name}/",client=client)
                    cp.download_to(path_artifact)

            #load the pretrained model
            models=pickle.load(open(f'{path_artifact}/model.pkl', 'rb'))

            data=batch_predict(models,data,col_category,x_col)
            data[f'{att}'] = [{'label':k,'score':.99} for k in data['pred']]
            data=data.drop(['pred'],axis=1)

            if params['labels_params'][att]['drop_category_col']=='True':
                data=data.drop([params['labels_params'][att]['col_category']],axis=1)
            else:
                data[params['labels_params'][att]['col_category']] = discipline_pred
                if 'discipline' not in attributes_original:
                    attributes+=['discipline']

        print('\n----\n')

    attributes = set(attributes)

    if params['inference_type']=='batch' and save_output_csv=='True':
        d=None
        if output_format_csv=='pandas_prob':
            d=from_raw_pandas_to_json(data,attributes,probabilities=True)
            d=get_clean_dataframe(d,probabilities=True)
        elif output_format_csv=='pandas_no_prob':
            d=from_raw_pandas_to_json(data,attributes,probabilities=False)
            d=get_clean_dataframe(d,probabilities=False)


        if path_output_data=='':
            path_output_data = path_input_data

        if output_filename=='':
            output_filename = input_filename.replace('.csv','')+f'_predictions_{round_time}.csv'

        path_output_datafile = f'{path_output_data}{output_filename}'

        d.to_csv(path_output_datafile)

        params['output']["output_filename"] = output_filename
        params['output']["path_output_data"] = path_output_data

        print(f'saving csv file to {path_output_datafile}')


    params['output']['log_models'] = log_models
    params['output']['datetime'] = round_time

    #     run_name = f'predictions__filename_[{output_filename}]'
    #     run = wandb.init(project=params['project']['project_name']
    #                  , entity=params['project']['entity_name']
    #                  , name=run_name
    #                  ,reinit=True)

    #     for k in params.keys():
    #         run.summary[k] = str(params[k])
    #     run.finish()

    if output_format=='pandas_raw':
        return data
    elif output_format=='pandas_clean':
        data_json=from_raw_pandas_to_json(data,attributes,probabilities=True)
        data_clean,att_list = from_json_to_pandas(data_json)
        data_clean[x_col] = data[x_col]
        return data_clean
    elif output_format=='json_no_prob':
        data_json=from_raw_pandas_to_json(data,attributes,probabilities=False)
        return data_json
    elif output_format=='json_prob':
        data_json=from_raw_pandas_to_json(data,attributes,probabilities=True)
        return data_json

    return None


def uploadDirectory(path_local,bucketname,path_bucket):
    s3C = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
    for root,dirs,files in tqdm(os.walk(path_local)):
        for file in files:
            built = os.path.join(root,file)
            out = path_bucket+file
            s3C.upload_file(Filename=built,Bucket=bucketname,Key=out)