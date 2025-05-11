#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 21:29
@Author  : Poco Ray
@File    : FileDataDriver.py
@Software: PyCharm
@Desc    : Description
"""
import openpyxl
from config.global_config import EXCEL_PATH, SHEET_NAME, YAML_PATH


class FileReader:

    @staticmethod
    def read_excel_to_dict(file_path: str = EXCEL_PATH, sheet_name: str = SHEET_NAME) -> list[dict]:
        """
        读取Excel文件并转换为字典列表
        :param file_path: Excel文件路径
        :param sheet_name: 工作表名称
        :return: 转换后的字典列表，[{}, {}, ...]
        """
        # 1. 加载Excel文件
        try:
            workbook = openpyxl.load_workbook(file_path)
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

        # 2. 获取工作表
        if sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
        else:
            worksheet = workbook.create_sheet(sheet_name)

        # 3. 读取数据
        data_for_list = []
        headers = [cell.value for cell in worksheet[2]]
        for row in worksheet.iter_rows(min_row=3, values_only=True):
            data_for_list.append(dict(zip(headers, row)))
        workbook.close()
        return data_for_list

    @staticmethod
    def write_excel_from_data(
            file_path: str = EXCEL_PATH, sheet_name: str = SHEET_NAME,
            row=None, column=None, value=None):
        """
        将数据写入Excel文件
        :param file_path: Excel文件路径
        :param sheet_name: 工作表名称
        :param row: 行号
        :param column: 列号
        :param value: 写入的值
        """
        # 1. 加载Excel文件
        try:
            workbook = openpyxl.load_workbook(file_path)
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

        # 2. 获取工作表
        if sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
        else:
            worksheet = workbook.create_sheet(sheet_name)

        # 3. 写入数据
        worksheet.cell(row=row, column=column, value=value)
        workbook.save(file_path)
        workbook.close()


if __name__ == '__main__':
    data = FileReader.read_excel_to_dict()
    print(data)
