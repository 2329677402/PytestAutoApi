#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 20:29
@Author  : Poco Ray
@File    : test_auth.py
@Software: PyCharm
@Desc    : Description
"""
import requests
from requests import utils


def test_cookies():
    session = requests.Session()
    res = session.get('https://httpbin.org/cookies')
    print(res.json() if res.status_code == 200 else 'status not 200')

    res = session.get('https://httpbin.org/cookies/set/qiucao/demo')
    print(res.json() if res.status_code == 200 else 'status not 200')

    res = session.get('https://httpbin.org/cookies/set/mytest/cookie')
    print(res.json() if res.status_code == 200 else 'status not 200')
    session.close()

    session2 = requests.Session()
    cookies = {'test1':'demo1'}
    # 设置cookie
    utils.cookiejar_from_dict(cookies, session2.cookies)
    # 添加cookie
    utils.add_dict_to_cookiejar(session2.cookies, {'test2': 'demo2'})
    res = session2.get('https://httpbin.org/cookies')
    # print(res.json())
    # 查询cookie
    print(utils.dict_from_cookiejar(session2.cookies))