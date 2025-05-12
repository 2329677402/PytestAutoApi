#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:23
@Author  : Poco Ray
@File    : conftest.py
@Software: PyCharm
@Desc    : Description
"""
import json
import yaml
import jsonpath
import requests
from string import Template
import pytest
import logging
from common.api_key import ApiKey
from config.global_config import *

variables = dict()


# @pytest.fixture(scope='session')
# def token_fixture():
#     ak = ApiKey()
#     data = {
#         "url": f"{PROJECT_URL}?s=api/user/login",
#         "params": {
#             "application": "app",
#             "application_client_type": "weixin"
#         },
#         "data": {
#             "accounts": USERNAME,
#             "pwd": PASSWORD,
#             "type": TYPE
#         }
#     }
#     res = ak.post(**data)
#     token = ak.get_value_by_jsonpath(res, "$..token")
#     return ak, token


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    pytest钩子函数，获取测试用例的执行结果
    :param item: 测试用例对象
    :param call: 测试用例执行结果
    :return:
    """
    out = yield
    res = out.get_result()
    if res.when == "call":
        logging.info(f"🆔用例编号: {res.nodeid}")
        if res.outcome == "passed":
            logging.info(f"✅测试结果: {res.outcome}")
        else:
            logging.info(f"❌测试结果: {res.outcome}")
        logging.info(f"🐞故障标识: {res.longrepr}")
        logging.info(f"⚠️异常信息: {call.excinfo}")
        logging.info(f"⏱️用例耗时: {res.duration:.2f}秒")
        logging.info("❯" * 100)


@pytest.fixture(autouse=True, scope="session")
def disable_proxy():
    # 备份当前的代理设置
    original_proxies = {key: os.environ.get(key) for key in ['http_proxy', 'https_proxy', 'all_proxy']}
    # 清除代理设置
    for key in original_proxies:
        os.environ.pop(key, None)
    yield
    # 恢复原始的代理设置
    for key, value in original_proxies.items():
        if value is not None:
            os.environ[key] = value

# def pytest_collect_file(parent, file_path):
#     if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
#         return YamlFile.from_parent(parent, path=file_path)
#
#
# class YamlFile(pytest.File):
#     def collect(self):
#         global variables
#         print()
#         raw = self.fspath.open(encoding="utf-8").read()
#         print('yml原始文件'.center(80, '-'), '\r\n', raw)
#         suite = yaml.safe_load(raw)
#
#         for case in suite:
#             if 'config' in case:
#                 variables = case['config'].get('variables')
#                 print('测试变量清单'.center(80, '-'), '\r\n', variables)
#
#             if 'test' in case:
#                 name = case['test'].get('name')
#                 spec = case['test']
#                 yield YamlItem.from_parent(self, name=name, spec=spec)
#
#
# class YamlItem(pytest.Item):
#     def __init__(self, *, spec, **kwargs):
#         super().__init__(**kwargs)
#         self.spec = spec
#         self.request = spec.get('request')
#         self.check = spec.get('check')
#         self.name = spec.get('name')
#         self.s = requests.session()
#         self.s.headers = variables.get('headers')
#
#     def runtest(self):
#         global variables
#         print()
#         test_case = Template(json.dumps(self.spec)).safe_substitute(variables)
#         test_case = json.loads(test_case)
#         print('测试用例'.center(80, '-'), '\r\n', test_case)
#         request_params = test_case.get('request')
#         res = self.s.request(**request_params)
#         print('响应内容'.center(80, '-'), '\r\n', res.text)
#
#         if test_case.get('extract'):
#             for key, value in test_case.get('extract').items():
#                 variables[key] = jsonpath.jsonpath(res.json(), value)[0]
#                 print(f'提取了变量{key}, 取值:{variables[key]}')
#
#         self.check_result(res, test_case.get('check'))
#
#     def check_result(self, res, check):
#         print('验证内容'.center(80, '-'), '\r\n', check)
#         for point in check:
#             for key, value in point.items():
#                 if 'status_code' == key:
#                     expect = value
#                     actual = res.status_code
#                     assert expect == actual
