import pytest
from interface.IndentInterface import Ident
from utils.Database import Database


def test_add_member_address_1():
    '''
    添加地址,不填名字
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "",
        "phoneNumber": "13288881234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select * from ums_member_receive_address where member_id=21 and phone_number='13288881234'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)
    pytest.assume(res is not None, "数据库不能查找到添加的数据")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_8():
    '''
    添加地址,名字存在不和谐词
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "傻逼",
        "phoneNumber": "13288881234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_2():
    '''
    添加地址,不填电话
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_3():
    '''
    添加地址,不填邮编
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "13288881234",
        "postCode": "",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select * from ums_member_receive_address where member_id=21 and phone_number='13288881234'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)
    pytest.assume(res is not None, "数据库不能查找到添加的数据")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_4():
    '''
    添加地址,不填city,province,region中的region
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "13288881234",
        "postCode": "610000",
        "province": "四川省",
        "region": ""
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_5():
    '''
    添加地址,填city,province,region中的region实际不存在的
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "晋阳街道",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "13288881234",
        "postCode": "610000",
        "province": "四川省",
        "region": "巴州区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_6():
    '''
    添加地址,不填 detailAddress
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "13288881234",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


def test_add_member_address_7():
    '''
    添加地址,号码不正确的
    :return:
    '''
    payload = {
        "city": "成都市",
        "defaultStatus": 0,
        "detailAddress": "中央花园3期",
        "id": 0,
        "memberId": 0,
        "name": "轻松大虾2",
        "phoneNumber": "132",
        "postCode": "610000",
        "province": "四川省",
        "region": "武侯区"
    }
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql_ums_member_receive_address = "delete from ums_member_receive_address where member_id=21"
    Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
             port=3306).execute(sql=sql_ums_member_receive_address)


if __name__ == '__main__':
    pytest.main()
