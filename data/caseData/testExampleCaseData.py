# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/20 15:48
@Author  : cody
@File    : testExampleCaseData.py
数据处理中转

'''

from utils.OpreationData import OperationData

excelFileName = "testdata.xlsx"
csvFileName = "testdata.csv"
envFileNasme = "testExample.xlsx"

# 接口数据excel文件
oper = OperationData(filename=excelFileName, sheet_name=0)
# oper = OperationData(filename=fileName, sheet_name="testSheet1")
excel_data_baiDuSerach_sheetOne = oper.get_data_to_dict()

# 接口数据excel文件
oper = OperationData(filename=excelFileName, sheet_name="testSheet2")
excel_data_baiDuSerach_sheetTwo = oper.get_data_to_dict()

# 接口数据csv文件
oper = OperationData(filename=csvFileName)
csv_data_baiDuSerach = oper.get_data_to_dict()

# 用例前置处理数据
oper = OperationData(filename=envFileNasme, dataType="env", sheet_name="setup_TestBaiDu")
setup_TestBaiDu_data = oper.get_data_to_list()

# 用例后置处理数据
oper = OperationData(filename=envFileNasme, dataType="env", sheet_name="teardown_TestBaiDu")
teardown_TestBaiDu_data = oper.get_data_to_list()

if __name__ == '__main__':
    # print(excel_data_baiDuSerach_sheetOne)
    # print(excel_data_baiDuSerach_sheetTwo)
    # print(csv_data_baiDuSerach)
    print(setup_TestBaiDu_data)
    print(teardown_TestBaiDu_data)

    # print(teardown_TestBaiDu_data[0][2].split(","))
    # print(teardown_TestBaiDu_data[0])
