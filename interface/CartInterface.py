from utils.SendMethod import SendMethod
from interface.MemberInterface import Member


class Cart(object):
    '''
    "createDate": 创建时间
    "deleteStatus": 是否删除
    "id": id编号
    "memberId": 会员id
    "memberNickname": 会员名称
    "modifyDate": 修改时间
    "price": 添加到购物车的价格
    "productAttr":商品销售属性
    "productBrand": 产品品牌
    "productCategoryId":商品分类
    "productId": 产品id
    "productName": 产品名称
    "productPic": 产品主图
    "productSkuCode":产品sku条码
    "productSkuId":sku的id
    "productSn":产品货号
    "productSubTitle":产品副标题(卖点)
    "quantity": 产品数量
    '''

    def __init__(self):
        self.url = "http://139.159.146.104:8083"
        self.headers = {"Authorization": "Bearer " + Member().token_daxia()}

    def add_cart(self, payload):  # 已通过
        '''
        添加购物车,添加的商品应该是数据库有的,否则是不能提交订单的(业务逻辑),json格式
        :param payload:
        :return:
        '''
        url = self.url + "/cart/add"
        method = "post"
        return SendMethod.send_method(method=method, url=url, json=payload, headers=self.headers)

    def clear_cart(self):  # 已通过
        '''
        清空购物车
        :return:
        '''
        url = self.url + "/cart/clear"
        method = "post"
        return SendMethod.send_method(method=method, url=url, headers=self.headers)

    def delete_cart(self, ids):  # 已通过
        '''
        删除购物车中的某个商品
        :return:
        '''
        url = self.url + "/cart/delete"
        method = "post"
        data = {"ids": ids}
        return SendMethod.send_method(method=method, url=url, data=data, headers=self.headers)

    # def get_product(self, productId):
    #     '''
    #     获取购物车中某个商品的规格,用于重选规格
    #     :param productId:
    #     :return:
    #     '''
    #     url = self.url + f"/cart/getProduct/{productId}"
    #     method = "get"
    #     return SendMethod.send_method(method=method, url=url, headers=self.headers)

    def list_cart(self):  # 已通过
        '''
        获取某个会员的购物车列表
        :return:
        '''
        url = self.url + "/cart/list"
        method = "get"
        return SendMethod.send_method(method=method, url=url, headers=self.headers)

    # def list_cart_promotion(self):
    #     '''
    #     获取某个会员的购物车列表,包括促销信息
    #     :return:
    #     '''
    #     url = self.url + "/cart/list/promotion"
    #     method = "get"
    #     return SendMethod.send_method(method=method, url=url, headers=self.headers)

    # def update_cart_attr(self, payload: dict):  # 已通过,商品属性颜色无法修改
    #     '''
    #     修改购物车中商品的规格,json格式
    #     :return:
    #     '''
    #     url = self.url + "/cart/update/attr"
    #     method = "post"
    #     return SendMethod.send_method(method=method, url=url, json=payload, headers=self.headers)

    def update_cart_quantity(self, id, quantity):  # 已通过
        '''
        修改购物车中某个商品的数量
        :return:
        '''
        url = self.url + "/cart/update/quantity"
        method = "get"
        payload = {"id": id, "quantity": quantity}
        return SendMethod.send_method(method=method, url=url, params=payload, headers=self.headers)


if __name__ == '__main__':
    # payload = {
    #     "price": 2699,
    #     "productAttr": '[{"key":"颜色","value":"黑色"},{"key":"容量","value":"32G"}]',
    #     "productBrand": "小米",
    #     "productCategoryId": 19,
    #     "productId": 27,
    #     "productName": "小米8 全面屏游戏智能手机 6GB+64GB 黑色 全网通4G 双卡双待",
    #     "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/xiaomi.jpg",
    #     "productSkuCode": "201808270027001",
    #     "productSkuId": 98,
    #     "productSn": "7437788",
    #     "productSubTitle": "骁龙845处理器，红外人脸解锁，AI变焦双摄，AI语音助手小米6X低至1299，点击抢购",
    #     "quantity": 2
    # }
    # print(Cart().add_cart(payload=payload))
    # print(Cart().list_cart())
    print(Cart().update_cart_quantity(id=33, quantity=1))
    payload = {
        "createDate": "2021-03-02T06:44:52.051Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T06:44:52.051Z",
        "price": 2699,
        "productAttr": '[{"key":"颜色","value":"黑色"},{"key":"容量","value":"32G"}]',
        "productBrand": "小米",
        "productCategoryId": 19,
        "productId": 27,
        "productName": "小米8 全面屏游戏智能手机 6GB+64GB 黑色 全网通4G 双卡双待",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/xiaomi.jpg",
        "productSkuCode": "201808270027001",
        "productSkuId": 98,
        "productSn": "7437788",
        "productSubTitle": "骁龙845处理器，红外人脸解锁，AI变焦双摄，AI语音助手小米6X低至1299，点击抢购",
        "quantity": 1
    }
    # print(Cart().update_cart_attr(payload=payload))
    print(Cart().delete_cart(ids=33))
    print(Cart().clear_cart())
