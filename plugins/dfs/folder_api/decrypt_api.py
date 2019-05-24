#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from django.http import HttpResponse
import json
from functools import  wraps
import time
import hashlib


#过期时间
expires_time = 600

def auth_api_vaild(data):
    try:
        encryption = data['signature']
        timestamp = data['timestamp']
        nonce = data['nonce']
        if nonce and timestamp and nonce:
            #根据用户传过来的clientid获取WEBAPI_TOKEN
            WEBAPI_TOKEN = "FdffG$#@%^sd@2018@)!*0806"
            if expires_time != 0:
                timestamp = int(timestamp)
                if (int(time.time()) - timestamp) > expires_time:
                    return False
                timestamp = str(timestamp)
            tmp_list = [WEBAPI_TOKEN, timestamp, nonce]
            tmp_list.sort()
            tmp_str = "%s%s%s" % tuple(tmp_list)
            str_key = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
            if str_key == encryption:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
    return False


# Post方法获取加密key
def api_auth_post(func):
    @wraps(func)
    def wrapper(self,request):
        timestamp = self.request.POST.get('timestamp', None)
        nonce = self.request.POST.get('nonce', None)
        signature = self.request.POST.get('signature', None)
        #ip = request.META.get('HTTP_X_FORWARDED_FOR',self.request.META['REMOTE_ADDR'])
        securty_key = {'timestamp': timestamp,'nonce': nonce,'signature': signature}
        if not securty_key:
            respjson = {'message': '接口传入的值错误！', 'isSuccess': False,'code':1}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(respjson,ensure_ascii=False))
            return response
        if not auth_api_vaild(securty_key):
            respjson = {'message': '接口没有权限！or 传入值错误！', 'isSuccess': False,'code':2}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(respjson,ensure_ascii=False))
            return response
        return func(self,request)
    return wrapper


def setkey():
    WEBAPI_TOKEN = "FdffG$#@%^sd@2018@)!*0806"
    timestamp = str(int(time.time()))
    nonce = uuid.uuid1().hex
    tmp_list = [WEBAPI_TOKEN, timestamp, nonce]
    tmp_list.sort()
    tmp_str = "%s%s%s" % tuple(tmp_list)
    signature = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
    dict = {"signature": signature, "timestamp": timestamp, "nonce": nonce}
    return dict

# print(setkey())