# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/18 17:34
@Author  : cody
@File    : testExample.py

'''
import time
import logging

from config.setting import Token_PATH
from interface.Example import BaiDu
import pytest

from utils.GetKeyWord import *
from utils.LogFormat import CaseLogFormat

from data.caseData.testExampleCaseData import excel_data_baiDuSerach_sheetOne, excel_data_baiDuSerach_sheetTwo, \
    csv_data_baiDuSerach, setup_TestBaiDu_data, teardown_TestBaiDu_data
from utils.Database import Database


class TestBaiDu():

    @classmethod
    def setup_class(cls, list_data=setup_TestBaiDu_data):
        '''
        数据库待调试
        tableName = list_data[0]
        tableColumns = list_data[1].split(",")
        tableVlues = list_data[2].split(",")
        sql = "insert into %s (%s,%s) values (%s,%s)"  # 构造前置数据
        data = (tableName, tableColumns[0], tableColumns[1], tableVlues[0], tableVlues[1])
        # 执行前置sql
        cls.db = Database()
        cls.db.executemany(sql=sql, args=data)
        '''

        print("cody class setup", list_data)

    @classmethod
    def teardown_class(cls, list_data=teardown_TestBaiDu_data):
        '''
        数据库待调试
        # 获取后置数据
        tableName = list_data[0]
        tableColumns = list_data[1].split(",")
        tableVlues = list_data[2].split(",")
        sql = "delete from  %s  where %s=%s and %s=%s"  # 清理前置数据
        data = (tableName, tableColumns[0], tableVlues[0], tableColumns[1], tableVlues[1])
        # 执行后置sql
        cls.db.executemany(sql=sql, args=data)
        '''

        print("cody class teardown", list_data)

    def setup(self, ):
        print("cody funcation setup")

    def teardown(self):
        print("cody funcation teardown ")

    @pytest.mark.normal
    @pytest.mark.parametrize("dic_data", excel_data_baiDuSerach_sheetOne)
    def test_baiDuSerach_sheetOne(self, dic_data):
        '''
         备注信息，写入report的description字段中，接口测试
        '''

        # 获取表格中的接口用例数据
        excel_case_id = dic_data["case_id"]
        excel_request_data = dic_data["request_data"]
        excel_status_code = dic_data["status_code"]
        excel_response_expect = dic_data["response_expect"]
        excel_response_time = dic_data["response_time"]
        excel_case_comment = dic_data["case_comment"]

        # 实例化日志格式化对象
        cf = CaseLogFormat(excel_case_id)

        # 调用接口获取响应数据
        res = BaiDu().baiDuSerach(request_data=excel_request_data, case_comment=excel_case_comment,
                                  excel_case_id=excel_case_id)
        # 断言响应状态码
        response_status_code = GetKeyword.get_keyword(data=res, keyword="status_code")
        logging.info(msg=cf.statusCodeLog(expect=excel_status_code, actual=response_status_code))
        pytest.assume(response_status_code == excel_status_code, msg=cf.statusCodeErroRemark)

        # 断言body里面的数据
        response_expect = GetKeyword.get_keyword(data=res, keyword="err_no")
        logging.info(msg=cf.bodyLog(expect=excel_response_expect, actual=response_expect))
        pytest.assume(excel_response_expect == response_expect, msg=cf.bodyErroRemark)

        # 断言响应时间
        response_time = GetKeyword.get_keyword(data=res, keyword="response_time")
        logging.info(msg=cf.responseTimeLog(expect=excel_response_time, actual=response_time))
        pytest.assume(response_time <= excel_response_time, msg=cf.responseTimeErroRemark)

    @pytest.mark.normal
    @pytest.mark.parametrize("dic_data", excel_data_baiDuSerach_sheetTwo)
    def test_baiDuSerach_sheetTwo(self, dic_data):
        '''
         备注信息，传token接口测试
        '''

        # 获取表格中的接口用例数据
        excel_case_id = dic_data["case_id"]
        excel_request_data = dic_data["request_data"]
        excel_status_code = dic_data["status_code"]
        excel_response_expect = dic_data["response_expect"]
        excel_response_time = dic_data["response_time"]
        excel_case_comment = dic_data["case_comment"]

        # 实例化日志格式化对象
        cf = CaseLogFormat(excel_case_id)

        # 调用接口获取响应数据
        res = BaiDu().baiDuSerachToken(request_data=excel_request_data, case_comment=excel_case_comment,
                                       excel_case_id=excel_case_id)
        # 断言响应状态码
        response_status_code = GetKeyword.get_keyword(data=res, keyword="status_code")
        logging.info(msg=cf.statusCodeLog(expect=excel_status_code, actual=response_status_code))
        pytest.assume(response_status_code == excel_status_code, msg=cf.statusCodeErroRemark)

        # 断言body里面的数据
        response_expect = GetKeyword.get_keyword(data=res, keyword="err_no")
        logging.info(msg=cf.bodyLog(expect=excel_response_expect, actual=response_expect))
        pytest.assume(excel_response_expect == response_expect, msg=cf.bodyErroRemark)

        # 断言响应时间
        response_time = GetKeyword.get_keyword(data=res, keyword="response_time")
        logging.info(msg=cf.responseTimeLog(expect=excel_response_time, actual=response_time))
        pytest.assume(response_time <= excel_response_time, msg=cf.responseTimeErroRemark)

    @pytest.mark.normal
    @pytest.mark.parametrize("dic_data", csv_data_baiDuSerach)
    def test_baiDuSerach_csv(self, dic_data):
        '''
         备注信息，传token接口测试
        '''

        # 获取表格中的接口用例数据
        excel_case_id = dic_data["case_id"]
        excel_request_data = dic_data["request_data"]
        excel_status_code = dic_data["status_code"]
        excel_response_expect = dic_data["response_expect"]
        excel_response_time = dic_data["response_time"]
        excel_case_comment = dic_data["case_comment"]

        # 实例化日志格式化对象
        cf = CaseLogFormat(excel_case_id)

        # 调用接口获取响应数据
        res = BaiDu().baiDuSerachToken(request_data=excel_request_data, case_comment=excel_case_comment,
                                       excel_case_id=excel_case_id)
        # 断言响应状态码
        response_status_code = GetKeyword.get_keyword(data=res, keyword="status_code")
        logging.info(msg=cf.statusCodeLog(expect=excel_status_code, actual=response_status_code))
        pytest.assume(response_status_code == excel_status_code, msg=cf.statusCodeErroRemark)

        # 断言body里面的数据
        response_expect = GetKeyword.get_keyword(data=res, keyword="err_no")
        logging.info(msg=cf.bodyLog(expect=excel_response_expect, actual=response_expect))
        pytest.assume(excel_response_expect == response_expect, msg=cf.bodyErroRemark)

        # 断言响应时间
        response_time = GetKeyword.get_keyword(data=res, keyword="response_time")
        logging.info(msg=cf.responseTimeLog(expect=excel_response_time, actual=response_time))
        pytest.assume(response_time <= excel_response_time, msg=cf.responseTimeErroRemark)


if __name__ == '__main__':
    pytest.main()
