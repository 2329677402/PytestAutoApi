#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:38
@Author  : Poco Ray
@File    : baseUtil.py
@Software: PyCharm
@Desc    : Description
"""
import os.path


def get_root_dir():
    rootDir = os.path.dirname(os.path.dirname(__file__))
    return rootDir


def get_base64(file_path: str) -> str:
    """
    获取图片的Base64编码
    :param file_path: 图片文件路径
    :return: 图片的Base64编码
    """
    import base64

    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')
