# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:15
# @Author  :
from admin_account.dbinfo import dbinfo_select_global_configuration
from dfs.dbinfo import get_management_configuration
import requests
import hashlib
import time
import uuid
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

class dfs_api:
    def __init__(self):
        management_configuration = get_management_configuration()
        self.dfs_api = management_configuration.get("dfs_api","")
        self.dfs_manager = management_configuration.get("dfs_manager", "")
        self.dfs_group = management_configuration.get("dfs_group", "")
        self.Basic_authority = management_configuration.get("Basic_authority", "")
        self.AD_time = management_configuration.get("AD_time", "")
        mysqlallvalue = dbinfo_select_global_configuration()
        if mysqlallvalue:
            mysqlallvalue = mysqlallvalue[0]
            self.addomain = str(mysqlallvalue['ad_domain'])
            self.exdomain = str(mysqlallvalue['ex_domain'])
            self.dict = setkey()
            self.signature = self.dict.get("signature",'')
            self.timestamp = self.dict.get("timestamp", '')
            self.nonce = self.dict.get("nonce", '')

    def postapi(self, projectname, **kwargs):
        try:
            kwargs['domain'] = self.addomain
            kwargs['signature'] = self.signature
            kwargs['timestamp'] = self.timestamp
            kwargs['nonce'] = self.nonce
            kwargs['tokenid'] = '200'
            apiurl = requests.post(self.dfs_api + projectname+"/", data=kwargs)
            apidata = apiurl.json()
            return apidata
        except Exception as e:
            return {"isSuccess": False, "message": "连接接口报错:"+str(e)}


# print(dfs_api().postapi("dfs_api_test"))