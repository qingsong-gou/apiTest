import pytest
from interface.IndentInterface import Ident


def test_list_member_address():
    '''
    没添加地址时,查询收货地址
    :return:
    '''
    result = Ident().list_member_address()
    print(result)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] == 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")
    pytest.assume(result["body"]["data"] == [], "没有地址时,查询出地址了")


if __name__ == '__main__':
    pytest.main()
