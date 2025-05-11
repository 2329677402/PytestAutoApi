#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 02:33
@Author  : Poco Ray
@File    : RSA.py
@Software: PyCharm
@Desc    : 常用的非对称加密算法有RSA、DSA、ECC等，pip install pycryptodome
"""
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from config.global_config import RSA_PUBLIC_KEY, RSA_PRIVATE_KEY


class EncryptRSA:
    """
    RSA非对称加密算法
    """

    def __init__(self, public_key=RSA_PUBLIC_KEY, private_key=RSA_PRIVATE_KEY):
        """
        在线RSA公钥私钥生成: https://www.lddgo.net/encrypt/rsakey
        :param public_key: 公钥
        :param private_key: 私钥
        """
        self.public_key = RSA.importKey(public_key)  # 加载公钥
        self.private_key = RSA.importKey(private_key)  # 加载私钥

    def encrypt(self, text: str) -> str:
        """
        RSA 加密, 返回加密结果
        :param text:
        :return:
        """
        # 1. 创建一个加密器对象 cipher，使用self.public_key 作为公钥
        cipher = PKCS1_v1_5.new(self.public_key)
        # 2. 加密，将text.encode('utf-8') 转为 b64 编码
        rsa_text = base64.b64encode(cipher.encrypt(text.encode('utf-8')))
        # 3. 将加密后的文本解码为字符串
        text = rsa_text.decode('utf-8')
        return text

    def decrypt(self, encrypt_text: str) -> str:
        """
        RSA 解密, 返回解密结果
        :param encrypt_text:
        :return:
        """
        # 1. 创建一个解密器对象 cipher，使用self.private_key 作为私钥
        cipher = PKCS1_v1_5.new(self.private_key)
        # 2. 解密，将text.encode('utf-8') 转为 b64 编码
        rsa_text = cipher.decrypt(base64.b64decode(encrypt_text.encode('utf-8')), 0)
        # 3. 将解密后的文本解码为字符串
        decrypt_text = rsa_text.decode('utf-8')
        return decrypt_text

ENCRYPT_RSA = EncryptRSA()

if __name__ == '__main__':
    # 测试
    # 1. 加密处理
    info = ENCRYPT_RSA.encrypt('poco')
    print("加密结果: ", info)
    # 2. 解密处理
    decrypt_info = ENCRYPT_RSA.decrypt(info)
    print("解密结果: ", decrypt_info)
