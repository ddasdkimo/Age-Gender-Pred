# -*- coding: utf-8 -*-
import wget
import tarfile
import os
import shutil

def zip_list(file_path):
    zf = zipfile.ZipFile(file_path, 'r')
    zf.extractall()


if not os.path.isdir("pics/"):
    os.mkdir("pics/")

wget.download('https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/wiki_crop.tar',
              out='pics/wiki_crop.tar')
tar = tarfile.open('pics/wiki_crop.tar')
tar.extractall()
os.remove('pics/wiki_crop.tar')
shutil.move('wiki_crop','pics/wiki_crop')
wget.download('https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar',
              out='pics/imdb_crop.tar')
tar = tarfile.open('pics/imdb_crop.tar')
tar.extractall()
shutil.move('imdb_crop','pics/imdb_crop')
os.remove('pics/imdb_crop.tar')

