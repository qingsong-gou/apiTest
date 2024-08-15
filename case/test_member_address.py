import pytest
from interface.IndentInterface import Ident


def test_member_address_1():
    '''
    查询别人的地址id=11
    :return:
    '''
    result = Ident().member_address(id=11)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")


if __name__ == '__main__':
    pytest.main()
