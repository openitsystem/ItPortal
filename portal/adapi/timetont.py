#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 10:43
# @Author  : Center
import datetime
import time

def getnttime(day):
    now = datetime.datetime.now() + datetime.timedelta(days=day)
    mintime = time.mktime(now.timetuple())
    namintime = int(mintime + 11644473600)
    nowTime = lambda: int(round(namintime * 10000000))
    return nowTime()



# def getnttime(day):
#     now = day
#     print(now)
#     mintime = time.mktime(now.timetuple())
#     namintime = int(mintime + 11644473600)
#     nowTime = lambda: int(round(namintime * 10000000))
#     return nowTime()
#
