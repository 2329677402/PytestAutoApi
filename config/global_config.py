#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:37
@Author  : Poco Ray
@File    : global_config.py
@Software: PyCharm
@Desc    : Description
"""
import os
from config.path import get_root_dir, ensure_path_sep

# Tips: ⌘ + ⇧ + U（Command + Shift + U）: 在PyCharm中将选中的文本进行大小写切换

# Param
PROJECT_URL = "http://shop-xo.hctestedu.com"
USERNAME = "pocoray"
PASSWORD = "123456"
TYPE = "username"

# Path
ROOT_DIR = get_root_dir()
LOG_DIR = ensure_path_sep('\\logs')
LOG_PATH = ensure_path_sep('\\logs\\log.log')
SNAP_PATH = ensure_path_sep('\\snapshots')
REPORT_PATH = ensure_path_sep('\\report')
ALLURE_RESULTS = ensure_path_sep('\\report\\allure_results')
ALLURE_REPORTS = ensure_path_sep('\\report\\allure_reports')
EXCEL_PATH = ensure_path_sep('\\data\\Excel\\Api_Case_V7.xlsx')
SHEET_NAME = "Sheet1"
YAML_PATH = ensure_path_sep('\\data\\Yaml\\Api_Case_V3.yaml')

# Message
MSG_JSON_ERROR_01 = "❌数据解析失败，请检查dict_data数据格式是否正确"
MSG_JSON_ERROR_02 = "❌数据解析失败，请检查响应数据或actualResult字段中的JSONPath表达式是否正确"
MSG_RESULT_PASS = "✅单字段断言成功"
MSG_RESULT_FAIL = "❌单字段断言失败"
MSG_FULL_PASS = "✅全量字段断言成功"
MSG_FULL_FAIL = "❌全量字段断言失败"
MSG_JSONPATH_EXTRACT_ERROR = "❌变量提取失败，请检查响应数据或JSONPath表达式是否正确"
SQL_EXECUTE_ERROR = "❌SQL执行失败，请检查SQL语句是否正确"
SQL_RESULT_PASS = "✅数据库断言成功"
SQL_RESULT_FAIL = "❌数据库断言失败"
SQL_EXTRACT_ERROR = "❌SQL变量提取失败，请检查SQLExpectKey和SQLExpectValue字段值"

# DB
HOST = "shop-xo.hctestedu.com"
PORT = 3306
DB_USER = "api_test"
DB_PWD = "Aa9999!"
DB_NAME = "shopxo_hctested"

# Key
KEY_AES = "1234567812345678" # AES加密密钥，长度需为16的倍数
# 在线RSA公钥私钥生成: https://www.lddgo.net/encrypt/rsakey
RSA_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApZfoR1e5VxWM9QyhwnQR
6L9dGjLDbjyKZUjryyqMY8y9XcncG2qSL2Lpk9JpyWNwqG87SZX2jLUFTeS9ieiN
roB/SUgRv5au+dDtmbMFU91xaPQs/O1fhJeJeUO+19JEeS1wqqKp3suQnq9tWmcn
S1CQ5SvzVEGEufI3Z7L1F4tR2sqgy0tzQrZi7x5rrNvPlCIcMAfgtuk4gsZt+uSh
38YXZ6xjozLOEq5qPmx7acC06sxHgO2dzpTchFFUX+igzpazZLPxdjVJ9psoN0MY
tA5puC0Jn5/SswPtMfAUt+7clmBuTV8/PfCVDIw+VLMWeoWHMMg17y7n2hOxo+Sm
LwIDAQAB
-----END PUBLIC KEY-----'''
RSA_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
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
