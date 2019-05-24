#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 16:14
# @Author  : Center
import ast
import json
import urllib
import uuid

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

import datetime
from Thr.Ther import flow_agree
from adapi.ad_api import adapi, sel_account_to_group
from adapi.dbinfo import searchcount, searchover, searchreviercont, searchrevier, showid, updatepumailuser,updatepumailuser_allow,getmailou_new, \
    searchrsystemlog, searchreviersystemlog, shwotitle
from adapi.pwd import genpwd
from admin_account.dbinfo import dbinfo_select_global_configuration
from dfs.dbinfo import get_management_configuration
from logmanager.views import logmanager
from sendmail.sendmail import send_email_by_template
from threading import Thread

from tools.views import MyThread


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj:
            if isinstance(obj, (datetime.datetime, obj)):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            raise TypeError("Type %s not serializable" % type(obj))

def referuser(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('overall/refer.html', locals())


def review(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('overall/review.html', locals())

def systemlog(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    if userisinitgroup(username):
        return render_to_response('overall/systemlog.html', locals())
    else:
        return HttpResponseRedirect('/', request)


def showmailpubapp(request):
    log = logmanager()
    username = request.session.get('username')
    try:
        row = searchover(username)
    except Exception as e:
        log.log(returnid=0, username=username, message=username + "获取申请记录", returnparameters=str(e),
                issuccess=0,
                methodname="showmailpubapp", types="exchange")
        print(e)
    result = {'status':row}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,cls=DatetimeEncoder))
    return response


def showmailpubreview(request):
    log = logmanager()
    username = request.session.get('username')
    try:
        row = searchrevier(username)

    except Exception as e:
        log.log(returnid=0, username=username, message=username + "获取审批记录", returnparameters=str(e),
                issuccess=0,
                methodname="showmailpubreview", types="exchange")
    result = {'status': row}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, cls=DatetimeEncoder))
    return response

def showsystemlog(request):
    username = request.session.get('username')
    index = int(request.GET.get("pageIndex"))
    size = int(request.GET.get("pageSize"))
    startPos = (index - 1) * size
    total=searchrsystemlog()[0]['count(* )']
    row=[]
    row = searchreviersystemlog(startPos,size)
    return HttpResponse(json.dumps({"total": total, "rows": row}, cls=DatetimeEncoder),content_type="application/json")


#申请详细
def usershowid(request):
    log = logmanager()
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    messagelast = ""
    if username:
        try:
            post = request.POST
            id = post.get('id')
            message=showid(id)
            if len(message):
                if message[0]['adaccount'].lower() == username.lower():
                    messagelast = message
        except Exception as e:
            log.log(returnid=0, username=username, message=username + "获取申请记录详细", returnparameters=str(e),
                    issuccess=0,
                    methodname="showmailpubapp", types="exchange")
            print(e)
        result = {'status': messagelast}
        return HttpResponse(json.dumps(result,cls=DatetimeEncoder),content_type="application/json")
    else:
        return HttpResponseRedirect('/', request)


# class MyThread(Thread):
#
#     def __init__(self, parameter1):
#         Thread.__init__(self)
#         self.parameter1 = parameter1
#
#     def run(self):
#         self.result1 = adapi().Initialapi('GetPropertyFordistinguishedName', distinguishedName=self.parameter1)
#         self.result = (self.result1)['message'][0]
#
#     def get_result(self):
#         try:
#             return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
#         except Exception:
#             return None

#用户信息首页申请详细
def userindexvalueshow(request):
    log = logmanager()
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    isSuccess = False
    message = {}
    if username:
        try:
            uservalue = adapi().Initialapi("GetobjectProperty",objects=username,objectClass="user")
            if uservalue['isSuccess']:
                userdisplayname = uservalue['message'][0]['displayName']
                usermail = uservalue['message'][0]['mail']
                PasswordExpirationDate = uservalue['message'][0]['PasswordExpirationDate']
                usermemberof = uservalue['message'][0]['memberof']
                usermemberoflist = list()
                usermemberoflastlist = list()
                userip = ip
                strtype = ""
                listtype = list()
                if type(usermemberof) == type(strtype) or type(usermemberof) == type(listtype):
                    if type(usermemberof) == type(strtype):
                        usermemberoflist.append(usermemberof)
                    else:
                        usermemberoflist = usermemberof
                    li = list()
                    rows = list()
                    for i in usermemberoflist:
                        t = MyThread(i)
                        li.append(t)
                        t.start()
                    for t in li:
                        t.join()
                        usermemberoflastlist.append(t.get_result())
                usermaillist = list()
                userinternetlist = list()
                userwifilist = list()
                uservpnlist = list()
                for i in usermemberoflastlist:
                    if i['mail'] != None:
                        usermaillist.append({"displayname":i['displayName'],"mail":i['mail']})
                    internet_group = ast.literal_eval(get_management_configuration()['internet_group'])
                    for internet_group_one in internet_group:
                        if internet_group_one['name'].lower() == i['sAMAccountName'].lower():
                            userinternetlist.append(internet_group_one['description'])
                    wifi_group = ast.literal_eval(get_management_configuration()['wifi_group'])
                    for wifi_group_one in wifi_group:
                        if wifi_group_one['name'].lower() == i['sAMAccountName'].lower():
                            userwifilist.append(wifi_group_one['description'])
                    vpn_group = ast.literal_eval(get_management_configuration()['vpn_group'])
                    for vpn_group_one in vpn_group:
                        if vpn_group_one['name'].lower() == i['sAMAccountName'].lower():
                            uservpnlist.append(vpn_group_one['description'])
                isSuccess = True
                message = {"userdisplayname":userdisplayname,"usermail":usermail,"usermaillist":usermaillist,"userinternetlist":userinternetlist,"userwifilist":userwifilist,"uservpnlist":uservpnlist,"ip":ip,"PasswordExpirationDate":PasswordExpirationDate}
        except Exception as e:
            isSuccess = False
            message = {}
        result = {'isSuccess': isSuccess,"message":message}
        return HttpResponse(json.dumps(result,cls=DatetimeEncoder),content_type="application/json")
    else:
        return HttpResponseRedirect('/', request)


def showtitle(request):
    try:
        tltile = shwotitle()
        if tltile == None or tltile ==False :
            status='IT开放平台'
        else:
            status = tltile['title']
    except Exception as e:
        status = 'IT开放平台'
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response



#邮箱审批
def pumailaccid(request):
    log = logmanager()
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    post = request.POST
    id = post.get("id")
    try:
        folowvalue = showid(id)[0]
        if folowvalue['director'].lower() == username.lower():
            updatepumailuser(id, 0)
            flow_agree(folowvalue)
            status = 1
            log.log(returnid=1, username=username,ip=ip,message="同意申请单ID" + str(id), issuccess=1,
                    methodname="pumailaccid", types="other")
        else:
            status = 0
            log.log(returnid=0, username=username,ip=ip,message="同意申请单ID" + str(id), issuccess=0,
                    returnparameters="越权！",
                    methodname="pumailaccid", types="other")
    except Exception as e:
        status = 0
        log.log(returnid=0, username=username,ip=ip,message="同意申请单ID" + str(id), issuccess=0,
                returnparameters=str(e),
                methodname="pumailaccid", types="other")
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#审批不同意
def refuspubmail(request):
    log = logmanager()
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    post = request.POST
    id = post.get("id")
    try:
        folowvalue = showid(id)[0]
        if folowvalue['director'].lower() == username.lower():
            updatepumailuser_allow(id, 3)
            status = 1
            log.log(returnid=1, username=username,ip=ip,message="拒绝申请单ID" + str(id), issuccess=1,
                    methodname="pumailaccid", types="other")
        else:
            status = 0
            log.log(returnid=0, username=username,ip=ip,message="拒绝申请单ID" + str(id), issuccess=0,
                    returnparameters="越权！",
                    methodname="pumailaccid", types="other")
    except Exception as e:
        status = 0
        log.log(returnid=0, username=username,ip=ip,message="拒绝申请单ID" + str(id), issuccess=0,
                returnparameters=str(e),
                methodname="pumailaccid", types="other")
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#关闭公共邮箱
def mailcountdel(request):
    log=logmanager()
    username = request.session.get('username')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    count = request.POST.get('count')
    try:
        configsql = getmailou_new()
        publicmailconfig = configsql[0]['pubmailou']
        pubmailfence = configsql[0]['pubmailfence']
        if pubmailfence != "" and pubmailfence != None:
            pubmailfencelastvalue = pubmailfence
        else:
            pubmailfencelastvalue = "physicalDeliveryOfficeName"
        if publicmailconfig != "" and publicmailconfig != None:
            ad_path = publicmailconfig
        else:
            ad_path = dbinfo_select_global_configuration()[0]['ad_path']
        publicmailvalue = adapi().postapi('GetUserFromLdap',ldaps='(&(objectCategory=person)(objectClass=user)(mail=*) (sAMAccountName=' + count + '))',
                                          path=ad_path)
        if publicmailvalue['isSuccess'] and publicmailvalue['Count'] != 0:
            publicmailvaluemessage = publicmailvalue['message'][0]
            managervalue = publicmailvaluemessage.get(pubmailfencelastvalue.lower(), [None])[0]
            if managervalue.lower() == username.lower():
                message = adapi().Initialapi('SetuserProperty', username=count, PropertyName='userAccountControl',
                                             PropertyValue=514)
                if message['isSuccess']:
                    status=1
                    log.log(returnid=0, ip=ip, message=username + "删除公共邮箱成功" + count, issuccess=0,
                            inparameters=str(publicmailvalue), methodname="mailcountdel", types="exchange")
                else:
                    log.log(returnid=0, ip=ip, message=username + "删除公共邮箱失败" + count, issuccess=0,
                            inparameters=str(publicmailvalue), methodname="mailcountdel", types="exchange")
                    status=2
            else:
                status=2
                log.log(returnid=0, ip=ip, message=username + "越权" + count, issuccess=0,
                        inparameters=str(publicmailvalue), methodname="mailcountdel", types="exchange")
        else:
            status=2
            log.log(returnid=0, ip=ip, message=username + "为查询到公共邮箱，疑似越权" + count, issuccess=0,
                    inparameters=str(publicmailvalue), methodname="mailcountdel", types="exchange")
    except Exception as e:
        status=2
        log.log(returnid=0, ip=ip, message=username + "删除公共邮箱异常"+count , issuccess=0,
                inparameters=str(e), methodname="mailcountdel", types="exchange")
        print(e)
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#修改公共邮箱属性
def updatepubmess(request):
    log=logmanager()
    username = request.session.get('username')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    pubmailadd = request.POST.get('pubmailadd')
    samcoun = request.POST.get('sancount')
    displaypub = request.POST.get('displaypub')
    pbmanger = request.POST.get('pbmanger')
    oldmanger = request.POST.get('oldmanger')
    try:
        configsql = getmailou_new()
        publicmailconfig = configsql[0]['pubmailou']
        pubmailfence = configsql[0]['pubmailfence']
        if pubmailfence != "" and pubmailfence != None:
            pubmailfencelastvalue = pubmailfence
        else:
            pubmailfencelastvalue = "physicalDeliveryOfficeName"
        if publicmailconfig != "" and publicmailconfig != None:
            ad_path = publicmailconfig
        else:
            ad_path = dbinfo_select_global_configuration()[0]['ad_path']
        publicmailvalue = adapi().postapi('GetUserFromLdap',
                                          ldaps='(&(objectCategory=person)(objectClass=user)(mail=*) (sAMAccountName=' + samcoun + '))',
                                          path=ad_path)
        if publicmailvalue['isSuccess'] and publicmailvalue['Count'] != 0:
            publicmailvaluemessage = publicmailvalue['message'][0]
            managervalue = publicmailvaluemessage.get(pubmailfencelastvalue.lower(), [None])[0]
            if managervalue.lower() == username.lower():
                if oldmanger.lower() != pbmanger.lower():
                    usermail = adapi().Initialapi('GetobjectProperty', objects=pbmanger.lower(), objectClass='user')
                    pnmangermail=usermail['message'][0]['mail']
                    setdisname = adapi().Initialapi('SetuserProperty', username=samcoun, PropertyName='displayName',PropertyValue=displaypub)
                    setmanger = adapi().Initialapi('SetuserProperty', username=samcoun, PropertyName='physicalDeliveryOfficeName',PropertyValue=pbmanger)
                    if setdisname['isSuccess'] and setmanger['isSuccess']:
                        log.log(returnid=1, ip=ip,message=username+"修改公共邮箱属性，修改管理者为"+pbmanger+'修改显示名称'+displaypub, issuccess=1, inparameters=str(setdisname)+str(setmanger),
                                methodname="updatepubmess", types="exchange")
                        subject = u'公共邮箱更改'
                        emaillists = '您已经拥有公共邮箱:'+pubmailadd+'的权限,如果想要重置密码，请登录平台重置该公共邮箱的密码！ '
                        email_data = {'emaillists': emaillists}
                        template = "mailmould/sendmailpassword.html"
                        to_list = [pnmangermail]
                        send_email_by_template(subject, template, email_data, to_list)
                        status=1
                    else:
                        log.log(returnid=0, ip=ip,message=username+"修改公共邮箱属性，修改管理者为"+pbmanger+'修改显示名称'+displaypub, issuccess=0, inparameters=str(setdisname)+str(setmanger),
                                methodname="updatepubmess", types="exchange")
                        status=2
                else:
                    setdisname = adapi().Initialapi('SetuserProperty', username=samcoun, PropertyName='displayName',PropertyValue=displaypub)
                    if setdisname['isSuccess']:
                        log.log(returnid=1, ip=ip, message=username + "修改公共邮箱属性，修改显示名称" + displaypub, issuccess=1,
                                inparameters=str(setdisname),
                                methodname="updatepubmess", types="exchange")
                        status=1
                    else:
                        log.log(returnid=0, ip=ip, message=username + "修改公共邮箱属性，修改显示名称" + displaypub, issuccess=0,
                                inparameters=str(setdisname),methodname="updatepubmess", types="exchange")
                        status=2
            else:
                status=2
    except Exception as e:
        log.log(returnid=0, ip=ip, message=username + "修改公共邮箱属性，修改显示名称" + displaypub, issuccess=0,
                inparameters=str(e), methodname="updatepubmess", types="exchange")
        print(e)
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#公共邮箱重置密码
def psdpubmailset(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    samcoun = request.POST.get('samcoun')
    mailaddress = request.session.get('mail')
    try:
        configsql = getmailou_new()
        publicmailconfig = configsql[0]['pubmailou']
        pubmailfence = configsql[0]['pubmailfence']
        if pubmailfence != "" and pubmailfence != None:
            pubmailfencelastvalue = pubmailfence
        else:
            pubmailfencelastvalue = "physicalDeliveryOfficeName"
        if publicmailconfig != "" and publicmailconfig != None:
            ad_path = publicmailconfig
        else:
            ad_path = dbinfo_select_global_configuration()[0]['ad_path']
        publicmailvalue = adapi().postapi('GetUserFromLdap',ldaps='(&(objectCategory=person)(objectClass=user)(mail=*) (sAMAccountName=' + samcoun + '))',
                                          path=ad_path)
        if publicmailvalue['isSuccess'] and publicmailvalue['Count'] != 0:
            publicmailvaluemessage = publicmailvalue['message'][0]
            managervalue = publicmailvaluemessage.get(pubmailfencelastvalue.lower(), [None])[0]
            if managervalue.lower() == username.lower():
                passwd=genpwd()
                message=adapi().Initialapi('ResetPasswordByOU', username=samcoun,newpassword=passwd)
                if  message['isSuccess']:
                    subject = u'公共邮箱密码重置'
                    emaillists = '您的公共邮箱:' + samcoun + '已经重置密码,新密码为'+passwd+'，请妥善保管密码，并同步给使用此公共邮箱的同事'
                    email_data = {'emaillists': emaillists}
                    template = "mailmould/sendmailpassword.html"
                    to_list = [mailaddress]
                    send_email_by_template(subject, template, email_data, to_list)
                    log.log(returnid=1, username=username, ip=ip,
                            message=username + "重置公共邮箱密码", returnparameters='密码修改成功',
                            issuccess=1,methodname="psdpubmailset", types="AD")
                else:
                    message = {'message': {'message': '重置失败。'}, 'isSuccess': False}
                    log.log(returnid=0, username=username, ip=ip,
                            message=username + "重置公共邮箱密码", returnparameters=str(message),
                            issuccess=0, methodname="psdpubmailset", types="AD")
            else:
                message = {'message': {'message': '越权操作。'}, 'isSuccess': False}
    except Exception as e:
        message={'message': {'message': '异常。'}, 'isSuccess': False}
        print(e)
        log.log(returnid=0, username=username, ip=ip,
                message=username + "重置公共邮箱密码", returnparameters=str(e),
                issuccess=0, methodname="psdpubmailset", types="AD")
    result = message
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#判断是否有IT权限
def userisinitgroup(username):
    mysqlallvalue = dbinfo_select_global_configuration()[0]
    it_group = mysqlallvalue['it_group']
    if it_group == '' or it_group == None or it_group == "None":
        return False
    else:
        if sel_account_to_group(username,it_group):
            return True
        else:
            return False


#判断是否有IT权限
def systemlog_permission(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    samcoun = request.POST.get('samcoun')
    try:
        if userisinitgroup(username):
            message = True
        else:
            message = False
    except Exception as e:
        message = False
    result = message
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def publicmailmanagement(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('overall/publicmailmanagement.html', locals())

#公共邮箱管理者展示
def showmailpumangaer(request):
    log = logmanager()
    username = request.session.get('username')
    try:
        pubmes=get_management_configuration()
        mess= adapi().postapi('GetUserFromLdap',ldaps='(&(objectCategory=person)(objectClass=user)(mail=*) ('+pubmes['pubmailfence']+'='+username+'))',path=pubmes['pubmailou'])
        temptable=[]
        if mess['isSuccess']:
            for i in mess['message']:
                if i.get('useraccountcontrol', ['None'])[0]==514 or i.get('useraccountcontrol', ['None'])[0] == 546 or i.get('useraccountcontrol', ['None'])[0] == 4130 or i.get('useraccountcontrol', ['None'])[0] == 4198:
                    pass
                else:
                    mangefenc=pubmes['pubmailfence'].lower()
                    lastpwd = adapi().Initialapi('GetobjectProperty', objects=i['samaccountname'][0], objectClass='user')
                    temptable.append({'samaccountname': i.get('samaccountname', ['None'])[0],
                                      'physicaldeliveryofficename': i.get(mangefenc, ['None'])[0],
                                      'displayname': i.get('displayname', ['None'])[0],
                                      'mail': i.get('mail', ['None'])[0],
                                      'PasswordExpirationDate': lastpwd['message'][0].get('PasswordExpirationDate',
                                                                                          'None')})
    except Exception as e:
        log.log(returnid=1, username=username, message=username + "登录获取公共邮箱管理者账号信息", returnparameters=str(e),issuccess=1, methodname="showmailpumangaer", types="exchange")
        print(e)
    result = {'status':temptable}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response
