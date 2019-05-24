# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 15:50
# @Author  :
# {"status":0, "message": {"id":"1","username":"测试","displayname":"测试","types":"测试","applytype":"测试","applydetail":"测试"}}
#传入值
import requests
import uuid,json
from django.shortcuts import HttpResponse
from dfs.dbinfo import get_api

# 流程传入值
from logmanager.views import logmanager


def process_outgoing(value):
    try:
        process = get_api("process")
        if process:
            url = process.get("mess",'')
            value = json.dumps(value)
            headers = {
                "Content-Type": "application/json"
            }
            r = requests.post(url, data=value, headers=headers)
            # r = requests.post(url, data=value)
            resultinfo = r.json()
            # resultinfo = {"status": 0, "message": ""}
            # return resultinfo
        else:
            resultinfo = {"status": -1, "message": "没有这个接口"}
    except Exception as e:
        resultinfo = {"status":-1,"message":str(e)}
    if resultinfo["status"] != 0:
        logmanager().log(returnid=2, username='process', ip='process', message="process_outgoing,流程传入值接口：", issuccess=0, methodname=str(resultinfo), returnparameters=str(value),
                         types="process")
    else:
        logmanager().log(returnid=0, username='process', ip='process', message="process_outgoing,流程传入值接口：", issuccess=0, methodname=str(resultinfo), returnparameters=str(value),
                         types="process")
    return resultinfo



# # 流程传入值
# def process_incoming(request):
#     try:
#         ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
#         status = request.POST.get('status', '')  # status 3 同意，其他不同意
#         types = request.POST.get('types', '')
#         id = request.POST.get('id', '')
#         respjson = {'isSuccess': True, "message": "接口测试通过"}
#     except Exception as e:
#         respjson = {'isSuccess': False, "message": "接口测试不通过：" + str(e)}
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     response.write(json.dumps(respjson, ensure_ascii=False))
#     return response
