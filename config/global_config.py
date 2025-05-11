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
EXCEL_PATH = ensure_path_sep('\\data\\Excel\\Api_Case_V5.xlsx')
SHEET_NAME = "Sheet1"
YAML_PATH = ensure_path_sep('\\data\\Yaml\\api_cases.yaml')

# Message
MSG_JSON_ERROR_01 = "❌数据解析失败，请检查dict_data数据格式是否正确"
MSG_JSON_ERROR_02 = "❌数据解析失败，请检查响应数据或actualResult字段中的JSONPath表达式是否正确"
MSG_RESULT_PASS = "✅通过"
MSG_RESULT_FAIL = "❌失败"
MSG_JSONPATH_EXTRACT_ERROR = "❌变量提取失败，请检查响应数据或JSONPath表达式是否正确"
SQL_EXECUTE_ERROR = "❌SQL执行失败，请检查SQL语句是否正确"
SQL_RESULT_PASS = "✅数据库断言通过"
SQL_RESULT_FAIL = "❌数据库断言失败"
SQL_EXTRACT_ERROR = "❌SQL变量提取失败，请检查SQLExpectKey和SQLExpectValue字段值"

# DB
HOST = "shop-xo.hctestedu.com"
PORT = 3306
DB_USER = "api_test"
DB_PWD = "Aa9999!"
DB_NAME = "shopxo_hctested"


if __name__ == '__main__':
    print(LOG_PATH)
    print(SNAP_PATH)
    print(REPORT_PATH)
    print(ALLURE_RESULTS)
    print(ALLURE_REPORTS)
    print(EXCEL_PATH)