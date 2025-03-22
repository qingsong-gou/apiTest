# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/20 09:44
@Author  : cody
@File    : LogFormat.py

'''


class CaseLogFormat():
    def __init__(self, excel_case_id):
        # 每条用例的标题
        self.excel_case_id = excel_case_id
        self.statusCodeErroRemark = "断言响应状态码失败"
        self.bodyErroRemark = "断言body内容失败"
        self.responseTimeErroRemark = "断言响应时间失败"

    def statusCodeLog(self, expect, actual):
        return f"{self.excel_case_id}:断言响应状态码;期望结果：{expect};实际结果：{actual}"

    def bodyLog(self, expect, actual):
        return f"{self.excel_case_id}:断言响应体字段值;期望结果:{expect};实际结果：{actual}"

    def responseTimeLog(self, expect, actual):
        return f"{self.excel_case_id}:断言响应时间;期望结果:{expect};实际结果：{actual}"

    @classmethod
    def apiLog(self, apiName, requestData, excelCaseId, caseComment=None, token=None):
        return f"用例id：{excelCaseId}:接口名称：{apiName};传递token：{token};传递参数：{requestData};用例备注：{caseComment}"


if __name__ == '__main__':
    logLine = CaseLogFormat.apiLog(apiName="testApi", requestData="testData", excelCaseId="001")
    print(logLine)
