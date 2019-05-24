#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from urllib import request, parse
import json
from datetime import datetime

import requests

from folder_api.dbinfo import dbinfo


def dbinfo_select_global_configuration():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from global_configuration "
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def serverip():
    try:
        mysqlallvalue = dbinfo_select_global_configuration()[0]
        ipvalue = 'http://' + str(mysqlallvalue['iis_ip']) + ':' + str(mysqlallvalue['iis_port']) + '/api/Adapi/'
    except:
        ipvalue = 'http://localhost:22238/api/adapi/'
    return ipvalue

def get_md5(domain):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT skey from global_configuration where ad_domain= %s"
        conncur.execute(connsql, domain)
        MD5 = conncur.fetchone()
        conn.commit()
        conn.close()
        return MD5['skey']
    except Exception as e:
        print(e)
        return None

def insert_interface_c_log(ip, isSuccess, tokenid, apiname, parameter, message):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO interface_c_log (ip,isSuccess, tokenid,apiname,parameter,message,times) VALUES (%s,%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (ip, isSuccess, tokenid, apiname, parameter, message, createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def Createobject(objects,oudn,objectClass,domain,sn=None,displayName=None,wWWHomePage=None,password=None,guid=None,tokenid=None,ip=None):
    '''
    :param objects:
    :param oudn:
    :param objectClass: 'user','group','organizationalUnit','computer'
    :param sn:
    :param displayName:
    :param wWWHomePage:
    :param password:
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
        "skey": get_md5(domain)
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
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
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
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    return respjson


#(8)将用户加入到用户组中
def AddUserToGroup(sAMAccountName,groupname,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'AddUserToGroup'
    value = {
        "sAMAccountName": sAMAccountName,
        "groupname": groupname,
        "domain": domain,
        "skey": get_md5(domain)
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
        "skey": get_md5(domain)
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
        "skey": get_md5(domain)
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
        "skey": get_md5(domain)
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
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetAdGroup', str(respjson), str(value))
    return respjson


#(13)根据工号获取AD账号，姓名，邮箱）
def GetAccountinfoByJobnumber(jobnumber,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'GetAccountinfoByJobnumber'
    value = {
        "jobnumber": jobnumber,
        "domain": domain,
        "skey": get_md5(domain)
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
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'GetAccountinfoByGid', str(respjson), str(value))
    return respjson




#(17)设置OU进行删除组
def DeleteAdgroupByOU(groupname,oudn,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'DeleteAdgroupByOU'
    value = {
        "groupname": groupname,
        "ou": oudn,
        "domain": domain,
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'DeleteAdgroupByOU', str(respjson), str(value))
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
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'Renameobject', str(respjson), str(value))
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
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'SetobjectProperty', str(respjson), str(value))
    return respjson


#（29）删除AD账号
def delaccount(username,domain,tokenid=None,ip=None):
    ipvalue = serverip()
    url = ipvalue + 'delaccount'
    value = {
        "username": username,
        "domain": domain,
        "skey": get_md5(domain)
    }
    querystring = parse.urlencode(value)
    u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    respjson = json.loads(u)
    insert_interface_c_log(str(ip),str(respjson['isSuccess']), str(tokenid), 'delaccount', str(respjson), str(value))
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
            "skey": get_md5(domain)
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


