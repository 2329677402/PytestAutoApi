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
from deepdiff import DeepDiff


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

    @allure.step("❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯提取响应数据变量")
    def get_value_by_jsonpath(self, response: Union[requests.Response, dict, str], expr: str) -> str:
        """
        通过JSONPath表达式获取响应数据中的文本内容
        :param response: 响应数据
        :param expr: JSONPath表达式
        :return:
        :Usage:
            ✅get_value_by_jsonpath(res, "$..msg")
            ✅get_value_by_jsonpath(res.json(), "$..msg")
            ✅get_value_by_jsonpath(res.text, "$..msg")
        """
        if isinstance(response, requests.Response):
            response = response.json()
        elif isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                raise ValueError(f"无法解析 JSON 字符串: {e}")
        value_list = jsonpath.jsonpath(response, expr)
        return value_list[0] if len(value_list) > 0 else None

    @allure.step("❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯数据库断言或提取")
    def sql_check(self, sql: str) -> tuple:
        """
        执行SQL语句并返回结果
        :param sql: SQL语句
        :return: SQL执行结果
        :Usage:
            ak = ApiKey()
            res = ak.sql_check("SELECT username FROM table WHERE username='pocoray'")
            print(res) # ('pocoray',)
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
        result = cursor.fetchall()[0]  # 返回第一行数据, Tuple 类型
        cursor.close()
        connection.close()
        return result

    @allure.step("❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯全量数据JSON校验")
    def json_deepdiff(self, json1, json2, **kwargs):
        """
        对比两个JSON数据的差异
        :param json1:
        :param json2:
        :param kwargs: 条件字段, 如: ignore_order(忽略顺序), exclude_paths(排除路径), ignore_string_case(忽略大小写),
        :return: 如果没有差异, 返回空集合{}; 否则返回差异的内容
        """
        result = DeepDiff(json1, json2, **kwargs)
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
    msg = ak.get_value_by_jsonpath(res.text, "$..msg")
    print(msg)
    sql_value = "Select username From sxo_user Where username='pocoray';"
    res = ak.sql_check(sql_value)
    print(res)
    print(set(res))
