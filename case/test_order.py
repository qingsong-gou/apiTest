from interface.IndentInterface import Ident
from interface.OrderInterface import Order
import pytest, allure
from utils.GetKeyword import GetKeyword
from utils.Database import Database
from interface.CartInterface import Cart

data = [1, 2, 3, 4]


@allure.title("购买折扣商品")
@allure.story("购物促销活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantitys", data)
def test_order(quantitys):
    '''购买折扣商品'''
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
        "quantity": quantitys
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item WHERE member_id=21;"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21;"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args = [27, '[{"key":"颜色","value":"黑色"},{"key":"容量","value":"32G"}]']
    sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                          charset="utf8",
                          port=3306).fetchone(sql=sql, args=args)
    stock = GetKeyword.get_keyword(sql_result, "stock")
    # 1添加购物车
    with allure.step("添加购物车"):
        cart_result = Cart().add_cart(payload=payload)
        pytest.assume(GetKeyword.get_keyword(cart_result, "code") == 200, "开发自检字段不是200")
        cart_sql = "SELECT * from oms_cart_item WHERE member_id=21 and product_id = %s and product_sku_id=%s and quantity=%s and delete_status=%s "
        quantity = payload["quantity"]
        cart_args = [27, 98, quantity, 0]
        cart_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                   charset="utf8",
                                   port=3306).fetchone(sql=cart_sql, args=cart_args)
        pytest.assume(cart_sql_result != None, "数据库购物车表中没有添加的数据")
    # 2.确认订单
    with allure.step("确认订单"):
        order_result = Order().confirm_order()
        pytest.assume(GetKeyword.get_keyword(order_result, "code") == 200, "断言开发自检字段")
        promotionAmount = GetKeyword.get_keyword(order_result, "promotionAmount")  # 优惠金额
        payAmount = GetKeyword.get_keyword(order_result, "payAmount")  # 支付金额
        if quantity == 2:
            promotionAmount_result = round(0.2 * quantity * payload["price"], 1)
            payAmount_result = round(0.8 * quantity * payload["price"], 1)
        elif quantity >= 3:
            promotionAmount_result = round(0.25 * quantity * payload["price"], 2)
            payAmount_result = round(0.75 * quantity * payload["price"], 2)
        else:
            promotionAmount_result = 0
            payAmount_result = quantity * payload["price"]
        pytest.assume(promotionAmount == promotionAmount_result, "优惠金额不正确")
        pytest.assume(payAmount == payAmount_result, "支付金额不正确")
        print(promotionAmount, promotionAmount_result, payAmount, payAmount_result)
    # 3.生成订单,先创建一个收货地址
    with allure.step("生成订单"):
        payload = {
            "city": "成都市",
            "defaultStatus": 0,
            "detailAddress": "晋阳街道",
            "id": 0,
            "memberId": 0,
            "name": "轻松大侠",
            "phoneNumber": "121",
            "postCode": "610000",
            "province": "四川省",
            "region": "武侯区"
        }
        Ident().add_member_address(payload=payload)
        address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
        generate_result = Order().generate_order(address_id=address_id, pay_type=1)
        print(generate_result)
        pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200, "断言开发自检字段")
        order_id = GetKeyword.get_keyword(generate_result, "orderId")  # 获取返回值中订单号的id
        # 购物车订单delete_status=1
        cart_sql_2 = "SELECT delete_status from oms_cart_item WHERE member_id=21 and product_id = %s and product_sku_id=%s and quantity=%s "
        cart_args_2 = [27, 98, quantity]
        cart_sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                     charset="utf8",
                                     port=3306).fetchone(sql=cart_sql_2, args=cart_args_2)
        pytest.assume(GetKeyword.get_keyword(cart_sql_result_2, "delete_status") == 1,
                      "数据库中购物车表该条记录没有变成delete_status=1")
        # 数据库中订单表已生成
        order_sql = "SELECT status from oms_order WHERE member_id=21 and id=%s "
        order_args = [order_id]
        order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                    charset="utf8",
                                    port=3306).fetchone(sql=order_sql, args=order_args)
        pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0, "订单status不为0,应该是0未付款")
    # # # 4.支付回调
    with allure.step("支付回调"):
        pay_success_result = Order().pay_success(order_id=order_id)
        print(pay_success_result)
        pytest.assume(GetKeyword.get_keyword(pay_success_result, "code") == 200, "断言开发自检字段")
        # 数据库订单生效
        order_sql = "SELECT status from oms_order WHERE member_id=21 and id=%s "
        order_args = [order_id]
        order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                    charset="utf8",
                                    port=3306).fetchone(sql=order_sql, args=order_args)
        pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1, "订单status不为1,应该是1待发货")
    sql_0 = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_0 = [27, '[{"key":"颜色","value":"黑色"},{"key":"容量","value":"32G"}]']
    sql_result_0 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql_0, args=args_0)
    stock_0 = GetKeyword.get_keyword(sql_result_0, "stock")
    print(stock, quantitys, stock_0)
    pytest.assume(stock - quantitys == stock_0, '数据库该商品库存数量前后差值不等于购买商品的数量')
    # 删除地址
    Ident().delete_member_address(id=address_id)


data_2 = [1, 2, 3]


@allure.title("购买满减商品")
@allure.story("购物促销活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantitys", data_2)
def test_order2(quantitys):
    """购买满减商品"""
    # 1.添加购物车
    cart_payload = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
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
        "quantity": quantitys
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item  WHERE member_id=21"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args = [cart_payload["productId"], cart_payload["productAttr"]]
    sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                          charset="utf8",
                          port=3306).fetchone(sql=sql, args=args)
    stock = GetKeyword.get_keyword(sql_result, "stock")
    cart_result = Cart().add_cart(cart_payload)  # 添加满减商品到购物车
    print(cart_result)
    pytest.assume(GetKeyword.get_keyword(cart_result, "code") == 200)  # 断言添加购物车是否成功
    cart_sql = """SELECT * FROM oms_cart_item WHERE member_id = 21 AND delete_status = %s AND quantity=%s AND product_sku_id=%s"""
    cart_args = [0, quantitys, 102]
    cart_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                               charset="utf8",
                               port=3306).fetchone(sql=cart_sql, args=cart_args)
    pytest.assume(cart_sql_result != None)  # 断言SQL不为空
    # 2.确认订单
    order = Order()
    confirm_order = order.confirm_order()
    print(confirm_order)
    pytest.assume(GetKeyword.get_keyword(confirm_order, "code") == 200)  # 断言确认订单是否请求成功
    promotionAmount = GetKeyword.get_keyword(confirm_order, "promotionAmount")  # 获取返回值中的优惠金额
    payAmount = GetKeyword.get_keyword(confirm_order, "payAmount")  # 获取返回值中的支付金额
    price = cart_payload["price"] * cart_payload["quantity"]
    if price >= 500 and price < 1000:
        reduce_price = 50
    elif price >= 1000:
        reduce_price = 120
    else:
        reduce_price = 0
    pytest.assume(reduce_price == promotionAmount)  # 断言满减金额是否正确
    pay_price = price - reduce_price  # 支付金额
    print(promotionAmount, reduce_price, pay_price, payAmount)
    pytest.assume(pay_price == payAmount)  # 断言支付金额是否正确
    # 3.生成订单,先创建一个收货地址
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大侠",
        "phoneNumber": "121",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    Ident().add_member_address(payload=payload)
    address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    generate_result = Order().generate_order(address_id, 1)
    print(generate_result)
    pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200)
    order_id = GetKeyword.get_keyword(generate_result, "orderId")
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0)  # 断言数据库中订单是否生成
    cart_sql = """SELECT delete_status FROM oms_cart_item WHERE member_id = 21 AND quantity=%s AND product_sku_id=%s"""
    args_cart = [quantitys, 102]
    cart_sql_result_after = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                     charset="utf8",
                                     port=3306).fetchone(sql=cart_sql, args=args_cart)
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    # 4.支付回调
    pay_result = order.pay_success(order_id=order_id)
    print(pay_result)
    pytest.assume(GetKeyword.get_keyword(pay_result, "code") == 200)
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1)
    sql_0 = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_0 = [cart_payload["productId"], cart_payload["productAttr"]]
    sql_result_0 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql_0, args=args_0)
    stock_0 = GetKeyword.get_keyword(sql_result_0, "stock")
    print(stock, quantitys, stock_0)
    pytest.assume(stock - quantitys == stock_0, '数据库该商品库存数量前后差值不等于购买商品的数量')
    # 删除地址
    Ident().delete_member_address(id=address_id)


data_3 = [2]


@allure.title("购买普通商品")
@allure.story("购物促销无活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantitys", data_3)
def test_order3(quantitys):
    '''普通商品'''
    # 1.添加购物车
    cart_payload = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
        "price": 369,
        "productAttr": '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"39"},{"key":"风格","value":"秋季"}]',
        "productBrand": "NIKE",
        "productCategoryId": 29,
        "productId": 35,
        "productName": "耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5b235bb9Nf606460b.jpg",
        "productSkuCode": "202002250035008",
        "productSkuId": 178,
        "productSn": "6799342",
        "productSubTitle": "8耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "quantity": quantitys
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item  WHERE member_id=21"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args = [cart_payload["productId"], cart_payload["productAttr"]]
    sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                          charset="utf8",
                          port=3306).fetchone(sql=sql, args=args)
    stock = GetKeyword.get_keyword(sql_result, "stock")
    cart_result = Cart().add_cart(cart_payload)  # 添加满减商品到购物车
    pytest.assume(GetKeyword.get_keyword(cart_result, "code") == 200)  # 断言添加购物车是否成功
    cart_sql = """SELECT * FROM oms_cart_item WHERE member_id = 21 AND delete_status = %s AND quantity=%s AND product_sku_id=%s"""
    cart_args = [0, quantitys, cart_payload["productSkuId"]]
    cart_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                               charset="utf8",
                               port=3306).fetchone(sql=cart_sql, args=cart_args)
    pytest.assume(cart_sql_result != None)  # 断言SQL不为空
    # 2.确认订单
    order = Order()
    confirm_order = order.confirm_order()
    pytest.assume(GetKeyword.get_keyword(confirm_order, "code") == 200)  # 断言确认订单是否请求成功
    promotionAmount = GetKeyword.get_keyword(confirm_order, "promotionAmount")  # 获取返回值中的优惠金额
    payAmount = GetKeyword.get_keyword(confirm_order, "payAmount")  # 获取返回值中的支付金额
    price = cart_payload["price"] * cart_payload["quantity"]
    pytest.assume(0 == promotionAmount)  # 断言满减金额是否正确
    print(promotionAmount, price, payAmount)
    pytest.assume(price == payAmount)  # 断言支付金额是否正确
    # 3.生成订单,先创建一个收货地址
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大侠",
        "phoneNumber": "121",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    Ident().add_member_address(payload=payload)
    address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    generate_result = Order().generate_order(address_id, 1)
    print(generate_result)
    pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200)
    order_id = GetKeyword.get_keyword(generate_result, "orderId")
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0)  # 断言数据库中订单是否生成
    cart_sql = """SELECT delete_status FROM oms_cart_item WHERE member_id = 21 AND quantity=%s AND product_sku_id=%s"""
    args_cart = [quantitys, cart_payload["productSkuId"]]
    cart_sql_result_after = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                     charset="utf8",
                                     port=3306).fetchone(sql=cart_sql, args=args_cart)
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    # 4.支付回调
    pay_result = order.pay_success(order_id=order_id)
    pytest.assume(GetKeyword.get_keyword(pay_result, "code") == 200)
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1)
    sql_0 = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_0 = [cart_payload["productId"], cart_payload["productAttr"]]
    sql_result_0 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql_0, args=args_0)
    stock_0 = GetKeyword.get_keyword(sql_result_0, "stock")
    print(stock, quantitys, stock_0)
    pytest.assume(stock - quantitys == stock_0, '数据库该商品库存数量前后差值不等于购买商品的数量')
    # 删除地址
    Ident().delete_member_address(id=address_id)


data_4 = [(1, 1)]


@allure.title("购买普通商品和满减商品")
@allure.story("购物促销活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantity_1,quantity_2", data_4)
def test_test_order4(quantity_1, quantity_2):
    '''普通商品和满减商品'''
    # 添加购物车
    payload_1 = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
        "price": 369,
        "productAttr": '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"39"},{"key":"风格","value":"秋季"}]',
        "productBrand": "NIKE",
        "productCategoryId": 29,
        "productId": 35,
        "productName": "耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5b235bb9Nf606460b.jpg",
        "productSkuCode": "202002250035008",
        "productSkuId": 178,
        "productSn": "6799342",
        "productSubTitle": "8耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "quantity": quantity_1
    }
    payload_2 = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
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
        "quantity": quantity_2
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item  WHERE member_id=21"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_1 = [payload_1["productId"], payload_1["productAttr"]]
    args_2 = [payload_2["productId"], payload_2["productAttr"]]
    sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_1)
    sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_2)
    stock_1 = GetKeyword.get_keyword(sql_result_1, "stock")  # 获取普通商品数量
    stock_2 = GetKeyword.get_keyword(sql_result_2, "stock")  # 获取满减商品数量
    cart_result_1 = Cart().add_cart(payload_1)  # 添加普通商品到购物车
    cart_result_2 = Cart().add_cart(payload_2)  # 添加满减商品到购物车
    pytest.assume(GetKeyword.get_keyword(cart_result_1, "code") == 200)
    pytest.assume(GetKeyword.get_keyword(cart_result_2, "code") == 200)
    cart_sql = """SELECT * FROM oms_cart_item WHERE member_id = 21 AND delete_status = %s AND quantity=%s AND product_sku_id=%s"""
    cart_args_1 = [0, quantity_1, payload_1["productSkuId"]]
    cart_args_2 = [0, quantity_2, payload_2["productSkuId"]]
    cart_sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_1)
    cart_sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_2)
    pytest.assume(cart_sql_result_1 != None)  # 断言SQL不为空
    pytest.assume(cart_sql_result_2 != None)  # 断言SQL不为空
    # 确认订单
    order = Order()
    confirm_order = order.confirm_order()
    pytest.assume(GetKeyword.get_keyword(confirm_order, "code") == 200)  # 断言确认订单是否请求成功
    promotionAmount = GetKeyword.get_keyword(confirm_order, "promotionAmount")  # 获取返回值中的优惠金额
    payAmount = GetKeyword.get_keyword(confirm_order, "payAmount")  # 获取返回值中的支付金额
    price_1 = payload_1["price"] * payload_1["quantity"]
    price_2 = payload_2["price"] * payload_2["quantity"]  # 只有满减商品才会优惠
    if price_2 >= 500 and price_2 < 1000:
        reduce_price = 50
    elif price_2 >= 1000:
        reduce_price = 120
    else:
        reduce_price = 0
    price = price_1 + price_2 - reduce_price
    pytest.assume(reduce_price == promotionAmount)  # 断言满减金额是否正确
    print(promotionAmount, reduce_price, payAmount, price)
    pytest.assume(price == payAmount)  # 断言支付金额是否正确
    # 生成订单,先创建地址
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大侠",
        "phoneNumber": "121",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    Ident().add_member_address(payload=payload)
    address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    generate_result = Order().generate_order(address_id, 1)
    print(generate_result)
    pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200)
    order_id = GetKeyword.get_keyword(generate_result, "orderId")
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0)  # 断言数据库中订单是否生成且status=0未支付
    cart_sql = """SELECT delete_status FROM oms_cart_item WHERE member_id = 21 AND quantity=%s AND product_sku_id=%s"""
    args_cart_1 = [quantity_1, payload_1["productSkuId"]]
    args_cart_2 = [quantity_2, payload_2["productSkuId"]]
    cart_sql_result_after_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_1)
    cart_sql_result_after_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_2)
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_1, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_2, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    # 回调支付
    pay_result = order.pay_success(order_id=order_id)
    pytest.assume(GetKeyword.get_keyword(pay_result, "code") == 200)
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1)

    sql_result_11 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_1)  # 查询一样的内容,sql可用最初的
    sql_result_22 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_2)  # 查询一样的内容,sql可用最初的
    stock_11 = GetKeyword.get_keyword(sql_result_11, "stock")  # 获取普通商品数量
    stock_22 = GetKeyword.get_keyword(sql_result_22, "stock")  # 获取满减商品数量
    pytest.assume(stock_1 - quantity_1 == stock_11)  # 断言普通商品前后差值等于购买数量
    pytest.assume(stock_2 - quantity_2 == stock_22)  # 断言满减商品前后差值等于购买数量
    print(stock_1, stock_11, stock_2, stock_22)
    # 删除地址
    Ident().delete_member_address(id=address_id)


data_5 = [(1, 1)]


@allure.title("购买普通商品和折扣商品")
@allure.story("购物促销活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantity_1,quantity_2", data_5)
def test_test_order5(quantity_1, quantity_2):
    '''普通商品和折扣商品'''
    # 添加购物车
    payload_1 = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
        "price": 369,
        "productAttr": '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"39"},{"key":"风格","value":"秋季"}]',
        "productBrand": "NIKE",
        "productCategoryId": 29,
        "productId": 35,
        "productName": "耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5b235bb9Nf606460b.jpg",
        "productSkuCode": "202002250035008",
        "productSkuId": 178,
        "productSn": "6799342",
        "productSubTitle": "8耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "quantity": quantity_1
    }
    payload_2 = {
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
        "quantity": quantity_2
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item  WHERE member_id=21"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_1 = [payload_1["productId"], payload_1["productAttr"]]
    args_2 = [payload_2["productId"], payload_2["productAttr"]]
    sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_1)
    sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_2)
    stock_1 = GetKeyword.get_keyword(sql_result_1, "stock")  # 获取普通商品数量
    stock_2 = GetKeyword.get_keyword(sql_result_2, "stock")  # 获取折扣商品数量
    cart_result_1 = Cart().add_cart(payload_1)  # 添加普通商品到购物车
    cart_result_2 = Cart().add_cart(payload_2)  # 添加折扣商品到购物车
    pytest.assume(GetKeyword.get_keyword(cart_result_1, "code") == 200)
    pytest.assume(GetKeyword.get_keyword(cart_result_2, "code") == 200)
    cart_sql = """SELECT * FROM oms_cart_item WHERE member_id = 21 AND delete_status = %s AND quantity=%s AND product_sku_id=%s"""
    cart_args_1 = [0, quantity_1, payload_1["productSkuId"]]
    cart_args_2 = [0, quantity_2, payload_2["productSkuId"]]
    cart_sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_1)
    cart_sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_2)
    pytest.assume(cart_sql_result_1 != None)  # 断言SQL不为空
    pytest.assume(cart_sql_result_2 != None)  # 断言SQL不为空
    # 确认订单
    confirm_order = Order().confirm_order()
    pytest.assume(GetKeyword.get_keyword(confirm_order, "code") == 200)  # 断言确认订单是否请求成功
    promotionAmount = GetKeyword.get_keyword(confirm_order, "promotionAmount")  # 获取返回值中的优惠金额
    payAmount = GetKeyword.get_keyword(confirm_order, "payAmount")  # 获取返回值中的支付金额
    price_1 = payload_1["price"] * quantity_1  # 普通商品的价格
    price_2 = payload_2["price"] * quantity_2  # 只有折扣商品才会优惠
    if quantity_2 == 2:
        promotionAmount_result = round(0.2 * price_2, 1)
        payAmount_result = round(0.8 * price_2, 1) + price_1
    elif quantity_2 >= 3:
        promotionAmount_result = round(0.25 * price_2, 2)
        payAmount_result = round(0.75 * price_2, 2) + price_1
    else:
        promotionAmount_result = 0
        payAmount_result = price_2 + price_1
    pytest.assume(promotionAmount_result == promotionAmount)  # 断言满减金额是否正确
    print(promotionAmount, promotionAmount_result, payAmount, payAmount_result)
    pytest.assume(payAmount_result == payAmount)  # 断言支付金额是否正确
    # 生成订单,先创建地址
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大侠",
        "phoneNumber": "121",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    Ident().add_member_address(payload=payload)
    address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    generate_result = Order().generate_order(address_id, 1)
    print(generate_result)
    pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200)
    order_id = GetKeyword.get_keyword(generate_result, "orderId")
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0)  # 断言数据库中订单是否生成且status=0未支付
    cart_sql = """SELECT delete_status FROM oms_cart_item WHERE member_id = 21 AND quantity=%s AND product_sku_id=%s"""
    args_cart_1 = [quantity_1, payload_1["productSkuId"]]
    args_cart_2 = [quantity_2, payload_2["productSkuId"]]
    cart_sql_result_after_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_1)
    cart_sql_result_after_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_2)
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_1, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_2, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    # 回调支付
    pay_result = Order().pay_success(order_id=order_id)
    pytest.assume(GetKeyword.get_keyword(pay_result, "code") == 200)
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1)

    sql_result_11 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_1)  # 查询一样的内容,sql可用最初的
    sql_result_22 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_2)  # 查询一样的内容,sql可用最初的
    stock_11 = GetKeyword.get_keyword(sql_result_11, "stock")  # 获取普通商品数量
    stock_22 = GetKeyword.get_keyword(sql_result_22, "stock")  # 获取折扣商品数量
    pytest.assume(stock_1 - quantity_1 == stock_11)  # 断言普通商品前后差值等于购买数量
    pytest.assume(stock_2 - quantity_2 == stock_22)  # 断言折扣商品前后差值等于购买数量
    print(stock_1, stock_11, stock_2, stock_22)
    # 删除地址
    Ident().delete_member_address(id=address_id)


data_6 = [(1, 1), (1, 2)]


@allure.title("购买满减商品和折扣商品")
@allure.story("购物促销活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantity_1,quantity_2", data_6)
def test_test_order6(quantity_1, quantity_2):
    ''''满减商品和折扣商品'''
    # 添加购物车
    payload_1 = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
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
        "quantity": quantity_1
    }
    payload_2 = {
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
        "quantity": quantity_2
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item  WHERE member_id=21"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_1 = [payload_1["productId"], payload_1["productAttr"]]
    args_2 = [payload_2["productId"], payload_2["productAttr"]]
    sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_1)
    sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_2)
    stock_1 = GetKeyword.get_keyword(sql_result_1, "stock")  # 获取普通商品数量
    stock_2 = GetKeyword.get_keyword(sql_result_2, "stock")  # 获取折扣商品数量
    cart_result_1 = Cart().add_cart(payload_1)  # 添加普通商品到购物车
    cart_result_2 = Cart().add_cart(payload_2)  # 添加折扣商品到购物车
    pytest.assume(GetKeyword.get_keyword(cart_result_1, "code") == 200)
    pytest.assume(GetKeyword.get_keyword(cart_result_2, "code") == 200)
    cart_sql = """SELECT * FROM oms_cart_item WHERE member_id = 21 AND delete_status = %s AND quantity=%s AND product_sku_id=%s"""
    cart_args_1 = [0, quantity_1, payload_1["productSkuId"]]
    cart_args_2 = [0, quantity_2, payload_2["productSkuId"]]
    cart_sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_1)
    cart_sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_2)
    pytest.assume(cart_sql_result_1 != None)  # 断言SQL不为空
    pytest.assume(cart_sql_result_2 != None)  # 断言SQL不为空
    # 确认订单
    confirm_order = Order().confirm_order()
    pytest.assume(GetKeyword.get_keyword(confirm_order, "code") == 200)  # 断言确认订单是否请求成功
    promotionAmount = GetKeyword.get_keyword(confirm_order, "promotionAmount")  # 获取返回值中的优惠金额
    payAmount = GetKeyword.get_keyword(confirm_order, "payAmount")  # 获取返回值中的支付金额
    price_1 = payload_1["price"] * quantity_1  # 满减商品的价格
    price_2 = payload_2["price"] * quantity_2  # 只有折扣商品才会优惠
    if price_1 >= 500 and price_1 < 1000:
        reduce_price_1 = 50
    elif price_1 >= 1000:
        reduce_price_1 = 120
    else:
        reduce_price_1 = 0
    if quantity_2 == 2:
        reduce_price_2 = 0.2 * price_2
    elif quantity_2 >= 3:
        reduce_price_2 = 0.25 * price_2
    else:
        reduce_price_2 = 0
    reduce_price = round(reduce_price_1 + reduce_price_2, 2)
    price = price_1 + price_2 - reduce_price
    pytest.assume(reduce_price == promotionAmount)  # 断言优惠金额是否正确
    print(promotionAmount, reduce_price, payAmount, price)
    pytest.assume(price == payAmount)  # 断言支付金额是否正确
    # 生成订单,先创建地址
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大侠",
        "phoneNumber": "121",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    Ident().add_member_address(payload=payload)
    address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    generate_result = Order().generate_order(address_id, 1)
    print(generate_result)
    pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200)
    order_id = GetKeyword.get_keyword(generate_result, "orderId")
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0)  # 断言数据库中订单是否生成且status=0未支付
    cart_sql = """SELECT delete_status FROM oms_cart_item WHERE member_id = 21 AND quantity=%s AND product_sku_id=%s"""
    args_cart_1 = [quantity_1, payload_1["productSkuId"]]
    args_cart_2 = [quantity_2, payload_2["productSkuId"]]
    cart_sql_result_after_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_1)
    cart_sql_result_after_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_2)
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_1, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_2, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    # 回调支付
    pay_result = Order().pay_success(order_id=order_id)
    pytest.assume(GetKeyword.get_keyword(pay_result, "code") == 200)
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1)

    sql_result_11 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_1)  # 查询一样的内容,sql可用最初的
    sql_result_22 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_2)  # 查询一样的内容,sql可用最初的
    stock_11 = GetKeyword.get_keyword(sql_result_11, "stock")  # 获取普通商品数量
    stock_22 = GetKeyword.get_keyword(sql_result_22, "stock")  # 获取折扣商品数量
    pytest.assume(stock_1 - quantity_1 == stock_11)  # 断言满减商品前后差值等于购买数量
    pytest.assume(stock_2 - quantity_2 == stock_22)  # 断言折扣商品前后差值等于购买数量
    print(stock_1, stock_11, stock_2, stock_22)
    # 删除地址
    Ident().delete_member_address(id=address_id)


data_7 = [(1, 1, 1), (2, 1, 1), (3, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 1)]


@allure.title("购买满减商品,折扣商品,普通商品")
@allure.story("购物促销活动商品")
@allure.feature("购物流程")
@pytest.mark.parametrize("quantity_1,quantity_2,quantity_3", data_7)
def test_test_order7(quantity_1, quantity_2, quantity_3):
    ''''满减商品和折扣商品'''
    # 添加购物车
    payload_1 = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
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
        "quantity": quantity_1
    }
    payload_2 = {
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
        "quantity": quantity_2
    }
    payload_3 = {
        "createDate": "2021-03-02T00:55:11.724Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 0,
        "memberNickname": "string",
        "modifyDate": "2021-03-02T00:55:11.724Z",
        "price": 369,
        "productAttr": '[{"key":"颜色","value":"蓝色"},{"key":"尺寸","value":"39"},{"key":"风格","value":"秋季"}]',
        "productBrand": "NIKE",
        "productCategoryId": 29,
        "productId": 35,
        "productName": "耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5b235bb9Nf606460b.jpg",
        "productSkuCode": "202002250035008",
        "productSkuId": 178,
        "productSn": "6799342",
        "productSubTitle": "8耐克NIKE 男子 休闲鞋 ROSHE RUN 运动鞋 511881-010黑色41码",
        "quantity": quantity_3
    }
    sql_oms_cart_item = "DELETE FROM oms_cart_item  WHERE member_id=21"
    sql_oms_order = "DELETE FROM oms_order WHERE member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_cart_item)  # 清空购物车
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
             charset="utf8",
             port=3306).execute(sql=sql_oms_order)  # 清空订单
    sql = "SELECT stock from pms_sku_stock WHERE product_id =%s and sp_data=%s"
    args_1 = [payload_1["productId"], payload_1["productAttr"]]
    args_2 = [payload_2["productId"], payload_2["productAttr"]]
    args_3 = [payload_3["productId"], payload_3["productAttr"]]
    sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_1)
    sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_2)
    sql_result_3 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                            charset="utf8",
                            port=3306).fetchone(sql=sql, args=args_3)
    stock_1 = GetKeyword.get_keyword(sql_result_1, "stock")  # 获取普通商品数量
    stock_2 = GetKeyword.get_keyword(sql_result_2, "stock")  # 获取折扣商品数量
    stock_3 = GetKeyword.get_keyword(sql_result_3, "stock")  # 获取折扣商品数量
    cart_result_1 = Cart().add_cart(payload_1)  # 添加满减商品到购物车
    cart_result_2 = Cart().add_cart(payload_2)  # 添加折扣商品到购物车
    cart_result_3 = Cart().add_cart(payload_3)  # 添加普通商品到购物车
    pytest.assume(GetKeyword.get_keyword(cart_result_1, "code") == 200)
    pytest.assume(GetKeyword.get_keyword(cart_result_2, "code") == 200)
    pytest.assume(GetKeyword.get_keyword(cart_result_3, "code") == 200)
    cart_sql = """SELECT * FROM oms_cart_item WHERE member_id = 21 AND delete_status = %s AND quantity=%s AND product_sku_id=%s"""
    cart_args_1 = [0, quantity_1, payload_1["productSkuId"]]
    cart_args_2 = [0, quantity_2, payload_2["productSkuId"]]
    cart_args_3 = [0, quantity_3, payload_3["productSkuId"]]
    cart_sql_result_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_1)
    cart_sql_result_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_2)
    cart_sql_result_3 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                 charset="utf8",
                                 port=3306).fetchone(sql=cart_sql, args=cart_args_3)
    pytest.assume(cart_sql_result_1 != None)  # 断言SQL不为空
    pytest.assume(cart_sql_result_2 != None)  # 断言SQL不为空
    pytest.assume(cart_sql_result_3 != None)  # 断言SQL不为空
    # 确认订单
    confirm_order = Order().confirm_order()
    pytest.assume(GetKeyword.get_keyword(confirm_order, "code") == 200)  # 断言确认订单是否请求成功
    promotionAmount = GetKeyword.get_keyword(confirm_order, "promotionAmount")  # 获取返回值中的优惠金额
    payAmount = GetKeyword.get_keyword(confirm_order, "payAmount")  # 获取返回值中的支付金额
    price_1 = payload_1["price"] * quantity_1  # 满减商品的价格
    price_2 = payload_2["price"] * quantity_2  # 折扣商品优惠
    price_3 = payload_3["price"] * quantity_3  # 普通商品价格
    if price_1 >= 500 and price_1 < 1000:
        reduce_price_1 = 50
    elif price_1 >= 1000:
        reduce_price_1 = 120
    else:
        reduce_price_1 = 0
    if quantity_2 == 2:
        reduce_price_2 = 0.2 * price_2
    elif quantity_2 >= 3:
        reduce_price_2 = 0.25 * price_2
    else:
        reduce_price_2 = 0
    reduce_price = round(reduce_price_1 + reduce_price_2, 2)
    price = price_1 + price_2 + price_3 - reduce_price
    pytest.assume(reduce_price == promotionAmount)  # 断言优惠金额是否正确
    print(promotionAmount, reduce_price, payAmount, price)
    pytest.assume(price == payAmount)  # 断言支付金额是否正确
    # 生成订单,先创建地址
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大侠",
        "phoneNumber": "121",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    Ident().add_member_address(payload=payload)
    address_id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    generate_result = Order().generate_order(address_id, 1)
    print(generate_result)
    pytest.assume(GetKeyword.get_keyword(generate_result, "code") == 200)
    order_id = GetKeyword.get_keyword(generate_result, "orderId")
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 0)  # 断言数据库中订单是否生成且status=0未支付
    cart_sql = """SELECT delete_status FROM oms_cart_item WHERE member_id = 21 AND quantity=%s AND product_sku_id=%s"""
    args_cart_1 = [quantity_1, payload_1["productSkuId"]]
    args_cart_2 = [quantity_2, payload_2["productSkuId"]]
    args_cart_3 = [quantity_3, payload_3["productSkuId"]]
    cart_sql_result_after_1 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_1)
    cart_sql_result_after_2 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_2)
    cart_sql_result_after_3 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104",
                                       user="root",
                                       charset="utf8",
                                       port=3306).fetchone(sql=cart_sql, args=args_cart_3)
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_1, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_2, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    pytest.assume(GetKeyword.get_keyword(cart_sql_result_after_3, "delete_status") == 1)  # 断言购物车表中记录状态是否删除
    # 回调支付
    pay_result = Order().pay_success(order_id=order_id)
    pytest.assume(GetKeyword.get_keyword(pay_result, "code") == 200)
    order_sql = """SELECT `status` FROM oms_order where id=%s;"""
    order_sql_result = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                                charset="utf8",
                                port=3306).fetchone(sql=order_sql, args=order_id)
    pytest.assume(GetKeyword.get_keyword(order_sql_result, "status") == 1)

    sql_result_11 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_1)  # 查询一样的内容,sql可用最初的
    sql_result_22 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_2)  # 查询一样的内容,sql可用最初的
    sql_result_33 = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root",
                             charset="utf8",
                             port=3306).fetchone(sql=sql, args=args_3)  # 查询一样的内容,sql可用最初的
    stock_11 = GetKeyword.get_keyword(sql_result_11, "stock")  # 获取普通商品数量
    stock_22 = GetKeyword.get_keyword(sql_result_22, "stock")  # 获取折扣商品数量
    stock_33 = GetKeyword.get_keyword(sql_result_33, "stock")  # 获取折扣商品数量
    pytest.assume(stock_1 - quantity_1 == stock_11)  # 断言满减商品前后差值等于购买数量
    pytest.assume(stock_2 - quantity_2 == stock_22)  # 断言折扣商品前后差值等于购买数量
    pytest.assume(stock_3 - quantity_3 == stock_33)  # 断言折扣商品前后差值等于购买数量
    print(stock_1, stock_11, stock_2, stock_22, stock_3, stock_33)
    # 删除地址
    Ident().delete_member_address(id=address_id)


if __name__ == '__main__':
    pytest.main()
