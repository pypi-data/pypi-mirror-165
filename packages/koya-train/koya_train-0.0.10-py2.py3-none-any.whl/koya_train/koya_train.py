import pytest
import ipytest

import pandas as pd
from tqdm import tqdm
import numpy as np
import urllib
from datetime import date, timedelta
from itertools import permutations
import datetime
import string
from IPython.core.display import display, HTML
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from IPython.display import Image
from IPython import get_ipython
import html2text
import torch
import datasets
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
# import wandb
import re

from transformers.utils.dummy_pt_objects import TRANSFO_XL_PRETRAINED_MODEL_ARCHIVE_LIST


def identify_tensor_device():
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    return device


def get_datapath(context,run_name=None):
    if context == 'local-drive':
        path_root = '/Volumes/GoogleDrive/My Drive/'
    elif context == 'gdrive':
        path_root = '/content/drive/MyDrive/'

    path_project = path_root+'Data Science/Projects/Vivian-Health/'
    path_data = path_project+'data/'
    path_output = path_project+'artifacts/'

    if run_name is None:
        path_artifact = None
    else:
        path_artifact = path_output+f'{run_name}'

    return path_data,path_output,path_artifact


def retrieve_data(path, index_column, method='filepath'):
    if method == 'filepath':
        data = pd.read_csv(path)
    else:
        raise NotImplementedError(f'Method {method} is not implemented.')
    
    data = data.dropna(subset=[index_column]).set_index(index_column)

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
                    ,path_filename=None
                    ,metric_name='best_accuracy'
                    ,metric_name_show='accuracy'
                    ,filters={'state':'finished'}
                    ,drop_on_metric=True):

    
    if read_from=='local':
        runs_df = pd.read_csv(path_filename)
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

def from_json_to_pandas(d,id_name='job_id'):
    key_list = list(d.keys())
    att_list = list(d[list(d.keys())[0]].keys())
    newd={}
    newd[id_name] = key_list
    for att in att_list:
        label_list, score_list = [],[]
        for k,v in d.items():
            label_list.append(v[att]['label'])
            score_list.append(v[att]['score'])

        newd[f'{att}-label']=label_list
        newd[f'{att}-score']=score_list
    return pd.DataFrame(newd).set_index(id_name),att_list

def from_raw_pandas_to_json(data,attributes):
    d={}
    for index,row in data.iterrows():
        temp_col={}
        for col in attributes:
            temp_col[col]=row[col]
        d[index]=temp_col
    return d

def get_clean_dataframe(d):
    data,att_list = from_json_to_pandas(d)
    for att in att_list:
        data=data.rename(columns={f'{att}-label':att})
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