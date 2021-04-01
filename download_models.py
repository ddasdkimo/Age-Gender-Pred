# -*- coding: utf-8 -*-
import wget
import zipfile
import os

def zip_list(file_path):
    zf = zipfile.ZipFile(file_path, 'r')
    zf.extractall()

if not os.path.isdir("models/"):
    os.mkdir("models/")
wget.download('https://ftpweb.intemotech.com/rai_ai_models/age_gender_models/models.zip', out='models/modwls.zip')
zip_list('models/modwls.zip')

os.remove('models/modwls.zip')
