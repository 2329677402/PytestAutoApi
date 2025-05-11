#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 22:48
@Author  : Poco Ray
@File    : test_Excel_V1.py
@Software: PyCharm
@Desc    : Description
"""
import allure
import pytest
from common.api_key import ApiKey
from utils.data_tool.FileDataDriver import FileReader
from config.global_config import *


class TestExcelCase:
    ak = ApiKey()
    AllCaseData = FileReader.read_excel_to_dict()

    @staticmethod
    def __dynamic_title(case_data):
        """
        动态生成Allure标题
        :param case_data: 用例数据
        :return: Allure标题
        """
        if case_data["CaseName"] is not None:
            allure.dynamic.title(case_data["CaseName"])
        if case_data["StoryName"] is not None:
            allure.dynamic.story(case_data["StoryName"])
        if case_data["FeatureName"] is not None:
            allure.dynamic.feature(case_data["FeatureName"])
        if case_data["Description"] is not None:
            allure.dynamic.description(case_data["Description"])
        if case_data["Severity"] is not None:
            allure.dynamic.severity(case_data["Severity"])

    @pytest.mark.parametrize("case_data", AllCaseData)
    def test_case(self, case_data):
        # 动态生成Allure报告数据
        self.__dynamic_title(case_data)

        # 局部变量
        msg = None
        # Excel Result字段写入值
        row = case_data["ID"]
        column = 11

        # 1. 读取Excel数据
        try:
            dict_data = {
                "url": case_data["URL"] + case_data["Path"],
                "params": eval(case_data["Params"]),
                "data": eval(case_data["Data"]),
                "headers": eval(case_data["Headers"]),
            }
        except Exception:
            print(MSG_JSON_ERROR_01)
            FileReader.write_excel_from_data(row=row, column=column, value=MSG_JSON_ERROR_01)
        else:
            res = getattr(self.ak, case_data["Method"])(**dict_data)

            # 2. 数据断言处理
            try:
                msg = self.ak.get_value_by_jsonpath(res, case_data["ActualResult"])
            except Exception:
                print(MSG_JSON_ERROR_02)
                FileReader.write_excel_from_data(row=row, column=column, value=MSG_JSON_ERROR_02)
            else:
                if case_data["ExpectResult"] == msg:
                    value = MSG_RESULT_PASS
                    print("✅测试通过")
                else:
                    value = MSG_RESULT_FAIL
                    print("❌测试失败")
                FileReader.write_excel_from_data(row=row, column=column, value=value)
            finally:
                assert case_data["ExpectResult"] == msg
