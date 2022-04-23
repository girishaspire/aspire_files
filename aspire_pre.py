import pandas as pd
# import pymysql
# import pymysql.cursors
import re
import time
import numpy as np
# import smshelper as helper
import math
from typing import List, Optional, Any
from datetime import datetime
import copy
from tqdm import tqdm
from tqdm.notebook import tqdm_notebook
import json
from functools import reduce
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)





def add_entity_name(data, header_entity):
    """
    Add Entity name/Company name corresponding to SMS address in the data DataFrame and returns it.
    Add "" if Entity corresponding to any SMS address is not present.
    data : DataFrame having SMS address column.
    header_entity : DataFrame having Header to Entity mapping.
    Returns DataFrame.
    """
    #header_entity = pd.read_csv(header_file_path)
    # Header = last 6 characters of SMS address for Indian Entities
    data['Header'] = data['address'].map(lambda address: address[-6:])

    data = data.merge(header_entity[['Header','Principal Entity Name']], on='Header', how='left')
    data['Principal Entity Name'].fillna(value='', inplace=True)
    data.rename(columns={'Principal Entity Name':'Entity'}, inplace=True)
    
    return data

def add_entity_category(data, entity_category):
    """
    Add Entity category to data
    Add "" if Entity corresponding to any SMS address is not present.
    data : DataFrame having SMS address column.
    header_entity : DataFrame having Header to Entity mapping.
    Returns DataFrame.
    """
    #header_entity = pd.read_csv(header_file_path)
    # Header = last 6 characters of SMS address for Indian Entities
    
    data = pd.merge(data,entity_category[['Entity','Type']], on = 'Entity', how = 'left')
    data['Type'] = data['Type'].str.lower().fillna(value='not categorized')
    
    return data

######### Adds header category to dataframe ##############
def add_header_category (data,header_categories):
    data = pd.merge(data,header_categories,on= 'Header', how = 'left')
    data['Header_Class'] = data['Header_Class'].fillna(value= 0).astype(int)
#     data['Balance_header'].fillna(value= 0, inplace=True)
    # data['Credit_header'].fillna(value= 0, inplace=True)
    return data



def header_class_file():
    header_categories =  (""""https://drive.google.com/file/d/1H_5-fHVhUCy-JNsPKaHjzfiKM0mqOaBw/view?usp=sharing"\n""")
    path1 = re.compile(r"d/(.*?)/view").search(header_categories).group(1)
    fileDownloaded = drive.CreateFile({'id':path1})
    header_file = fileDownloaded.GetContentFile('header_class.csv')
    return pd.read_csv("/content/header_class.csv", usecols=['Header','Header_Class'])

def Entity_class_file():
    entity_classification =  (""""https://drive.google.com/file/d/1hNultpiWzfOqnQVPztwDMDAqi1jbTTg5/view?usp=sharing"\n""")
    path2 = re.compile(r"d/(.*?)/view").search(entity_classification).group(1)
    fileDownloaded = drive.CreateFile({'id':path2})
    entity_class =  fileDownloaded.GetContentFile('entity_classification.csv')
    return pd.read_csv('/content/entity_classification.csv', usecols=['Entity','Company Brand', 'Type'])

def Entity_header_file():
    entity_header =  (""""https://drive.google.com/file/d/1An_ifwT0ZGmHp9cWBQGQOa40JlrCXWDH/view?usp=sharing"\n""")
    path3 = re.compile(r"d/(.*?)/view").search(entity_header).group(1)
    fileDownloaded = drive.CreateFile({'id':path3})
    entity_header =  fileDownloaded.GetContentFile('Entiy_header.csv')
    return pd.read_csv('/content/Entiy_header.csv')

def result_preproccessing(data):
    header_categories = header_class_file()
    entity_category = Entity_class_file()
    header_entity = Entity_header_file()

    data = add_entity_name(data, header_entity)
    data = add_entity_category(data, entity_category)
    data = add_header_category (data,header_categories)

    return data
