#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import urllib
import uuid
from urllib import request, parse
import json
import datetime
import requests

from Thr.sendmessage import Send_message_thr
from adapi.dbinfo import insert_interface_c_log, getmangerapi, genmangemessage, genmangemessageshow, genmangehow
from admin_account.dbinfo import dbinfo_select_global_configuration

def admd5():
    mysqlallvalue = dbinfo_select_global_configuration()[0]
    skey = mysqlallvalue['skey']
    return skey


def iisservertest(ip,port,**kwargs):
    try:
        allurl = 'http://'+ip+':'+port+'/api/Adapi/OnLineTest'
        kwargs['skey'] = admd5()
        u = requests.get(allurl,params=kwargs)
        data = u.json()
        return  True
    except Exception as e:
        return  False


def serverip_new():
    mysqlallvalue = dbinfo_select_global_configuration()[0]
    iisip = str(mysqlallvalue['iis_ip'])
    iisport = str(mysqlallvalue['iis_port'])
    ipvalue = 'http://'+iisip+':'+iisport+'/api/Adapi/'
    return ipvalue

def serverip():
    #ipvalue = 'http://localhost:55823/api/adapi/'
    try:
        mysqlallvalue = dbinfo_select_global_configuration()[0]
        iisip = str(mysqlallvalue['iis_ip'])
        iisport = str(mysqlallvalue['iis_port'])
        ipvalue = 'http://' + iisip + ':' + iisport + '/api/Adapi/'
    except Exception as e:
        ipvalue = '没有获取到url'
    return ipvalue



class adapi:
    def __init__(self):
        mysqlallvalue = dbinfo_select_global_configuration()[0]
        self.iisip = 'http://'+str(mysqlallvalue['iis_ip'])+':'+str(mysqlallvalue['iis_port'])+'/api/Adapi/'
        self.testiisip = 'http://localhost:22238/api/Adapi/'
        self.addomain = str(mysqlallvalue['ad_domain'])
        self.exdomain = str(mysqlallvalue['ex_domain'])
        self.skey = admd5()

    def Initialapi(self,projectname,**kwargs):
        try:
            kwargs['domain'] = self.addomain
            kwargs['skey'] = self.skey
            apiurl = requests.get(self.iisip+projectname, params=kwargs)
            apidata = apiurl.json()
            return  apidata
        except Exception as e:
            return False


    def Initialapi_noskey(self,projectname,**kwargs):
        try:
            kwargs['domain'] = self.addomain
            apiurl = requests.get(self.iisip+projectname, params=kwargs)
            apidata = apiurl.json()
            return  apidata
        except Exception as e:
            return False

    def postapi(self, projectname, **kwargs):
        try:
            kwargs['domain'] = self.addomain
            kwargs['skey'] = self.skey
            apiurl = requests.post(self.iisip + projectname, data=kwargs)
            apidata = apiurl.json()
            return apidata
        except Exception as e:
            return False

    def testapi(self, projectname, **kwargs):
        try:
            kwargs['skey'] = self.skey
            apiurl = requests.get(self.iisip + projectname, params=kwargs)
            apidata = apiurl.json()
            return apidata
        except Exception as e:
            return False



def adlinktestvalue(method,**kwargs):
    try:
        urlvalue = serverip_new()
        methodvalue = str(method)
        r = requests.get(urlvalue+methodvalue, params=kwargs)
        a = r.json()
        if a['isSuccess']:
            pass
        return True
    except Exception as e:
        return True

# (2)根据对象类别新建对象
def Createobject(objects,oudn,objectClass,domain,sn=None,displayName=None,wWWHomePage=None,password=None,guid=None,tokenid=None,ip=None):
    '''
    (32)根据对象类别新建对象
    :param objects:
    :param oudn:  oudn = 'OU=xx,OU=xx,DC=test,DC=cn'
    :param objectClass: 'user','group','organizationalUnit','computer'
    :param sn:
    :param displayName:
    :param wWWHomePage:
    :param password:
    :return: {'message': {'message': ''}, 'isSuccess': True}
    '''
    ipvalue = serverip()
    url=ipvalue+'Createobject'
    value = {
        "objects": objects,
        "oudn": oudn,
        "objectClass":objectClass,
        "domain": domain,
        "sn": sn,
        "displayName": displayName,
        "wWWHomePage": wWWHomePage,
        "password": password,
        "guid": guid,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']),  str(tokenid), 'Createobject', str(respjson), str(value))
    return respjson


# 1.判断AD域中是否有这个对象
def ObjectExist(objectName,catalog,domain,tokenid=None,ip=None):
    '''
    :param objectName:
    :param catalog:   'user','group','organizationalUnit','computer'
    :return:  True
    '''
    ipvalue = serverip()
    url=ipvalue+'ObjectExists'
    value = {
        "objectName": objectName,
        "catalog": catalog,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    return respjson


# 判断是否存在AD  ObjectExistAD
def ObjectExistADs(objectName,domain,tokenid=None,ip=None):
    '''
    :param objectName:
    :param catalog:   'user','group','organizationalUnit','computer'
    :return:  True
    '''
    ipvalue = serverip()
    url=ipvalue+'ObjectExistAD'
    value = {
        "objectName": objectName,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson), str(tokenid), 'ObjectExistAD', str(respjson), str(value))
    return respjson

# 1.判断AD域中是否有这个对象,限制OU
def ObjectExistsOU(objectName,catalog,ouname,domain,tokenid=None,ip=None):
    '''
    :param objectName:
    :param catalog:   'user','group','organizationalUnit','computer'
    :return:  True
    '''
    ipvalue = serverip()
    url=ipvalue+'ObjectExistsOU'
    value = {
        "objectName": objectName,
        "catalog": catalog,
        "ouname": ouname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson), str(tokenid), 'ObjectExistsOU', str(respjson), str(value))
    return respjson



#(3)根据对象类别查询属性
def GetobjectProperty(objects,catalog,domain,tokenid=None,ip=None):
    '''
    :param objects:
    :param catalog: 'user','group','organizationalUnit','computer'
    :return:
    '''
    ipvalue = serverip()
    url = ipvalue + 'GetobjectProperty'
    value = {
        "objects": objects,
        "objectClass": catalog,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetobjectProperty', str(respjson), str(value))
    return respjson



#(6)密码重置
def ResetPasswordByOU(username,newpassword,domain,tokenid=None,ip=None):
    '''

    :param username:
    :param newpassword:
    :return: {'isSuccess': True, 'message': {'newpassword': 'tX$7wM#3', 'message': 。'}}
    '''
    ipvalue = serverip()
    url = ipvalue + 'ResetPasswordByOU'

    value = {
        "username": username,
        "newpassword": newpassword,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'ResetPasswordByOU', str(respjson), str(value))
    return respjson



#(6)user密码修改
def ChangePassword(username,oldpassword,newpassword,domain,tokenid=None,ip=None):
    '''

    :param username:
    :param oldpassword:
    :param newpassword:
    :return: {'isSuccess': True, 'message': '。'}
    '''
    ipvalue = serverip()
    url = ipvalue + 'ChangePassword'

    value = {
        "username": username,
        "oldpassword": oldpassword,
        "newpassword": newpassword,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'ChangePassword', str(respjson), str(value))
    return respjson


#(5)修改用户属性
def SetuserProperty(username,PropertyName,PropertyValue,domain,tokenid=None,ip=None):
    '''

    :param username:
    :param PropertyName:
    :param PropertyValue:
    :return: {'message': {'message': 'wifitest1的sn属性，修改成功'}, 'isSuccess': True}
    ChangePassword('wifitest1','userAccountControl',514)
    '''
    ipvalue = serverip()
    url = ipvalue + 'SetuserProperty'

    value = {
        "username": username,
        "PropertyName": PropertyName,
        "PropertyValue": PropertyValue,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'SetuserProperty', str(respjson), str(value))
    return respjson


#(7)根据对象类别移动到新OU
def MoveToObject(objects,oudn,objectClass,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'MoveToObject'
    value = {
        "objects": objects,
        "oudn": oudn,
        "objectClass": objectClass,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'MoveToObject', str(respjson), str(value))
    return respjson


#(8)将用户加入到用户组中
def AddUserToGroup(sAMAccountName,groupname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'AddUserToGroup'
    value = {
        "sAMAccountName": sAMAccountName,
        "groupname": groupname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'AddUserToGroup', str(respjson), str(value))
    return respjson


#(9)将用户从组中移除
def RemoveUserFromGroup(sAMAccountName,groupname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'RemoveUserFromGroup'
    value = {
        "sAMAccountName": sAMAccountName,
        "groupname": groupname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'RemoveUserFromGroup', str(respjson), str(value))
    return respjson

#(10)从用户组中获得组员
def GetUserFromGroup(groupname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'GetUserFromGroup'
    value = {
        "groupname": groupname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetUserFromGroup', str(respjson), str(value))
    return respjson


#(11)移除组中所有成员
def RemoveAllUserFromGroup(groupname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'RemoveAllUserFromGroup'
    value = {
        "groupname": groupname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'RemoveAllUserFromGroup', str(respjson), str(value))
    return respjson

#(12)根据用户名获取用户所有组(权限）
def GetAdGroup(username,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'GetAdGroup'
    value = {
        "username": username,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetAdGroup', str(respjson), str(value))
    return respjson


#(13)根据工号获取AD账号，姓名，邮箱
def GetAccountinfoByJobnumber(jobnumber,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'GetAccountinfoByJobnumber'
    value = {
        "jobnumber": jobnumber,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetAccountinfoByJobnumber', str(respjson), str(value))
    return respjson



#(14)根据Gid获取AD账号，姓名，邮箱）
def GetAccountinfoByGid(guid,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'GetAccountinfoByGid'
    value = {
        "guid": guid,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetAccountinfoByGid', str(respjson), str(value))
    return respjson



#(15)测试加密
def Encryption(guid):
    ipvalue = serverip()
    url = ipvalue + 'Encryption'
    value = {
        "guid": guid,
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    return respjson


#(15)测试解密
def Decrypt(name,guid):
    ipvalue = serverip()
    url = ipvalue + 'Decrypt'
    value = {
        "guid": guid,
        "name": name,
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    return respjson


#(16)根据用户名和密码确定权限
def VerifyUserLogin(username,password,domain,tokenid=None,ip=None):
    '''

    :param username:
    :param password:
    :param domain:
    :param tokenid:
    :return:
    '''
    ipvalue = serverip()
    url = ipvalue + 'VerifyUserLogin'
    value = {
        "username": username,
        "password": password,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'VerifyUserLogin', str(respjson), str(value))
    return respjson


#(17)设置OU进行删除组
def DeleteAdgroupByOU(groupname,oudn,domain,tokenid=None,ip=None):
    '''
    :param groupname:
    :param oudn: OU=xxxxxxxxxxx,DC=xxx,DC=com
    :param domain:
    :param tokenid:
    :return:
    '''
    ipvalue = serverip()
    url = ipvalue + 'DeleteAdgroupByOU'
    value = {
        "groupname": groupname,
        "ou": oudn,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'DeleteAdgroupByOU', str(respjson), str(value))
    return respjson


#(18)判断OU下是否有任何对象
def inspectOU(ouname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'inspectOU'
    value = {
        "ouname": ouname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'inspectOU', str(respjson), str(value))
    return respjson



#(19)设置OU进行删除OU 固定OU=IT,当OU里面有对象无法删除
def DeleteAdouByOU(ouname,oudn,domain,tokenid=None,ip=None):
    '''
    :param domain:
    :param tokenid:
    :return:
    '''
    ipvalue = serverip()
    url = ipvalue + 'DeleteAdouByOU'
    value = {
        "ouname": ouname,
        "ou": oudn,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'DeleteAdouByOU', str(respjson), str(value))
    return respjson


#(20)根据对象类别重命名
def Renameobject(objects,newobjects,catalog,domain,tokenid=None,ip=None):
    '''
    :param objects:
    :param newobjects:
    :param catalog: 'user','group','organizationalUnit','computer'
    :param domain:
    :param tokenid:
    :return:
    '''
    ipvalue = serverip()
    url = ipvalue + 'Renameobject'
    value = {
        "objects": objects,
        "newobjects": newobjects,
        "objectClass": catalog,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'Renameobject', str(respjson), str(value))
    return respjson


#（21）user开通邮箱
def UserToExc(username,dbname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'UserToExc'
    value = {
        "username": username,
        "dbname": dbname,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'UserToExc', str(respjson), str(value))
    return respjson


#（22）user创建邮箱归档
def CreateMailboxArchive(username,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'CreateMailboxArchive'
    value = {
        "username": username,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'CreateMailboxArchive', str(respjson), str(value))
    return respjson


#(23)新增用户smtp地址
def setuseremailadress(username,smtpValue,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'setuseremailadress'
    value = {
        "username": username,
        "smtpValue": smtpValue,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'setuseremailadress', str(respjson), str(value))
    return respjson

#(24)删除用户smtp地址
def deluseremailadress(username,smtpValue,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'deluseremailadress'
    value = {
        "username": username,
        "smtpValue": smtpValue,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'deluseremailadress', str(respjson), str(value))
    return respjson



#(25)New-MoveRequestArchive迁移用户邮箱和存档数据库
def NewMoveRequestArchive(username,TargetDatabase,ArchiveTargetDatabase,domain,tokenid=None,ip=None):

    ipvalue = serverip()
    url = ipvalue + 'NewMoveRequestArchive'
    value = {
        "username": username,
        "TargetDatabase": TargetDatabase,
        "ArchiveTargetDatabase": ArchiveTargetDatabase,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'NewMoveRequestArchive', str(respjson), str(value))
    return respjson

#(26)修改邮箱
def EditMail(username,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'EditMail'
    value = {
        "username": username,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'EditMail', str(respjson), str(value))
    return respjson


#(27)根据对象类别修改属性
def SetobjectProperty(objects,objectClass,PropertyName,PropertyValue,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'SetobjectProperty'
    value = {
        "objects": objects,
        "objectClass": objectClass,
        "PropertyName": PropertyName,
        "PropertyValue": PropertyValue,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'SetobjectProperty', str(respjson), str(value))
    return respjson


#（28）get-mailboxdatabase-novalue  获取所有邮箱数据库信息 -远程执行get-mailboxdatabase命令
def getmailboxdatabasenovalue(domain,tokenid=None,ip=None):
    '''

    :param domain:
    :param tokenid:
    :return: {'isSuccess': True, 'message': ["{'daname':'Mailbox Database 0146370333'}"]}
    '''
    ipvalue = serverip()
    #ipvalue = 'http://localhost:26816/api/adapi/'
    url = ipvalue + 'getmailboxdatabasenovalue'
    value = {
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'getmailboxdatabasenovalue', str(respjson), str(value))
    return respjson




#（29）删除AD账号
def delaccount(username,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'delaccount'
    value = {
        "username": username,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'delaccount', str(respjson), str(value))
    return respjson



#（30）这个账号是否显示在Exchange通讯簿上
def ListsEnabled(username,isaddressbook,domain,tokenid=None,ip=None):
    '''
    isaddressbook = "1"
    不显示在Exchange地址列表中  打勾
    else
    不显示在Exchange地址列表中  不打勾
    :param username:
    :param isaddressbook:
    :param domain:
    :param tokenid:
    :return:
    '''
    try:
        ipvalue = serverip()
        url = ipvalue + 'ListsEnabled'
        value = {
            "username": username,
            "isaddressbook": isaddressbook,
            "domain": domain,
            "skey": admd5()
        }
        querystring = parse.urlencode(value)
        u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
        respjson = json.loads(u)
        insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'ListsEnabled', str(respjson), str(value))
        return respjson
    except Exception as e:
        insert_interface_c_log(str(ip),'False', str(tokenid), 'ListsEnabled', str(e), str(value))
        respjson = {'message': 'ListsEnabled:'+str(e), 'isSuccess': False,}
        return respjson



#（31）账号解锁
def UnlockAccount(objects,domain,tokenid=None,ip=None):
    try:
        ipvalue = serverip()
        url = ipvalue + 'UnlockAccount'
        value = {
            "objects": objects,
            "domain": domain,
            "skey": admd5()
        }
        querystring = parse.urlencode(value)
        u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
        respjson = json.loads(u)
        insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'UnlockAccount', str(respjson), str(value))
        return respjson
    except Exception as e:
        insert_interface_c_log(str(ip),'False', str(tokenid), 'UnlockAccount', str(e), str(value))
        respjson = {'message': 'UnlockAccount:'+str(e), 'isSuccess': False,}
        return respjson

#(32)根据OU获取数据
def GetobjectForOu(path,id,domain,tokenid=None,ip=None):
    try:
        ipvalue = serverip()
        url = ipvalue + 'GetobjectForOu'
        value = {
            "path": path,
            "id": id,
            "domain": domain,
        }
        querystring = parse.urlencode(value)
        u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
        respjson = json.loads(u)
        insert_interface_c_log(str(ip), str(respjson['isSuccess']), str(tokenid), 'GetobjectForOu', str(respjson), str(value))
        return respjson
    except Exception as e:
        respjson = {'message': 'GetobjectForOu:'+str(e), 'isSuccess': False,}
        insert_interface_c_log(str(ip), str(respjson['isSuccess']), str(tokenid), 'GetobjectForOu', str(respjson), str(value))
        return respjson


#(33)获取这个ou所有的user
def getuser(path,domain,users,tokenid=None,ip=None):
    getusers = GetobjectForOu(path,'1',domain,tokenid,ip)
    if getusers['isSuccess']:
        for i in getusers['message']:
            if i['objectClass']=='user':
                users.append({'path': i['path'], 'name': i['name'],})
            elif i['objectClass']=='organizationalUnit':
                getuser(i['path'],users)
        return users

# 根据 distinguishedName 获取信息并判定对象类别
def GetPropertyFordistinguishedName(distinguishedName,domain,tokenid=None,ip=None):
    try:
        ipvalue = serverip()
        url = ipvalue + 'GetPropertyFordistinguishedName'
        value = {
            "distinguishedName": distinguishedName,
            "domain": domain,
            "skey": admd5()
        }
        querystring = parse.urlencode(value)
        u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
        respjson = json.loads(u)
        insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetPropertyFordistinguishedName', str(respjson), str(value))
        return respjson
    except Exception as e:
        insert_interface_c_log(str(ip),'False', str(tokenid), 'GetPropertyFordistinguishedName', str(e), str(value))
        respjson = {'message': 'GetPropertyFordistinguishedName:'+str(e), 'isSuccess': False,}
        return respjson


#设置用户的最大发件人数量为100
def RecipientLimits(username,domain,tokenid=None,ip=None):
    try:
        ipvalue = serverip()
        url = ipvalue + 'SetMailbox'
        value = {
            "mailname": username,
            "parametername": "RecipientLimits",
            "parametervalue": "100",
            "skey": admd5()
        }
        querystring = parse.urlencode(value)
        u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
        respjson = json.loads(u)
        insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'RecipientLimits', str(respjson), str(value))
        return respjson
    except Exception as e:
        insert_interface_c_log(str(ip),'False', str(tokenid), 'RecipientLimits', str(e), str(value))
        respjson = {'message': 'RecipientLimits:'+str(e), 'isSuccess': False,}
        return respjson

#离职禁用手机邮箱
def CloseCASMailbox(username,domain,tokenid=None,ip=None):
    try:
        ipvalue = serverip()
        url = ipvalue + 'CloseCASMailbox'
        value = {
            "mailname": username,
            "skey": admd5()
        }
        querystring = parse.urlencode(value)
        u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
        respjson = json.loads(u)
        insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'CloseCASMailbox', str(respjson), str(value))
        return respjson
    except Exception as e:
        insert_interface_c_log(str(ip),'False', str(tokenid), 'CloseCASMailbox', str(e), str(value))
        respjson = {'message': 'RecipientLimits:'+str(e), 'isSuccess': False,}
        return respjson



#根据smtp查询user信息
def GetobjectPropertybysmtp(objects,domain):
    ipvalue = serverip()
    url=ipvalue+'GetobjectPropertybysmtp'
    value = {
        "objects": objects,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    return respjson

#查询用户是否有对应组权限
def sel_account_to_group(account,group):
    '''

    :param account:
    :param group:
    :return: True False
    '''
    try:
        result = False
        GetobjectPropertys = adapi().Initialapi("GetobjectProperty",objects=account,objectClass='user')
        if GetobjectPropertys['isSuccess']:
            memberof = GetobjectPropertys['message'][0].get("memberof",'')
            if memberof:
                groups = "CN="+str(group)+","
                for member in memberof:
                    if groups in member:
                        result = True
        return result
    except:
        return False

#获取上级主管方法
def getmanger(username,type):
    try:
        mangermess = genmangemessage()
        if mangermess == None:
            manger = False
        elif mangermess['status'] == '0':
            manger = genmangehow(type)[type]
        else:
            apiurl = getmangerapi('getmanger')['mess']
            url= apiurl+'&username='+username
            data = urllib.request.urlopen(url).read().decode('utf-8')
            directorlist = json.loads(data)
            if directorlist['ResultCode'] == 0:
                manger=directorlist['List'][0]['EmpCount']
            else:
                manger = genmangehow(type)[type]
                # manger = directorlist['List'][0]['Email']
        return manger
    except Exception as e:
        return genmangehow(type)[type]

def Send_message(jzphone, message):  # 调取短信接口
    Send_message_thr(jzphone, message)


#获取账号到期时间
def GetuseraccountExpires(objects,domain,tokenid=None, ip=None):
    '''
    :param objects:
    :return:  True
    '''
    ipvalue = serverip()
    url = ipvalue + 'GetuseraccountExpires'
    value = {
        "objects": objects,
        "domain": domain,
        "skey": admd5()
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip), str(respjson), str(tokenid), 'ObjectExists', str(respjson), str(value))
    return respjson
