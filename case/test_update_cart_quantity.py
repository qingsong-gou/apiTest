import pytest

from interface.CartInterface import Cart
from utils.GetKeyword import GetKeyword
from utils.Database import Database


def test_update_cart_quantity_1():
    '''
    修改商品数量为负数
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
        "quantity": 1
    }
    Cart().add_cart(payload=payload)  # 添加商品
    id = GetKeyword.get_keyword(Cart().list_cart(), "id")
    result = Cart().update_cart_quantity(id=id, quantity=-10)
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") != "操作成功", "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


def test_update_cart_quantity_2():
    '''
    修改商品数量为0
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
        "quantity": 1
    }
    Cart().add_cart(payload=payload)  # 添加商品
    id = GetKeyword.get_keyword(Cart().list_cart(), "id")
    result = Cart().update_cart_quantity(id=id, quantity=-0)
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") != "操作成功", "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


def test_update_cart_quantity_3():
    '''
    修改商品数量超过库存数量
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
        "quantity": 1
    }
    Cart().add_cart(payload=payload)  # 添加商品
    id = GetKeyword.get_keyword(Cart().list_cart(), "id")
    result = Cart().update_cart_quantity(id=id, quantity=99999999)
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") != "操作成功", "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


if __name__ == '__main__':
    pytest.main()
