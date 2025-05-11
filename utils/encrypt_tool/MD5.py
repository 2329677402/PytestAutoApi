#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 01:34
@Author  : Poco Ray
@File    : MD5.py
@Software: PyCharm
@Desc    : Description
"""


def md5_encrypt(text: str) -> str:
    """
    MD5加密, 不可逆：加密后的文本无法解密
    :param text: 需要加密的文本
    :return: 加密后的文本
    """
    import hashlib
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    # 测试
    content = '123456'
    print(f'原文: {content}')
    print("MD5加密: ", md5_encrypt(content))
