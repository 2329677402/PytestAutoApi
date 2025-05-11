#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 22:48
@Author  : Poco Ray
@File    : test_Excel_V1.py
@Software: PyCharm
@Desc    : Description
"""
import pytest
from common.api_key import ApiKey
from utils.data_tool.FileDataDriver import FileReader
from config.global_config import *


class TestExcelCase:
    ak = ApiKey()
    AllCaseData = FileReader.read_excel_to_dict()

    @pytest.mark.parametrize("case_data", AllCaseData)
    def test_case(self, case_data):
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
