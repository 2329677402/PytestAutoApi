#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 02:33
@Author  : Poco Ray
@File    : 非对称加密.py
@Software: PyCharm
@Desc    : 常用的非对称加密算法有RSA、DSA、ECC等，pip install pycryptodome
"""
import base64

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class RSAEncrypt:
    """
    RSA非对称加密算法
    """

    def __init__(self, public_key: str, private_key: str):
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


if __name__ == '__main__':
    # 测试
    # 1. 实例化对象
    pub_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApZfoR1e5VxWM9QyhwnQR
6L9dGjLDbjyKZUjryyqMY8y9XcncG2qSL2Lpk9JpyWNwqG87SZX2jLUFTeS9ieiN
roB/SUgRv5au+dDtmbMFU91xaPQs/O1fhJeJeUO+19JEeS1wqqKp3suQnq9tWmcn
S1CQ5SvzVEGEufI3Z7L1F4tR2sqgy0tzQrZi7x5rrNvPlCIcMAfgtuk4gsZt+uSh
38YXZ6xjozLOEq5qPmx7acC06sxHgO2dzpTchFFUX+igzpazZLPxdjVJ9psoN0MY
tA5puC0Jn5/SswPtMfAUt+7clmBuTV8/PfCVDIw+VLMWeoWHMMg17y7n2hOxo+Sm
LwIDAQAB
-----END PUBLIC KEY-----'''
    pri_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCll+hHV7lXFYz1
DKHCdBHov10aMsNuPIplSOvLKoxjzL1dydwbapIvYumT0mnJY3CobztJlfaMtQVN
5L2J6I2ugH9JSBG/lq750O2ZswVT3XFo9Cz87V+El4l5Q77X0kR5LXCqoqney5Ce
r21aZydLUJDlK/NUQYS58jdnsvUXi1HayqDLS3NCtmLvHmus28+UIhwwB+C26TiC
xm365KHfxhdnrGOjMs4Srmo+bHtpwLTqzEeA7Z3OlNyEUVRf6KDOlrNks/F2NUn2
myg3Qxi0Dmm4LQmfn9KzA+0x8BS37tyWYG5NXz898JUMjD5UsxZ6hYcwyDXvLufa
E7Gj5KYvAgMBAAECggEAQ3nX86JCasLkUkJYc9U6Kv43YOKIkhXnSwhg1MO8uzoF
e/8ySpWthdOnXE3kP2Te1jOlFAIgmgt1Yt0vgs+ZVB8WPvU4DjrHiBJjjzrMk/Tr
Lpo47sOHJY9ePGSnkmgi8MHcZBuuXpPSlWbkh277KwxkTo4PNCkSfXa+runUR0gb
QgcSUcMe1DDC0YirCFMPa1+IwnQBsynnQ1/BX2Pe7E7KEBLmO1tj1OZiJTtQ01Uv
PRIF7eNBEOFG6ENJbssJQsUfzJ5aeOGwYRL5FiqzuXlcHuWI9vjqmCPi3G1uS+oA
K9mB7P3pjHqedPxzEFoBceoEf3HRyVW2gMClRXNaSQKBgQDwN5rQXvqj/0wfjzA0
8w8gqY/pmVoCUWjzdqieG8VphMrqRhTKY4NaaS8EoJOY/Y6FUGsIXtB/I6G/E+3t
7D+pfmgaJVEqKFEaV9wWJPVsmJvgosFRHy++p1TMPhiX3yjYFv5BGdyEjQNm9Wm5
3eVJETkp07S7qEAhYcBLUQBzgwKBgQCweSXmD5CUwXL1Mj9dgv6GRD20Ed1FaIsv
MCafySNvYOrz7nqUBZY/cXRc3jlNV1OlXgg4KjjQmKfnT18ZUf+RRQ7uDL2KPN/P
7FMDX94W+QNNBgdTV9J3QL09WAi8F+Vapn+UZF+IdxTleA1q7aTEBvVbMVJQJ1xK
MJc2X2LG5QKBgQDmZN6GZeJNMspHJqWc01a6BAd0jFGpEX3wrOkyo/4mo2efZNIB
/4n3SBUBgiWuQdrVAHl30MB2gK1cv/efD81LemLMWOhM39hRxNzhHFeL7Z7ryA5U
CO5ZFNKfBhu+Zhodj4gS1oQLWdhegpkB3NJRz0QdWuDob4n6um+djTY6kwKBgHTo
TQsT1Jw3a4i0OPYiCau5GYdpLkUE9O/V3kCMZ0Up13yxx9K3wMlWx9eeACgUaf1r
RdavYeQOvWynUEDd6Yi7TyC0n/wsR7jevj/GCsL9RAqKq9+ylmMaKEOzRlYVHoPn
OS19MSyeduFtnrXvqO+UDIbVLcqbyK/9cK88kZthAoGAFUPSChCBQ2QIv6b9JRFD
+sUpM432CumM63fp3pem7sboRJrSCEODWscFL8St2exGi/yqEIknePWm0aKNR8XC
Zz4WOAQXuL0d4UUXLqBoK0yYyiBRwTPZif0OG/F17kgFFeUVU2RKT79nqvW5bLd7
hoW99vwE97mehYzZ9yVoAKg=
-----END RSA PRIVATE KEY-----'''
    rsa = RSAEncrypt(public_key=pub_key, private_key=pri_key)
    # 2. 加密处理
    info = rsa.encrypt('poco')
    print("加密结果: ", info)
    # 3. 解密处理
    decrypt_info = rsa.decrypt(info)
    print("解密结果: ", decrypt_info)
