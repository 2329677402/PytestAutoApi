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
from string import Template
import jsonpath
import pytest
import requests
import yaml
from github.githubAPI import GithubAPI

variables = dict()

@pytest.fixture(scope='session')
def github():
    base_url = 'https://api.github.com'
    # base_url = 'http://localhost:8088'
    token = 'xxx'
    github_api = GithubAPI(base_url, token)
    yield github_api
    github_api.close_session()



def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        return YamlFile.from_parent(parent, path=file_path)


class YamlFile(pytest.File):
    def collect(self):
        global variables
        print()
        raw = self.fspath.open(encoding="utf-8").read()
        print('yml原始文件'.center(80,  '-'), '\r\n', raw)
        suite = yaml.safe_load(raw)

        for case in suite:
            if 'config' in case:
                variables = case['config'].get('variables')
                print('测试变量清单'.center(80, '-'), '\r\n', variables)

            if 'test' in case:
                name = case['test'].get('name')
                spec = case['test']
                yield YamlItem.from_parent(self, name=name, spec=spec)


class YamlItem(pytest.Item):
    def __init__(self, *, spec, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        # self.request = spec.get('request')
        # self.check = spec.get('check')
        self.name = spec.get('name')
        self.s = requests.session()
        self.s.headers = variables.get('headers')

    def runtest(self):
        global variables
        print()
        test_case = Template(json.dumps(self.spec)).safe_substitute(variables)
        test_case = json.loads(test_case)
        print('测试用例'.center(80, '-'), '\r\n',test_case)
        request_params = test_case.get('request')
        res = self.s.request(**request_params)
        print('响应内容'.center(80, '-'), '\r\n', res.text)

        if test_case.get('extract'):
            for key, value in test_case.get('extract').items():
                variables[key] = jsonpath.jsonpath(res.json(), value)[0]
                print(f'提取了变量{key}, 取值:{variables[key]}')

        self.check_result(res, test_case.get('check'))

    def check_result(self, res, check):
        print('验证内容'.center(80, '-'), '\r\n', check)
        for point in check:
            for key, value in point.items():
                if 'status_code' == key:
                    expect = value
                    actual = res.status_code
                    assert expect == actual
