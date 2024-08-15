import pytest

from interface.CartInterface import Cart
from utils.Database import Database


def test_add_cart_1():
    '''
    添加商品价格为负数
    :return:
    '''
    payload = {
        "price": -100,
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
    result = Cart().add_cart(payload=payload)  # 获取响应内容
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    print(result)
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


def test_add_cart_2():
    '''
    添加商品数量为负数
    :return:
    '''
    payload = {
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
        "quantity": -10
    }
    result = Cart().add_cart(payload=payload)  # 获取响应内容
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    print(result)
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


def test_add_cart_3():
    '''
    添加商品数量为0
    :return:
    '''
    payload = {
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
        "quantity": 0
    }
    result = Cart().add_cart(payload=payload)  # 获取响应内容
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    print(result)
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


def test_add_cart_4():
    '''
    添加商品数量超过库存
    :return:
    '''
    payload = {
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
        "quantity": 999999
    }
    result = Cart().add_cart(payload=payload)  # 获取响应内容
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    print(result)
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


def test_add_cart_5():
    '''
    添加商品数量productSkuId与商品属性不一致
    :return:
    '''
    payload = {
        "price": 2699,
        "productAttr": '[{"key":"颜色","value":"黑色"},{"key":"容量","value":"32G"}]',
        "productBrand": "小米",
        "productCategoryId": 19,
        "productId": 27,
        "productName": "小米8 全面屏游戏智能手机 6GB+64GB 黑色 全网通4G 双卡双待",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/xiaomi.jpg",
        "productSkuCode": "201808270027001",
        "productSkuId": 9,
        "productSn": "7437788",
        "productSubTitle": "骁龙845处理器，红外人脸解锁，AI变焦双摄，AI语音助手小米6X低至1299，点击抢购",
        "quantity": 1
    }
    result = Cart().add_cart(payload=payload)  # 获取响应内容
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    print(result)
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


if __name__ == '__main__':
    pytest.main()
