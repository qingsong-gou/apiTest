# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/19 11:00
@Author  : cody
@File    : TimeFormat.py

'''
import time


def get_local_time():
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    return mytime


def get_local_date():
    tformat = '%Y %m %d %H:%M:%S'
    mytime = time.strftime(tformat, time.localtime())
    return mytime


if __name__ == '__main__':
    print(get_local_date())
    print(get_local_time())
