# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/19 10:48
@Author  : cody
@File    : conftest.py

'''
import os
import logging
import time

import pytest
import warnings
from datetime import datetime

from config.setting import LOG_PATH, ENVIRONMENT_TEST, Token_PATH, Get_TokenData
from utils.TimeFormat import get_local_time
from py.xml import html

warnings.filterwarnings("ignore")  # 忽略 UserWarning


def touchLogFile():
    """创建测试运行log文件，供Text控件实时读取,运行在主进程"""
    # log_path = makeDir(dirName=nameDir)  # 日志目录
    log_file_name = os.path.join(LOG_PATH,
                                 '%s_log.log' %
                                 (get_local_time()))
    with open(log_file_name, 'w', encoding='utf-8') as f:
        f.flush()
    return log_file_name


@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    # 初始化 logger，设置日志级别为 info
    logger = logging.getLogger()
    logger.setLevel(level_relations.get('info'))

    # global token
    log_file = touchLogFile()

    # 定义日志格式和文件 handler
    formatter = logging.Formatter(
        f'%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d- %(levelname)s: %(message)s')
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 将文件handler添加到logger
    logger.addHandler(file_handler)

    yield

    # 在测试结束后移出文件 handler
    logger.removeHandler(file_handler)


# 报告优化
def pytest_html_report_title(report):
    report.title = "Automation Test Report Title!"


def pytest_configure(config):
    # print("cody",config._metadata)
    # 给环境表添加时间
    config._metadata['StartTime'] = get_local_time()
    config._metadata['Project_Environment'] = ENVIRONMENT_TEST
    # config._metadata['Base URL'] = ENVIRONMENT_TEST
    # 将环境表 移出 Packages和Plugins
    config._metadata.pop('Packages')
    config._metadata.pop('Plugins')


def pytest_html_results_summary(prefix, summary, postfix):
    #  追加的内容
    prefix.extend([html.p("Tester: cody")])



def pytest_html_results_table_header(cells):
    """
    处理结果表的表头
    """
    # 往表格增加一列Description，并且给Description列增加排序
    cells.insert(2, html.th("Description", class_="sortable desc", col="desc"))
    # 往表格增加一列Time，并且给Time列增加排序
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    # 移除表格最后一列
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """
    处理结果表的行
    """

    # 往列 Description插入每行的值
    cells.insert(2, html.th(report.description))
    # 往列 Time 插入每行的值
    cells.insert(1, html.th(datetime.now(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 定义列 Description的值，默认为测试方法的文档注释，如果测试方法没有文档注释，就自定义Description的值
    if str(item.function.__doc__) != "None":
        # 结果表的description列的值 = 测试方法的文档注释
        report.description = str(item.function.__doc__)
    else:
        # 结果表的description列的值 = 自定义的信息
        # 注意：这里可以将测试用例中的用例标题或者描述作为列 Description的值
        report.description = "The content described here"


if __name__ == '__main__':
    # print(get_local_time())
    # print(touchLogFile())
    logging.info('testqsgou  1 == 1')
    print(datetime.utcnow())
    print(datetime.now())
