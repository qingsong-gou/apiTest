import pytest

from interface.CartInterface import Cart
from utils.Database import Database
from utils.GetKeyword import GetKeyword


def test_delete_cart_1():
    '''
    删除不存在商品id
    :return:
    '''
    result = Cart().delete_cart(ids=100000)
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") != "操作成功", "断言开发自检字段")


def test_delete_cart_2():
    '''
    删除别人的商品id
    :return:
    '''
    result = Cart().delete_cart(ids=1)
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") != "操作成功", "断言开发自检字段")


def test_delete_cart_3():
    '''
    购物车多次删除同一件商品
    :return:
    '''
    payload = {
        "price": 649,
        "productAttr": '[{"key":"颜色","value":"金色"},{"key":"容量","value":"16G"}]',
        "productBrand": "小米",
        "productCategoryId": 19,
        "productId": 28,
        "productName": "小米 红米5A 全网通版 3GB+32GB 香槟金 移动联通电信4G手机 双卡双待",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5a9d248cN071f4959.jpg",
        "productSkuCode": "201808270028001",
        "productSkuId": 102,
        "productSn": "7437789",
        "productSubTitle": "8天超长待机，137g轻巧机身，高通骁龙处理器小米6X低至1299，点击抢购",
        "quantity": 1
    }
    Cart().add_cart(payload=payload)
    sql = "select id from oms_cart_item where member_id=21 and product_id=28"
    id = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                  port=3306).fetchone(sql=sql)
    Cart().delete_cart(ids=id["id"])
    result = Cart().delete_cart(ids=id["id"])
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") != "操作成功", "断言开发自检字段")


def test_delete_cart_4():
    '''
    删除多件商品
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
    payload_2 = {
        "price": 649,
        "productAttr": '[{"key":"颜色","value":"金色"},{"key":"容量","value":"16G"}]',
        "productBrand": "小米",
        "productCategoryId": 19,
        "productId": 28,
        "productName": "小米 红米5A 全网通版 3GB+32GB 香槟金 移动联通电信4G手机 双卡双待",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5a9d248cN071f4959.jpg",
        "productSkuCode": "201808270028001",
        "productSkuId": 102,
        "productSn": "7437789",
        "productSubTitle": "8天超长待机，137g轻巧机身，高通骁龙处理器小米6X低至1299，点击抢购",
        "quantity": 1
    }
    Cart().add_cart(payload=payload)  # 获取响应内容
    Cart().add_cart(payload=payload_2)
    sql_28 = "select id from oms_cart_item where member_id=21 and product_id=28"
    id_28 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                     port=3306).fetchone(sql=sql_28)
    sql_27 = "select id from oms_cart_item where member_id=21 and product_id=27"
    id_27 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                     port=3306).fetchone(sql=sql_27)
    result = Cart().delete_cart(ids=(GetKeyword.get_keyword(id_27, "id"), GetKeyword.get_keyword(id_28, "id")))
    pytest.assume(GetKeyword.get_keyword(result, "status_code") == 200, "断言状态码")
    pytest.assume(GetKeyword.get_keyword(result, "message") == "操作成功", "断言开发自检字段")
    sql = "DELETE FROM oms_cart_item WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql)


if __name__ == '__main__':
    pytest.main()
