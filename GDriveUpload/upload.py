from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
import os
from os import listdir
from os.path import isfile, join

conf = yaml.safe_load(open('./config.yml'))
folder = conf['folderid']['id']
dir = conf['directory']['dir']
#title = conf['directory']['title']

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

#uploads file
def upload():
    os.chdir(dir)
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    for file in files:
        file1 = drive.CreateFile({'parents': [{'id': folder}]})
        print(file)
        file1.SetContentFile(file)
        file1.Upload()


upload()
