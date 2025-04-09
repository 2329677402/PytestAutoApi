#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/2 19:37
@Author  : Poco Ray
@File    : config.py
@Software: PyCharm
@Desc    : Description
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from utils import baseUtil


class Config:

    root_dir = baseUtil.get_root_dir()
    log_path = os.path.join(root_dir, 'logs')
    snap_path = os.path.join(root_dir, 'snapshots')
    report_path = os.path.join(root_dir, 'report')
    allure_results = os.path.join(root_dir, 'report', 'allure_results')
    allure_reports = os.path.join(root_dir, 'report', 'allure_reports')
