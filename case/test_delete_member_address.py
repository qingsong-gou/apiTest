import pytest
from interface.IndentInterface import Ident


def test_delete_member_address():
    '''
    删除别人的收获地址id=100
    :return:
    '''
    result = Ident().delete_member_address(id=100)
    pytest.assume(result["status_code"] == 200, "断言状态码")
    pytest.assume(result["body"]["code"] != 200, "断言开发自检字段")
    # pytest.assume(result['response_time'] < 300, "响应时间超过300毫秒,不合格")


if __name__ == '__main__':
    pytest.main()
