# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/18 14:49
@Author  : cody
@File    : setting.py

'''

import os

# 获取项目路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 项目运行环境路径
Env_Path = os.path.join(BASE_PATH, 'apiTestEnv\\Scripts\\')
# 定义测试用例的路径
TESTCASE_PATH = os.path.join(BASE_PATH, 'testcase\\')
# 定义测报告的路径
REPORT_PATH = os.path.join(BASE_PATH, 'report\\')
REPORT_STYLE_PATH = os.path.join(BASE_PATH, 'config\\report.css')
# 定义日志文件的路径
LOG_PATH = os.path.join(BASE_PATH, 'logs\\')
# 定义数据文件的路径
EXCEL_DATA_PATH = os.path.join(BASE_PATH, 'data\\caseExcelData\\')
CSV_DATA_PATH = os.path.join(BASE_PATH, 'data\\caseCsvData\\')
Env_DATA_PATH = os.path.join(BASE_PATH, 'data\\caseEnvData\\')
# 定义Token配置文件路径
Token_PATH = os.path.join(BASE_PATH, 'config\\TokenData.csv')
# 请求login接口参数获取token
Get_TokenData = {"bs": "123456"}

# 切换项目环境，测试，线上，预发布环境等
ENVIRONMENT_TEST = "https://www.baidu.com"

# mysql数据库的连接信息
# p=pymysql.connect(host=DB_IP,user=USER,password=DB_PASSWORD,database=DB_NAME,charset=CHARSET,port=PORT)
M_DB_NAME = 'database'
M_DB_PASSWORD = 'root'
M_DB_IP = '127.0.0.1'
M_DB_PORT = 3306
M_DB_USER = "root"
M_DB_CHARSET = "utf-8"

# redis数据库的连接信息
# r = redis.Redis(host='127.0.0.1',port=6379,db=0,password='root')
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
db = 0
REDIS_PASSWORD = 'root'

# 发邮件账户
Send_Email_Account = "cody@abcg.email"
Authorization = "ljud mwxw imyq eqeb"
# 收件人
Receiver_To = ["cody@abcg.email"]
# 抄送人
Receiver_Cc = ["cody@abcg.email"]

# print(LOG_PATH)
