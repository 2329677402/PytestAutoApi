#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 22:48
@Author  : Poco Ray
@File    : test_Excel_V1.py
@Software: PyCharm
@Desc    : Description
"""
import json
import allure
import pytest
from string import Template
from common.api_key import ApiKey
from utils.data_tool.FileDataDriver import FileReader
from config.global_config import *


class TestExcelCase:
    ak = ApiKey()
    AllCaseData = FileReader.read_excel_to_dict()

    # 存储所有提取的变量（JSONPath OR Regex）
    all_extract = {}

    @staticmethod
    def __dynamic_title(case_data):
        """
        动态生成Allure标题
        :param case_data: 用例数据
        :return: Allure标题
        """
        if case_data["CaseName"] is not None:
            caseName = f"ID({case_data['ID']}) - {case_data['CaseName']}"
            allure.dynamic.title(caseName)
        if case_data["StoryName"] is not None:
            allure.dynamic.story(case_data["StoryName"])
        if case_data["FeatureName"] is not None:
            allure.dynamic.feature(case_data["FeatureName"])
        if case_data["Description"] is not None:
            allure.dynamic.description(case_data["Description"])
        if case_data["Severity"] is not None:
            allure.dynamic.severity(case_data["Severity"])

    def __json_extract(self, res, case_data):
        """
        提取JSON响应数据
        :param res: 请求成功后的响应数据
        :param case_data: Excel中的用例数据
        :return: 提取的值
        """
        try:
            if case_data["JSONKey"] and case_data["JSONValue"]:
                JSONVarList: list = eval(case_data["JSONKey"])
                JSONExprList: list = eval(case_data["JSONValue"])

                for i in range(len(JSONVarList)):
                    key = JSONVarList[i]
                    expr = JSONExprList[i]

                    # 根据expr获取值
                    value = self.ak.get_value_by_jsonpath(res, expr)
                    # 将提取的值存储到all_extract字典中
                    self.all_extract[key] = value
                print("当前接口所提取的变量：", self.all_extract)
        except:
            print(MSG_JSONPATH_EXTRACT_ERROR)

    def __sql_extract(self, case_data):
        """
        提取SQL响应数据
        :param case_data: Excel中的用例数据
        :return: 提取的值
        """
        try:
            if case_data["SQLExpectKey"] and case_data["SQLExpectValue"]:
                SQLVarList: list = eval(case_data["SQLExpectKey"])
                SQLValueTuple: tuple = self.ak.sql_check(case_data["SQLExpectValue"])

                for i in range(len(SQLVarList)):
                    key = SQLVarList[i]
                    value = SQLValueTuple[i]

                    # 将提取的值存储到all_extract字典中
                    self.all_extract[key] = value
                print("当前接口所提取的变量：", self.all_extract)
        except:
            print(SQL_EXTRACT_ERROR)

    @pytest.mark.parametrize("case_data", AllCaseData)
    def test_case(self, case_data):
        # 动态生成Allure报告数据
        self.__dynamic_title(case_data)

        # 局部变量
        msg = None
        sql_count = None  # SQL断言差集计数

        # Excel Result字段（检查结果）写入值
        value = None
        row = case_data["ID"]
        column = 11

        # 1. 读取Excel数据
        try:
            url = case_data["URL"] + case_data["Path"]
            # 将all_extract中的变量应用到当前接口的URL的变量中, 通过 ${var} 来引用, 如: http://www.xxx.com?token=${token}&s=
            new_url = Template(url).substitute(self.all_extract)

            # 其它参数为空时的处理, 避免参数未填写时, 传入None, 导致eval方法解析失败
            params = eval(case_data["Params"]) if isinstance(case_data["Params"], str) else None
            headers = eval(case_data["Headers"]) if isinstance(case_data["Headers"], str) else None
            # 处理加密字段数据, 在需要加密的字段前加入@标识, 若没有@标识，则返回原数据
            data = FileReader.data_encrypt_by_aes(eval(case_data["Data"])) if isinstance(case_data["Data"],
                                                                                         str) else None

            dict_data = {
                "url": new_url,
                "params": params,
                "data": data,  # 传入加密数据或原数据
                "headers": headers,
            }
            # 增加入参方式为json的处理, 若data为dict类型, 则入参方式支持form-data，而不支持json
            if case_data["Type"] == "json":
                dict_data["data"] = json.dumps(dict_data["data"])

        except Exception:
            print(MSG_JSON_ERROR_01)
            FileReader.write_excel_from_data(row=row, column=column, value=MSG_JSON_ERROR_01)
        else:
            res = getattr(self.ak, case_data["Method"])(**dict_data)

            # 2. 响应数据断言处理
            try:
                msg = self.ak.get_value_by_jsonpath(res, case_data["ActualResult"])
            except Exception:
                print(MSG_JSON_ERROR_02)
                FileReader.write_excel_from_data(row=row, column=column, value=MSG_JSON_ERROR_02)
            else:
                # 2.1 单字段断言处理
                if case_data["ExpectResult"] == msg:
                    value = MSG_RESULT_PASS
                    print("✅测试通过")

                    # 3. 接口请求成功后，提取响应数据变量
                    self.__json_extract(res, case_data)
                else:
                    value = MSG_RESULT_FAIL
                    print("❌测试失败")

                # 2.2 全量字段断言处理
                if case_data["ResponseExpect"]:
                    try:
                        json1 = eval(case_data["ResponseExpect"])
                        condition = eval(case_data["ResponseExclude"])
                        DD_Result = self.ak.json_deepdiff(json1, res.json(), **condition)

                        if DD_Result == {}:
                            value = MSG_FULL_PASS
                        else:
                            value = MSG_FULL_FAIL
                    except:
                        print("⚠️不需要进行全量字段断言或数据解析错误")
                FileReader.write_excel_from_data(row=row, column=column, value=value)
            finally:
                assert msg == case_data["ExpectResult"]

            # 4. 数据库断言处理
            if case_data["SQLKey"] and case_data["SQLValue"] and case_data["SQLExpectResult"]:
                try:
                    sqlValue = case_data["SQLValue"]  # SQL 语句
                    all_sql_value = self.ak.sql_check(sqlValue)
                    all_sql_value = set(all_sql_value)  # SQL 实际结果

                    sqlExpectValue: set = eval(case_data["SQLExpectResult"])  # SQL 期望结果
                except:
                    value = SQL_EXECUTE_ERROR
                else:
                    # 求出all_sql_value和sqlExpectValue的交叉差集. 若差集为空，则表示相等
                    sql_count = len(sqlExpectValue.symmetric_difference(all_sql_value))
                    if sql_count == 0:
                        value = SQL_RESULT_PASS
                    else:
                        value = SQL_RESULT_FAIL
                finally:
                    FileReader.write_excel_from_data(row=row, column=column, value=value)
                    assert sql_count == 0, f"❌SQL断言失败，差集数量为：{sql_count}，请检查SQL语句或期望结果是否正确"
            else:
                print("⚠️没有SQL语句需要校验")
                # value = "⚠️没有SQL语句需要校验"
                # FileReader.write_excel_from_data(row=row, column=column, value=value)

            # 5. 提取SQL响应数据变量
            if case_data["SQLExpectKey"] and case_data["SQLExpectValue"]:
                try:
                    print("\n❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯❯提取SQL变量")
                    self.__sql_extract(case_data)
                except:
                    value = SQL_EXECUTE_ERROR
                    FileReader.write_excel_from_data(row=row, column=column, value=value)
