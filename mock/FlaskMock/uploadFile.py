#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/9 22:53
@Author  : Poco Ray
@File    : uploadFile.py
@Software: PyCharm
@Desc    : 上传文件接口Mock
"""
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "img"


@app.route('/upload', methods=['POST'])
def upload():
    if "image" not in request.files:
        data = {
            "msg": "当前用户未填写image参数！",
            "code": 400
        }
        return jsonify(data)

    file = request.files['image']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    data = {
        "msg": "文件上传成功！",
        "code": 200
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run()
