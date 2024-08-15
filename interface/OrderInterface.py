from utils.SendMethod import SendMethod
from interface.MemberInterface import Member


class Order(object):
    def __init__(self):
        self.url = "http://139.159.146.104:8083"
        self.headers = {"Authorization": "Bearer " + Member().token_daxia()}

    def confirm_order(self):
        '''确认订单'''
        url = self.url + "/order/generateConfirmOrder"
        method = "post"
        return SendMethod.send_method(method=method, url=url, headers=self.headers)

    def generate_order(self, address_id, pay_type):
        '''生成订单'''
        url = self.url + "/order/generateOrder"
        method = "post"
        payload = {
            "memberReceiveAddressId": address_id,
            "payType": pay_type,
        }
        return SendMethod.send_method(method=method, url=url, json=payload, headers=self.headers)

    def pay_success(self, order_id):
        '''支付回调'''
        url = self.url + "/order/paySuccess"
        method = "post"
        payload={"orderId":order_id}
        return SendMethod.send_method(method=method, url=url, data=payload, headers=self.headers)


if __name__ == '__main__':
    # print(Order().confirm_order())
    # # # print(Order().generate_order(19,1))
    print(Order().pay_success(order_id=168))
