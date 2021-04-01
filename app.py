from flask import Flask, escape, request, jsonify, make_response, render_template
import json
import os
import time
from PIL import Image
import cv2
import numpy as np
from flask_cors import CORS
from ai_tools import AiTools
app = Flask(__name__)
CORS(app)
mAiTools = AiTools()


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
    if not os.path.isdir("photo/"):
        os.mkdir("photo/")
    if not os.path.isdir("photo/"+name):
        os.mkdir("photo/"+name)
    filename = "photo/"+name+"/"+fileName+".jpg"
    img.save(filename)
    detectImgNp = cv2.imread(filename)
    labeled, gen_pred, age_pred_arr, point_arr = mAiTools.detect(detectImgNp)
    end = time.time()
    print("資料處理時間：%f 秒" % (end - start))

    filename = "photo/"+name+"/"+fileName+"_detect.jpg"
    img.save(filename)
    cv2.imwrite(filename, labeled)
    arr = []
    for i in range(len(point_arr)):
        arr.append({
            "name": "age_gender",
            "point": point_arr[i],
            "value": int2gender[gen_pred[i]] + "," + str(age_pred_arr[i])
        })

    return jsonify(arr)
