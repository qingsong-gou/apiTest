# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/21 13:34
@Author  : cody
@File    : conftest.py

调用登录接口，获取token
'''
import time

import pytest

from config.ApiBaseInfo import api_login
from config.setting import Get_TokenData, Token_PATH, ENVIRONMENT_TEST
from utils.GetKeyWord import GetKeyword
from utils.SendMethod import SendMethod


def login(request_data=Get_TokenData):
    '''
    获取token的接口
    :param request_data:
    :return:
    '''

    request_data["_t"] = time.time()
    res = SendMethod.send_method(method=api_login["method"], url=ENVIRONMENT_TEST + api_login["path"],
                                 params=request_data)
    response_time = GetKeyword.get_keyword(data=res, keyword="response_time")
    return str(response_time)


# 调用login获取token，测试仅执行一次
@pytest.fixture(scope='session', autouse=True)  # 自动执行
def getToken():
    # 调试获取token
    token = login()
    # time.sleep(5)
    with open(Token_PATH, "w", encoding="utf-8") as fp:
        fp.write("token\n")
        fp.write(token)



if __name__ == '__main__':
    print(login())

