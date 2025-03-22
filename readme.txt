环境处理：
1,项目环境，python 3.7.4，依赖包 requirements.txt,依赖环境apiTestEnv（activate/deactivate）
2.优化report里面的title
去除html里面的 Base Url 方法，修改源码：pytest-base-url中的plugin.py
def pytest_configure(config):
    if hasattr(config, "workerinput"):
        return  # don't run configure on xdist worker nodes
    base_url = config.getoption("base_url") or config.getini("base_url")
    if base_url is not None and base_url != '':
        config.option.base_url = base_url
        if hasattr(config, "_metadata"):
            config._metadata["Base URL"] = base_url
3.保存csv文件时，需要注意utf-8格式

用例书写：
1，config/ApiBaseInfo.py 添加基础接口信息
2，interface下面创建接口py文件，将同一类型接口封装至class，每一个interface里面需要log.info
3，data目录下创建测试用例数据csv或excel，caseEnvData下面创建环境前后置数据，并在caseData下面创建用例数据py文件，并获取用例数据
4，testcase目录下创建以test开头的py文件，在里面引用 data/caseData 里面的用例数据和环境数据，并编写测试用例类

待处理项：
testcase/conftest.py文件中需要调试getToken函数获取token
/utils/database.py文件中需要调试数据库连接以及用例前后置数据处理