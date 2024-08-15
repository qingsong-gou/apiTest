'''
jsonpath三方包
'''
import jsonpath


class GetKeyword(object):
    @staticmethod
    def get_keyword(data, keyword):
        '''
        通过关键字获取对应的值,若有多个,默认获取第一个
        :param data: 元数据
        :param keyword: 关键字
        :return:
        '''
        try:
            return jsonpath.jsonpath(data, f"$..{keyword}")[0]
        except:
            print("关键字不存在!!!")
            return False

    @staticmethod
    def get_keywords(data, keyword):
        '''
        通过关键字获取对应的所有值
        :param data:
        :param keyword:
        :return:
        '''
        if jsonpath.jsonpath(data, f"$..{keyword}"):  # 不存在会返回None
            return jsonpath.jsonpath(data, f"$..{keyword}")
        else:
            print("关键字不存在!!!")
            return False


if __name__ == '__main__':
    data = {
        "status": 10200,
        "message": "success",
        "data": {
            "eid": 1,
            "name": "小米7发布会",
            "limit": 2000,
            "status": "true",
            "address": "北京",
            "start_time": "2018-01-30T14:00:00"
        },
        "name": "小米10发布会"
    }
    res = GetKeyword.get_keywords(data=data, keyword="name")
    print(res)  # ['小米10发布会', '小米7发布会']
    res_2 = GetKeyword.get_keyword(data=data, keyword="name")
    print(res_2)  # 小米10发布会
