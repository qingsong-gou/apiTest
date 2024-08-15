"""
文件名:OperationData.py
作用:读取Excel表格和CSV文件,将excel数据读取成[{},{}]格式
"""
import pandas
import os
import json
import numpy


# base_path = os.path.dirname(__file__)  # 当前文件上一层的目录
# path = os.path.dirname(os.path.dirname(__file__)) + "/data" # 当前文件上上层
# print(path)
class OperationData:
    def __init__(self, filename):
        """
        通过传入的文件名,可以判其是CSV格式还是Excel格式,根据不同格式
        作出相应处理
        """
        # 得到存放数据的目录--数据在data文件夹中
        data_path = os.path.dirname(os.path.dirname(__file__)) + "/data"
        file_path = os.path.join(data_path, filename)  # 得到文件路径

        # 通过文件名判断文件格式
        if filename.split(".")[-1] == "csv":
            self.file = pandas.read_csv(file_path, keep_default_na=False)  # 如果是csv通过read_csv读取
        else:
            self.file = pandas.read_excel(file_path, keep_default_na=False)  # 如果是Excel,通过read_Excel读取

    def get_data_to_dict(self):
        """将文件数据获取成[{},{}]格式"""
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
        expect = [i["expect"] for i in data]  # 从原始数据中,取出expect
        for i in data:
            del i["expect"]  # 删除原始数据中的expect

        return list(zip(data, expect))

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


if __name__ == '__main__':
    oper = OperationData("add_cart_data.xlsx")
    datas = oper.format_data()[0]
    data = datas[0]
    expect = datas[1]
    print(data, expect)
