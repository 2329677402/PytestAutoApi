#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 16:07
@Author  : Poco Ray
@File    : test_DS.py
@Software: PyCharm
@Desc    : Description
"""
import allure

from common.api_key import ApiKey


@allure.title("登录测试用例")
def test_01():
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
        },
        "headers": {
            "Content-Type": "multipart/form-data"
        }
    }

    res = ak.post(**data)
    msg = ak.get_value_by_jsonpath(res, "$..msg")
    print(msg)


@allure.title("加入购物车测试用例")
def test_02(token_fixture):
    ak, token = token_fixture
    print("当前token：", token)

    with allure.step('01_登录测试用例'):
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
        msg = ak.get_value_by_jsonpath(res, "$..msg")
        token = ak.get_value_by_jsonpath(res, "$..token")

    with allure.step('02_加入购物车'):
        data = {
            "url": "http://shop-xo.hctestedu.com?s=api/cart/save",
            "params": {
                "application": "app",
                "application_client_type": "weixin",
                "token": token
            },
            "data": {
                "goods_id": "1",
                "sepc": [
                    {
                        "type": "尺寸",
                        "value": "M"
                    }
                ],
                "stock": "10"
            }
        }
        res = ak.post(**data)
        msg = ak.get_value_by_jsonpath(res, "$..msg")
        assert "加入成功" in msg
