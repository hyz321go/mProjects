# -*- coding: utf-8 -*-
# author： hyz321go
# IDE： PyCharm
# File ：mylibs.py
# datetime： 2022/10/5 21:04

import time

# 返回一个13位的时间戳，格式为字符串
def get_time():
    time_data = int(time.time() * 1000)
    # print(time_data)
    return str(time_data)

# get_time()