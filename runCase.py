# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/18 14:41
@Author  : cody
@File    : runCase.py

'''
import os
import time

import pytest

from config.setting import REPORT_PATH, REPORT_STYLE_PATH, Env_Path
from utils.SendEmail import send_email
from utils.TimeFormat import get_local_time

if __name__ == '__main__':
    # activate = Env_Path + "activate.bat"
    # deactivate = Env_Path + "deactivate.bat"
    #
    # os.system("cmd.exe /c "+activate)
    # print(50 * "*")
    # pytest.main(
    #     [f'--html={REPORT_PATH}{get_local_time()}_report.html', f'--css={REPORT_STYLE_PATH}'])
    # os.system("cmd.exe /c "+deactivate)

    htmlName = REPORT_PATH + get_local_time() + "_report.html"
    pytest.main(
        [f'--html={htmlName}', f'--css={REPORT_STYLE_PATH}'])
    url_report = "www.baidu.com"
    send_email(htmlName, url_report, test_type='自动化')
