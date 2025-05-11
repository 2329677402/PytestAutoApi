#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 01:39
@Author  : Poco Ray
@File    : AES.py
@Software: PyCharm
@Desc    : 常用的对称加密算法有AES、DES、3DES、RC4等，pip install pycryptodome
"""
import base64
from Crypto.Cipher import AES
from config.global_config import KEY_AES


class EncryptAES:

    def __init__(self, key: str = KEY_AES, length=AES.block_size, encrypt_mode=AES.MODE_ECB):
        """
        对称加密算法
        :param key: 密钥，长度需为16的倍数
        :param length: 密码长度，一般为16、24、32的倍数，默认16
        :param encrypt_mode: 加密模式，默认AES.MODE_ECB
        """
        self.key = key.encode('utf-8')
        self.length = length  # 密码长度，一般为16、24、32的倍数，默认16
        self.aes = AES.new(self.key, encrypt_mode)  # 设置加密模式

    def pad(self, text: str) -> str:
        """
        填充函数，使被加密的文本长度为block_size的整数倍
        :param text: 需要加密的文本
        :return: 填充后的文本，如果密码长度不足16位，则自动补到16位; 如果超过16位，则自动补到32位，以此类推...
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + chr(add) * add  # chr：内置函数，用于将整数转换为对应的Unicode字符
        return entext

    # AES 算法加密
    def encrypt(self, text: str) -> str:
        """
        :param text:
        :return:
        """
        # 1. 进行加密
        res = self.aes.encrypt(self.pad(text).encode('utf-8'))
        # 2. 进行base64编码
        encrypt_text = str(base64.b64encode(res), encoding='utf-8')
        return encrypt_text

    # AES 算法解密
    def decrypt(self, encrypt_text: str) -> str:
        """
        :param encrypt_text: 需要解密的加密文本
        :return:
        """
        # 1. 进行base64解码
        res = base64.b64decode(encrypt_text)
        # 2. 进行解密
        decrypt_text = self.aes.decrypt(res).decode('utf-8')
        # 3. 去除填充的字符
        count = ord(decrypt_text[-1])  # ord：内置函数，用于将Unicode字符转换为对应的整数
        return decrypt_text[:-count]

ENCRYPT_AES = EncryptAES()

if __name__ == '__main__':
    # 测试
    data = ENCRYPT_AES.encrypt(str('poco'))
    print(data)

    # 解密
    data = ENCRYPT_AES.decrypt(data)
    print(data)
