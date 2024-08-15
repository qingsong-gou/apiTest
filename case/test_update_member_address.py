import pytest

from interface.IndentInterface import Ident
from utils.GetKeyword import GetKeyword
from utils.Database import Database


def test_update_member_address_1():
    '''
    修改收货地址信息region为空
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "1231",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"region": ""}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_update_member_address_2():
    '''
    修改别人的收货地址信息 id=27
    :return:
    '''
    address = {"postCode": 600000}
    result = Ident().update_member_address(id=27, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")


def test_update_member_address_3():
    '''
    修改收货地址信息detail_address为空
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "路易大地",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "12312311234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"detailAddress": ""}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_update_member_address_4():
    '''
    修改收货地址信息,添加name
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "路易大地",
        "id": 0,
        "memberId": 0,
        "name": "",
        "phoneNumber": "12312311234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"name": "轻松大虾2"}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select name from ums_member_receive_address where member_id=21 and phone_number='12312311234'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的信息
    pytest.assume(res["name"] == "轻松大虾2", "修改后的收货信息与数据库不一致,修改失败")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_update_member_address_5():
    '''
    修改收货地址信息phone_number为不正确号码
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "路易大地",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "12312311234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"phoneNumber": "1231234"}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_update_member_address_6():
    '''
    修改收货地址信息post_code为不正确
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "路易大地",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "12312311234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"postCode": ""}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_update_member_address_7():
    '''
    修改收货地址信息default_status为10
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "路易大地",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "12312311234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"defaultStatus": "10"}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_update_member_address_8():
    '''
    修改收货地址信息member_id为其他10
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "路易大地",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "12312311234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    Ident().add_member_address(payload=payload)
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"memberId": "10"}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=10"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


if __name__ == '__main__':
    pytest.main()
