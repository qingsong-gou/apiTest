# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/18 15:05
@Author  : cody
@File    : SendMethod.py

'''
import time

import requests


class SendMethod():
    @staticmethod
    def send_method(method, url, params=None, data=None, json=None, headers=None):
        '''
        :param method: 请求方式
        :param url: 请求地址
        :param params: get请求参数
        :param data: post请求参数   x-www-form-urlencoded格式
        :param json: post请求参数   json格式
        :return: result
        '''
        if method.lower() == "get":
            response = requests.get(url=url, params=params, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url=url, data=data, json=json, headers=headers)
        else:
            response = None
        result = {}
        if response:
            result["status_code"] = response.status_code
            result["headers"] = response.headers
            result["body"] = response.json()
            result["response_time"] = int(response.elapsed.microseconds / 1000)  # 转换成毫秒
            return result
        else:
            return "requestErro!"


if __name__ == '__main__':
    from GetKeyWord import *

    url = "https://www.baidu.com/sugrec"
    data = {
        "_t": time.time(),
        "bs": "python"
    }
    res = (SendMethod.send_method(method="get", url=url, data=data))
    print(res)
    response_time = GetKeyword.get_keyword(data=res, keyword="response_time")
    print(response_time)

