#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:31
@Author  : Poco Ray
@File    : api_key.py
@Software: PyCharm
@Desc    : 关键字驱动API请求的工具类，如HTTP请求方法、JSONPath变量提取、数据库断言等
"""
import json
import allure
import jsonpath
import pymysql
import requests
from typing import Union
from config.global_config import *


class ApiKey:
    """
    工具类，实现对应的一些关键字驱动操作
    """

    @allure.step("❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯发送GET请求")
    def get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    @allure.step("❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯发送POST请求")
    def post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)

    @staticmethod
    def get_value_by_jsonpath(response: Union[requests.Response, dict], expr: str) -> str:
        """
        通过JSONPath表达式获取响应数据中的文本内容
        :param response: 响应数据
        :param expr: JSONPath表达式
        :return:
        :Usage:
            ✅get_value_by_jsonpath(res, "$..msg")
            ✅get_value_by_jsonpath(res.json(), "$..msg")
            ❌get_value_by_jsonpath(res.text, "$..msg")
        """
        if isinstance(response, requests.Response):
            response = response.json()
        value_list = jsonpath.jsonpath(response, expr)
        return value_list[0] if len(value_list) > 0 else None

    @allure.step("❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯数据库断言")
    def sql_check(self, sql):
        """
        执行SQL语句并返回结果
        :param sql: SQL语句
        :return: SQL执行结果
        """
        connection = pymysql.connect(
            host=HOST,
            port=PORT,
            user=DB_USER,
            password=DB_PWD,
            db=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()  # 返回第一行数据, Tuple 类型
        print(result)
        cursor.close()
        connection.close()
        return result


if __name__ == '__main__':
    ak = ApiKey()
    data = {
        "url": "http://shop-xo.hctestedu.com?s=api/user/login",
        "params": {
            "application": "app",
            "application_client_type": "weixin"
        },
        "data": {
            "accounts": "pocoray",
            "pwd": "123456",
            "type": "username"
        }
    }

    res = ak.post(**data)
    print(type(res))
    print(type(res.text))
    print(type(res.json()))
    msg = ak.get_value_by_jsonpath(res, "$..msg")
    print(msg)
