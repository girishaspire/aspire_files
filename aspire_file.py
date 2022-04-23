import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
import pandas as pd


def header_class_file():
    header_categories =  (""""https://drive.google.com/file/d/1H_5-fHVhUCy-JNsPKaHjzfiKM0mqOaBw/view?usp=sharing"\n""")
    path1 = re.compile(r"d/(.*?)/view").search(header_categories).group(1)
    fileDownloaded = drive.CreateFile({'id':path1})
    header_file = fileDownloaded.GetContentFile('header_class.csv')
    return pd.read_csv("/content/header_class.csv", usecols=['Entity','Header_Class'])

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
