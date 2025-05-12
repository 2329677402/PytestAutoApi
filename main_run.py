#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 17:23
@Author  : Poco Ray
@File    : main_run.py
@Software: PyCharm
@Desc    : Description
"""
import os
import shutil
import pytest
from config.global_config import *

if __name__ == '__main__':
    if not os.path.exists(REPORT_PATH):
        os.makedirs(REPORT_PATH)

    # 运行pytest并生成报告
    pytest.main(["-v","./tests/test_Excel_Latest.py", f'--alluredir={ALLURE_RESULTS}', '--clean-alluredir'])
    # 在测试开始运行，执行了--clean-alluredir的命令行参数后，再将environment.properties文件复制到allure-results目录下
    env_path = os.path.join(ALLURE_RESULTS, 'environment.properties')
    shutil.copy("environment.properties", env_path)
    os.system(f"allure generate {ALLURE_RESULTS} -o {ALLURE_REPORTS} --clean")
