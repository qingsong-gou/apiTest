from interface.IndentInterface import Ident
import pytest
from utils.GetKeyword import GetKeyword
from utils.Database import Database


def test_add_member_address():
    '''
    添加收货地址
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
    result = Ident().add_member_address(payload=payload)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select * from ums_member_receive_address where member_id=21 and name='轻松大虾2'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)
    pytest.assume(res is not None, "数据库不能查找到添加的数据")


def test_list_member_address():
    '''
    查询所有收货地址
    :return:
    '''
    result = Ident().list_member_address()
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    print(GetKeyword.get_keyword(result, "name"))
    pytest.assume(GetKeyword.get_keyword(result, "name") == "轻松大虾2", "添加的不是名字为 轻松大虾2 的收货地址")
    sql = "select * from ums_member_receive_address where member_id=21 and name='轻松大虾2'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的信息
    pytest.assume(res is not None, "数据库中不存在收货地址为 轻松大虾2 的地址")


def test_member_address():
    '''
    根据id查看收货信息
    :return:
    '''
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    result = Ident().member_address(id=id)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select * from ums_member_receive_address where member_id=21 and name='轻松大虾2'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的信息
    data = GetKeyword.get_keyword(result, "data")  # memberId与member_id不同,对比值
    li = [data[i] for i in data]  # 取出值
    lis = [res[i] for i in res]  # 取出值
    pytest.assume(li == lis, "数据库中的数据与获取到的收货信息不一致")


def test_update_member_address():
    '''
    修改收货地址信息
    :return:
    '''
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    address = {"postCode": 600000}
    result = Ident().update_member_address(id=id, address=address)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select post_code from ums_member_receive_address where member_id=21 and name='轻松大虾2'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的信息
    pytest.assume(res["post_code"] == "600000", "修改后的收货信息与数据库不一致,修改失败")


def test_delete_member_address():
    '''
    根据ums_member_receive_address表中的id删除收货地址
    :return:
    '''
    id = GetKeyword.get_keyword(Ident().list_member_address(), "id")
    result = Ident().delete_member_address(id=id)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    sql = "select * from ums_member_receive_address where member_id=21 and name ='轻松大虾2'"
    res = Database(password="itsource.cn..", database="03_mall", host="139.159.146.104", user="root", charset="utf8",
                   port=3306).fetchone(sql=sql)  # 获取数据库中的信息
    pytest.assume(res is None, "删除后数据库还能查出该条收货信息,删除失败")


if __name__ == '__main__':
    pytest.main()
