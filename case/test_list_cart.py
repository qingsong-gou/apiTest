import pytest
from interface.CartInterface import Cart


def test_list_cart_1():
    '''
    没有商品时,查询
    :return:
    '''
    result = Cart().list_cart()  # 获取购物车列表
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    pytest.assume(result["body"]["data"] == [], "购物车没添加商品时,能够查处商品")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
