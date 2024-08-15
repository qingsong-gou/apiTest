'''
请求地址:url
请求方式:
    post
    get
请求参数:
    post方式:
        x-www-form-urlencoded格式-->data
        json格式-->json
    get方式:
        params
返回值:
    response.headers
    response.status_code
    response.json()
    response.elapsed.microseconds
'''
import requests


class SendMethod(object):
    @staticmethod
    def send_method(method, url, params=None, data=None, json=None,headers=None):
        '''
        mall项目请求方式
        :param method: 请求方式
        :param url: 请求地址
        :param params: get请求参数
        :param data: post请求参数   x-www-form-urlencoded格式
        :param json: post请求参数   json格式
        :return: result
        '''
        if method.lower() == "get":
            response = requests.get(url=url, params=params,headers=headers)
        elif method.lower() == "post":
            response = requests.post(url=url, data=data, json=json,headers=headers)
        else:
            response = None
        # 定义一个空字典接收数据,并作为函数返回值
        result = {}
        # 判断response
        if response:
            result["status_code"] = response.status_code
            result["headers"] = response.headers
            result["body"] = response.json()
            result["response_time"] = int(response.elapsed.microseconds / 1000)  # 转换成毫秒
            return result
        else:
            return "请求失败!"


if __name__ == '__main__':
    json = {
        "password": "macro123",
        "username": "admin"
    }
    res = (SendMethod.send_method(method="post", url="http://139.159.146.104:8082/admin/login", json=json))
    print(res)
    token = res["body"]["data"]["token"]
    print(token)
