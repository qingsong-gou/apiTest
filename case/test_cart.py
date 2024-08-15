from utils.OperationData import OperationData
from interface.CartInterface import Cart
import pytest, time
from utils.GetKeyword import GetKeyword
from utils.Database import Database



def test_add_cart_1():
    '''
    验证添加数据库合理数据,添加成功,数据库有数据(添加了两条数据,方便后面清空购物车验证)
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
    result = Cart().add_cart(payload=payload)  # 获取响应内容
    result_2 = Cart().add_cart(payload=payload_2)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select delete_status from oms_cart_item where member_id=21 and product_id=27 "
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchall(sql=sql)
    print(res)
    pytest.assume(0 in GetKeyword.get_keywords(res, "delete_status"), "数据库不能查找到添加的数据")


def test_list_cart_1():
    '''
    查询添加的购物车的productId
    :return:
    '''
    result = Cart().list_cart()  # 获取购物车列表
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    pytest.assume(GetKeyword.get_keyword(result, "productId") == 27, "添加的不是productId为27的商品")  # 只添加了一件商品到购物车
    sql = "select * from oms_cart_item where member_id=21 and product_id=27"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的productId
    pytest.assume(res is not None, "数据库没有添加到购物车的商品")


def test_update_cart_quantity():
    '''
    修改商品数量
    :return:
    '''
    id = GetKeyword.get_keyword(Cart().list_cart(), "id")
    result = Cart().update_cart_quantity(id=id, quantity=10)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select quantity from oms_cart_item where id=%s"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql, args=[id])  # 获取数据库中的productId
    pytest.assume(res['quantity'] == 10, "修改购物车中商品的数量失败")


def test_delete_cart():
    '''
    删除商品
    :return:
    '''
    sql = "select id from oms_cart_item where member_id=21 and product_id=27"
    id = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                  port=3306).fetchone(sql=sql)
    result = Cart().delete_cart(ids=id["id"])
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select delete_status from oms_cart_item where member_id=21 and product_id=27"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的productId
    pytest.assume(GetKeyword.get_keyword(res, "delete_status") == 1, "删除失败,数据库仍然存在改数据")


def test_clear_cart():
    '''
    清空购物车
    :return:
    '''
    result = Cart().clear_cart()
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select delete_status from oms_cart_item where member_id=21 "
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchall(sql=sql)  # 获取数据库中的productId
    pytest.assume(0 not in GetKeyword.get_keywords(res, "delete_status"), "清空购物车失败,数据库仍然存在数据")


if __name__ == '__main__':
    pytest.main()
