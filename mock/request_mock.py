#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/12 01:22
@Author  : Poco Ray
@File    : request_mock.py
@Software: PyCharm
@Desc    : Description
"""
import requests


url = "http://127.0.0.1:5000/api/login"
data = {"USERNAME": "poco", "password": "123456"}

res = requests.post(url=url, json=data)
print(res.json())
