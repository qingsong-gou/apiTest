# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/18 17:00
@Author  : cody
@File    : Example.py

'''
import logging
import time

# 获取环境
from config.ApiBaseInfo import api_baiDuSerach
from config.setting import ENVIRONMENT_TEST, Token_PATH
from utils.OpreationData import OperationData
from utils.SendMethod import SendMethod
from utils.LogFormat import CaseLogFormat


# print(token)

class BaiDu(SendMethod):
    '''
    示例接口
    '''

    def __init__(self):
        # 每个接口类都获取token，需要则使用，不需要则不调用
        self.oper2 = OperationData(filename=Token_PATH)
        self.token = self.oper2.get_data_to_list()
        self.CaseLogFormat = CaseLogFormat

    def baiDuSerachToken(self, request_data, case_comment, excel_case_id):
        '''
        示例百度查询接口sugrec，传token
        :param request_data:
        :param case_comment:
        :param excel_case_id:
        :return:
        '''
        # 参数处理
        params = {
            "_t": time.time(),
            "bs": request_data
        }
        # 接口调用日志
        api_name = "baiDuSerach"
        logLine = self.CaseLogFormat.apiLog(excelCaseId=excel_case_id, apiName=api_name, requestData=request_data,
                                            caseComment=case_comment, token=self.token)
        logging.info(logLine)
        # 调用接口
        return self.send_method(method=api_baiDuSerach["method"], url=ENVIRONMENT_TEST + api_baiDuSerach["path"], params=params)

    def baiDuSerach(self, request_data, case_comment, excel_case_id):
        '''
        示例百度查询接口，不传token
        :return:
        '''
        # 参数处理
        params = {
            "_t": time.time(),
            "bs": request_data
        }
        # 接口调用日志
        api_name = "baiDuSerach"
        logLine = self.CaseLogFormat.apiLog(excelCaseId=excel_case_id, apiName=api_name, requestData=request_data,
                                            caseComment=case_comment)
        logging.info(logLine)
        # 调用接口
        return self.send_method(method=api_baiDuSerach["method"], url=ENVIRONMENT_TEST + api_baiDuSerach["path"], params=params)


if __name__ == '__main__':
    from utils.GetKeyWord import *

    request_data = "python"
    res = BaiDu.baiDuSerach(request_data=request_data)
    print(res)
    response_time = GetKeyword.get_keyword(data=res, keyword="response_time")
    print(response_time)
