#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:38
@Author  : Poco Ray
@File    : path.py
@Software: PyCharm
@Desc    : Description
"""
import os
from typing import Text


def get_root_dir() -> str:
    """
    Get the project root path.

    :return: Project root path.
    :Usage:
        os.path.join(root_path(), "report")
    """
    rootDir = os.path.dirname(os.path.dirname(__file__))
    return rootDir


def ensure_path_sep(path: Text) -> Text:
    """
    Ensure that the path separator is consistent with the current operating system.

    :param path: Path string.
    :return: Path string with consistent separator.
    :Usage:
        ensure_path_sep("/report/html")
        ensure_path_sep("\\report\\html")
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return get_root_dir() + path


def get_base64(file_path: str) -> str:
    """
    获取图片的Base64编码
    :param file_path: 图片文件路径
    :return: 图片的Base64编码
    """
    import base64

    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')


# 测试
if __name__ == '__main__':
    print(get_root_dir())
    print(ensure_path_sep("/report/html"))
    print(ensure_path_sep("\\report\\html"))
