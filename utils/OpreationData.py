# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/18 15:26
@Author  : cody
@File    : OpreationData.py

'''
import pandas
import os
import json
import numpy
from pandas.io.formats.format import return_docstring

from config.setting import EXCEL_DATA_PATH, CSV_DATA_PATH, Env_DATA_PATH,BASE_PATH, LOG_PATH  # 数据存放目录


class OperationData:
    def __init__(self, filename,dataType="case" ,sheet_name=0):
        """
        通过传入的文件名,可以判其是CSV格式还是Excel格式,根据不同格式
        作出相应处理
        """

        # 通过文件名判断文件格式
        if filename.split(".")[-1] == "csv":
            file_path = os.path.join(CSV_DATA_PATH, filename)  # 得到文件路径
            self.file = pandas.read_csv(file_path, keep_default_na=False)  # 如果是csv通过read_csv读取
        else:
            if dataType=="env":
                file_path = os.path.join(Env_DATA_PATH,filename)
            else:
                file_path = os.path.join(EXCEL_DATA_PATH, filename)  # 得到文件路径
            self.file = pandas.read_excel(file_path, sheet_name=sheet_name,
                                          keep_default_na=False)  # 如果是Excel,通过read_Excel读取,默认为0

    def get_data_to_dict(self):
        """将文件数据获取成[{},{}]格式"""
        # return [self.file.loc[i].to_dict() for i in self.file.index.values]
        return [self.file.loc[i].to_dict() for i in self.file.index.values]

    def get_data_to_list(self):
        """将文件数据获取成[[],[]]格式"""
        return self.file.values.tolist()

    def format_data(self):
        """
        1.从原始数据中取出comment字段值
        2.和原始数据重新组合成新数据[({},''),({},'')]
        :return:
        """
        data = self.get_data_to_dict()
        print(data)
        try:
            response_expect = [i["response_expect"] for i in data]  # 从原始数据中,取出expect
            for i in data:
                del i["response_expect"]  # 删除原始数据中的expect
            status_code = [i["status_code"] for i in data]  # 从原始数据中,取出expect
            for i in data:
                del i["status_code"]  # 删除原始数据中的expect
            response_time = [i["response_time"] for i in data]  # 从原始数据中,取出expect
            for i in data:
                del i["response_time"]  # 删除原始数据中的expect
        except Exception as e:
            return "Erro: response_expect status_code response_time"
        else:
            return list(zip(data, response_expect, status_code, response_time))

    def new_dict(self):
        dict_str = json.dumps(self.get_data_to_dict(), cls=NpEncoder)  # 将int64字段,转为int
        return json.loads(dict_str)


# 处理pandas读取CSV/excel中整数数据类型
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):  # numpy.integer 是int64
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


#
# def makeDir(dirName):
#     '''
#     检查并创建文件夹
#     :return:
#     '''
#     log_path = os.path.join(LOG_PATH,
#                             dirName)
#     if not os.path.exists(log_path):
#         os.makedirs(log_path)
#     return log_path + '\\'


if __name__ == '__main__':
    pass
    oper = OperationData(filename="testdata.xlsx", sheet_name="testSheet1")
    datas = oper.get_data_to_dict()
    print(datas[0])
    print(datas[0]["request_data"])

    oper2 = OperationData(filename="testdata.csv")
    datas2 = oper.get_data_to_dict()
    print(datas2[0])
    print(datas2[0]["request_data"])

    # data = datas[0]  # 除开response_expect
    # response_expect = datas[1]
    # print(data, response_expect)

    # file_path = os.path.join(DATA_PATH, "testdata.xlsx")
    # data=pandas.read_excel(file_path, sheet_name=0,
    #                     keep_default_na=False)
    # print(data)
