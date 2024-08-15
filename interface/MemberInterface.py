from utils.SendMethod import SendMethod
from utils.GetKeyword import GetKeyword


class Member(object):
    def __init__(self):
        '''
        实例属性,每个对象都能使用
        '''
        self.url = "http://139.159.146.104:8083"

    def get_auth_code(self, telephone):
        '''
        获取验证码返回值
        :param telephone:
        :return:
        '''
        url = self.url + "/sso/getAuthCode"
        method = "get"
        payload = {"telephone": telephone}
        return SendMethod.send_method(method=method, url=url, params=payload)

    def get_verify(self, telephone):
        '''
        获取验证码返回值中的验证码
        :param telephone:
        :return:
        '''
        res = self.get_auth_code(telephone=telephone)
        return GetKeyword.get_keyword(res, "data")

    def member_register(self, username, password, telephone):
        '''
        会员注册
        :param username:
        :param password:
        :param telephone:
        :return:
        '''
        authcode = self.get_verify(telephone)
        url = self.url + "/sso/register"
        method = "post"
        payload = {"username": username, "password": password, "telephone": telephone,
                   "authCode": authcode}
        return SendMethod.send_method(method=method, url=url, data=payload)

    def member_login(self, username, password):
        '''
        会员登录
        :param username:
        :param password:
        :return:
        '''
        url = self.url + "/sso/login"
        method = "post"
        payload = {"username": username, "password": password}
        return SendMethod.send_method(method=method, url=url, data=payload)

    def token_daxia(self):
        '''
        会员登录
        :return:
        '''
        url = self.url + "/sso/login"
        method = "post"
        payload = {"username": "大侠3", "password": "123456"}
        return GetKeyword.get_keyword(SendMethod.send_method(method=method, url=url, data=payload), "token")


if __name__ == '__main__':
    print(Member().member_register("大侠3", "123456", 15922223300))
    print(Member().member_login("大侠3", "123456"))
    print(Member().token_daxia())
