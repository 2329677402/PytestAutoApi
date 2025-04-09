#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:31
@Author  : Poco Ray
@File    : githubAPI.py
@Software: PyCharm
@Desc    : Description
"""
import json

import requests


class GithubAPI:
    def __init__(self, base_url, token):
        self.session = requests.Session()
        self.base_url = base_url
        self.session.headers = dict()
        self.session.headers['Authorization'] = f'Bearer {token}'
        self.session.headers['accept'] = 'application/vnd.github+json'

    def get_repo(self, owner, repo):
        end_point = self.base_url + f'/repos/{owner}/{repo}'
        res = self.session.get(end_point)
        print(res.json())
        return res

    def create_repo(self, body):
        end_point = self.base_url + '/user/repos'
        data = json.dumps(body)
        res = self.session.post(end_point, data=data)
        print(res.json())
        return res

    def update_repo(self, body, owner, repo):
        end_point = self.base_url + f'/repos/{owner}/{repo}'
        data = json.dumps(body)
        res = self.session.patch(end_point, data=data)
        print(res.json())
        return res

    def delete_repo(self, owner, repo):
        end_point = self.base_url + f'/repos/{owner}/{repo}'
        res = self.session.delete(end_point)
        return res

    def close_session(self):
        self.session.close()

