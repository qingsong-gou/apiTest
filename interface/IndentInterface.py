from utils.SendMethod import SendMethod
from interface.MemberInterface import Member


class Ident(object):
    '''
    city (string, optional): 城市 ,
    defaultStatus (integer, optional): 是否为默认 ,
    detailAddress (string, optional): 详细地址(街道) ,
    id (integer, optional),
    memberId (integer, optional),
    name (string, optional): 收货人名称 ,
    phoneNumber (string, optional),
    postCode (string, optional): 邮政编码 ,
    province (string, optional): 省份/直辖市 ,
    region (string, optional): 区
    '''

    def __init__(self):
        self.url = "http://139.159.146.104:8083"
        self.headers = {"Authorization": "Bearer " + Member().token_daxia()}

    def add_member_address(self, payload):  # 已通过
        '''
        添加收货地址,json格式
        :param payload:
        :return:
        '''
        url = self.url + "/member/address/add"
        method = "post"
        return SendMethod.send_method(method=method, url=url, json=payload, headers=self.headers)

    def delete_member_address(self, id):  # 已通过
        '''
        删除收货地址
        :param id:
        :return:
        '''
        url = self.url + "/member/address/delete/" + str(id)
        method = "post"
        return SendMethod.send_method(method=method, url=url, headers=self.headers)

    def list_member_address(self):  # 已通过
        '''显示所有收货地址'''
        url = self.url + "/member/address/list"
        method = "get"
        return SendMethod.send_method(method=method, url=url, headers=self.headers)

    def update_member_address(self, id, address):  # 已通过
        '''修改收货地址'''
        url = self.url + f"/member/address/update/{id}"
        method = "post"
        return SendMethod.send_method(method=method, url=url, json=address, headers=self.headers)

    def member_address(self, id):  # 已通过
        '''显示指定收货地址'''
        url = self.url + f"/member/address/{id}"
        method = "get"
        return SendMethod.send_method(method=method, url=url, headers=self.headers)


if __name__ == '__main__':
    # payload = {
    #     "city": "成都市",
    #     "defaultStatus": 0,
    #     "detailAddress": "晋阳街道",
    #     "id": 0,
    #     "memberId": 0,
    #     "name": "轻松大侠",
    #     "phoneNumber": "121",
    #     "postCode": "610000",
    #     "province": "四川省",
    #     "region": "武侯区"
    # }
    # print(Ident().add_member_address(payload=payload))
    print(Ident().list_member_address())
    # print(Ident().member_address(id=21))
    # address = {"defaultStatus": 1}
    # print(Ident().update_member_address(id=19, address=address))
    # print(Ident().delete_member_address(id=85))
