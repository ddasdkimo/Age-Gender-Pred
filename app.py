from flask import Flask, escape, request, jsonify, make_response, render_template
import json
import os
import time
from PIL import Image
import cv2
import numpy as np
from flask_cors import CORS
from ai_tools import AiTools
import threading
import shutil

app = Flask(__name__)
CORS(app)
mAiTools = AiTools()

savepath = "/dev/shm/"

threadarrLock = threading.Lock()

def delfile(path,name,findhead,imagelist):
    try:
        if findhead:
            shutil.move(path+name, "/face/findhead/inf_"+imagelist[0][0]["value"]+os.path.basename(name))
        else:
            shutil.move(path+name, "/face/notfindhead/"+os.path.basename(name))
    except:
        print("delerror")


@app.route("/detect", methods=['POST'])
def detect():
    start = time.time()
    int2gender = {0: 'Female', 1: 'Male'}
    name = "unknown"
    img = request.files.get('file')
    name = request.values['token']
    end = time.time()
    print("檔案接收時間：%f 秒" % (end - start))
    start = time.time()
    # 使用時間戳記當作檔案名稱
    fileName = str(time.time())
    # 檢查資料夾是否存在
    if not os.path.isdir(savepath+"photo/"):
        os.mkdir(savepath+"photo/")
    if not os.path.isdir(savepath+"photo/"+name):
        os.mkdir(savepath+"photo/"+name)
    filename = "photo/"+name+"/"+fileName+".jpg"
    img.save(savepath+filename)
    detectImgNp = cv2.imread(savepath+filename)
    labeled, gen_pred, age_pred_arr, point_arr, p = mAiTools.detect(
        detectImgNp)
    end = time.time()
    print("資料處理時間：%f 秒" % (end - start))

    # filename = "photo/"+name+"/"+fileName+"_detect.jpg"
    # img.save(filename)
    # cv2.imwrite(filename, labeled)
    arr = []
    for i in range(len(point_arr)):
        arr.append({
            "name": "age_gender",
            "point": point_arr[i],
            "value": int2gender[gen_pred[i]] + "," + str(age_pred_arr[i]),
            "p": p
        })
    try:
        os.remove(savepath+filename)
    except OSError as e:
        print(e)
    return jsonify(arr)


@app.route("/detects", methods=['POST'])
def detects():
    start = time.time()
    imagelist = []

    int2gender = {0: 'Female', 1: 'Male'}
    name = "unknown"
    files = request.files
    for fileitem in files:
        img = request.files.get(fileitem)
        name = request.values['token']
        # 使用時間戳記當作檔案名稱
        fileName = str(time.time())
        # 檢查資料夾是否存在
        if not os.path.isdir(savepath+"photo/"):
            os.mkdir(savepath+"photo/")
        if not os.path.isdir(savepath+"photo/"+name):
            os.mkdir(savepath+"photo/"+name)
        filename = "photo/"+name+"/"+fileName+".jpg"
        img.save(savepath+filename)
        detectImgNp = cv2.imread(savepath+filename)
        threadarrLock.acquire()
        print("run")
        labeled, gen_pred, age_pred_arr, point_arr, p = mAiTools.detect(
            detectImgNp)
        threadarrLock.release()
        findhead = False
        arr = []
        for i in range(len(point_arr)):
            
            if point_arr[i]['xmin'] + point_arr[i]['ymin'] > 0 or point_arr[i]['xmax'] != detectImgNp.shape[0] or point_arr[i]['ymax'] != detectImgNp.shape[1]:
                findhead = True
            if point_arr[i]['xmin'] + point_arr[i]['ymin'] == 0 and findhead:
                point_arr[i]['xmin'] = point_arr[i]['xmin'] + 1
                    
            
            arr.append({
                "name": "age_gender",
                "point": point_arr[i],
                "value": int2gender[gen_pred[i]] + "," + str(age_pred_arr[i]),
                "p": p
            })
        imagelist.append(arr)
        try:
            # os.remove(savepath+filename)
            delf = threading.Thread(target = delfile, args = (savepath,filename,findhead,imagelist))
            delf.start()
        except OSError as e:
            print(e)
    end = time.time()
    print("資料處理時間：%f 秒" % (end - start))
    print("end")
    return jsonify(imagelist)
