#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/11 17:14
@Author  : Poco Ray
@File    : test_Yaml_V3.py
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
    AllCaseData = FileReader.read_yaml_to_dict()

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
            allure.dynamic.title(case_data["CaseName"])
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
                JSONVarList: list = case_data["JSONKey"]
                JSONExprList: list = case_data["JSONValue"]

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

    @pytest.mark.parametrize("case_data", AllCaseData)
    def test_case(self, case_data):
        # 动态生成Allure报告数据
        self.__dynamic_title(case_data)

        # 局部变量
        msg = None

        # Yaml Result字段（检查结果）写入值
        index = case_data["ID"]

        # 1. 读取Yaml数据
        try:
            url = case_data["URL"] + case_data["Path"]
            # 将前一个接口提取的所有变量应用到当前接口的URL的变量中
            new_url = Template(url).substitute(self.all_extract)
            # 将Params参数中的 '{{var}}' 变量替换为对应值
            params = FileReader.replace_variable_in_yaml(case_data["Params"], self.all_extract)
            dict_data = {
                "url": new_url,
                "params": params,
                "data": case_data["Data"],  # 转换为dict类型，入参方式支持form-data，但不支持json
                "headers": case_data["Headers"]
            }
            if case_data["Type"] == "json":
                dict_data["data"] = json.dumps(dict_data["data"])

        except Exception:
            # 将错误信息写入到Yaml文件的Result字段
            value = MSG_JSON_ERROR_01
            case_data["Result"] = value
            self.AllCaseData[index] = case_data
            FileReader.write_data_to_yaml(self.AllCaseData)
        else:
            res = getattr(self.ak, case_data["Method"])(**dict_data)

            # 2. 响应数据断言处理
            try:
                msg = self.ak.get_value_by_jsonpath(res, case_data["ActualResult"])
            except Exception:
                value = MSG_JSON_ERROR_02
                case_data["Result"] = value
                self.AllCaseData[index] = case_data
                FileReader.write_data_to_yaml(self.AllCaseData)
            else:
                if case_data["ExpectResult"] == msg:
                    value = MSG_RESULT_PASS
                    print("✅测试通过")

                    # 接口请求成功后，提取变量
                    self.__json_extract(res, case_data)
                else:
                    value = MSG_RESULT_FAIL
                    print("❌测试失败")

                # 将错误信息写入到Yaml文件的Result字段
                case_data["Result"] = value
                self.AllCaseData[index] = case_data
                FileReader.write_data_to_yaml(self.AllCaseData)
            finally:
                assert msg == case_data["ExpectResult"]
