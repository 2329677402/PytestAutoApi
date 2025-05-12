#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/12 01:11
@Author  : Poco Ray
@File    : FlaskMockServer.py
@Software: PyCharm
@Desc    : Description
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# 假设从数据库中获取的用户数据如下
db_user = {"username": "poco", "password": "123456"}

# 自定义返回数据
# 1. 登录成功
MSG_LOGIN_SUCCESS = {
    "msg": "登录成功",
    "code": 200,
    "data": {"token": "1234567890"}
}
# 2. 参数不能为空
MSG_DATA_NOT_NULL = {
    "msg": "参数不能为空",
    "code": 400,
    "data": ""
}
# 3. 密码错误
MSG_PASSWORD_NULL = {
    "msg": "密码错误",
    "code": 401,
    "data": ""
}
# 4. 用户名不存在
MSG_USERNAME_NULL = {
    "msg": "用户名不存在",
    "code": 404,
    "data": ""
}
# 5. 参数填写错误
MSG_DATA_ERROR = {
    "msg": "参数填写错误",
    "code": 405,
    "data": ""
}
# 6. 登录失效或登录用户信息有误
MSG_LOGIN_ERROR = {
    "msg": "登录失效或登录用户信息有误",
    "code": 406,
    "data": ""
}


def str_rep(res) -> dict:
    """
    将请求参数的字段转为小写
    :param res:
    :return:
    """
    new_dict = {}
    for k, v in res.items():
        if isinstance(k, str):
            k = k.lower()
        new_dict[k] = v
    return new_dict


@app.route("/")
@app.route("/index.html")
def index():
    return "欢迎来到FlaskMock的世界！"


@app.route('/api/login', methods=['POST'])
def login():
    # 1. 用户请求数据
    res = request.get_json()
    # res = request.json
    # res = request.get_data()
    # res = request.data

    # 忽略大小写
    res = str_rep(res)
    print(res)

    try:
        # 2. 获取用户名和密码
        username = res["username"]
        password = res["password"]
    except KeyError:
        return jsonify(MSG_DATA_ERROR)
    else:

        # 3. 进行数据校验
        # 1> 参数不能为空
        # 2> 登录成功
        # 3> 密码错误
        # 4> 用户不存在
        # 5> 参数填写错误
        if username == "" or password == "":
            return jsonify(MSG_DATA_NOT_NULL)
        elif username == db_user["username"] and password == db_user["password"]:
            return jsonify(MSG_LOGIN_SUCCESS)
        elif username == db_user["username"] and password != db_user["password"]:
            return jsonify(MSG_PASSWORD_NULL)
        elif username != db_user["username"]:
            return jsonify(MSG_USERNAME_NULL)
        else:
            return None


@app.route('/api/info', methods=['POST'], strict_slashes=False)
def info():
    try:
        token = request.headers.get("token")
        if token == MSG_LOGIN_SUCCESS["data"]["token"]:
            return jsonify(MSG_LOGIN_SUCCESS)
        else:
            pass
    except:
        return jsonify(MSG_LOGIN_ERROR)


if __name__ == '__main__':
    app.run(debug=True)
