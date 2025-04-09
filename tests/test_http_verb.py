#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:30
@Author  : Poco Ray
@File    : test_http_verb.py
@Software: PyCharm
@Desc    : Description
"""
import json

import requests


class TestVerb:
    @staticmethod
    def setup_class():
        rule = {
            "priority": 8,
            "request": {
                "method": "GET",
                "urlPattern": "/repos/.*/.*"
            },
            "response": {
                "jsonBody": {"full_name": "通配repo"},
                "headers": {
                    "Content-Type": "application/json; charset=utf-8"
                },
                "status": 200
            }
        }

        requests.post('http://localhost:8088/__admin/reset')
        requests.post('http://localhost:8088/__admin/mappings', data=json.dumps(rule))

    def test_get_repo(self, github):
        # end_point = 'https://api.github.com/repos/appium/appium'
        # res = requests.get(end_point)

        owner = 'appium'
        repo = 'appium'
        res = github.get_repo(owner, repo)
        assert res.status_code == 200

    def test_create_repo(self, github):
        body = dict()
        body['name'] = 'qiucaoTest'
        body['auto_init'] = True
        res = github.create_repo(body)
        assert res.status_code == 201

    def test_update_repo(self, github):
        body = dict()
        body['description'] = '这是城下秋草API课程演示'
        body['has_projects'] = False
        body['has_wiki'] = False
        owner = '2329677402'
        repo = '2329677402'
        res = github.update_repo(body, owner, repo)
        assert res.status_code == 200

    def test_delete_repo(self, github):
        owner = '2329677402'
        repo = 'qiucaoTest'
        res = github.delete_repo(owner, repo)
        assert res.status_code == 204

    def test_delete_repo2(self, github):
        owner = '2329677402'
        repo = '2329677402 '
        res = github.delete_repo(owner, repo)
        assert res.status_code == 204
