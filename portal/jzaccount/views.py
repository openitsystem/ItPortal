import datetime
import json
import os
import re

import xlrd
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from threading import Thread
import time

from logmanager.views import logmanager


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj:
            if isinstance(obj, (datetime.datetime, obj)):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            raise TypeError("Type %s not serializable" % type(obj))


# Create your views here.
# 更改密码页面
from adapi.dbinfo import searchmind, get_domain, get_PermissionsGrops, sear_jzcount, searid_jzcountid, update_jzcountid, \
    updel_jzcountid, updel_jzpwd, insert_jzcountlog, searid_jzphone, get_Effective_account, upde_jzcountidmanger,get_Effective_accountALL
from adapi.pwd import genpwd
from adapi.timetont import getnttime
from jzaccount.jzscheduler import triggerjob
from tools.delpwdnolock import delpwdnolock, adapi, ResetPasswordByOU, ObjectExist, GetobjectProperty, VerifyUserLogin, \
    UnlockAccount, AddUserToGroup, Send_message, dbinfo_select_global_configuration, request
from tools.views import if_user_in_groupDN, if_user_in_group


#############数据库status含义+############
# status = 1  正常账号
# status= 2   创建成功，修改到期时间失败（需从AD中把账号删除）
# status = 3  申请人主动关闭
# status = 4  自动关闭
#status = 5  AD账号被管理员从AD中手动删除，同时申请人或管理员在页面执行关闭操作
#########################################


# 兼职账号申请页面
def jzaccountapp(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username = username.lower()
            domain = get_domain()
            it_authority_group = get_PermissionsGrops()['part_time_group']
            authority = if_user_in_group(username, it_authority_group, domain)
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority == True or authority1 == True:
                return render_to_response('jzaccount/jzaccountapp.html', locals())
            else:
                log.log(returnid=0, username=username, ip=ip, message='没有权限',
                        issuccess=0,
                        methodname="jzaccountapp", types="JZAD")
                return render_to_response('index.html', locals())
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="jzaccountapp", types="JZAD")
        return False

#管理员权限判断,前端是否显示
def IFadmin(request):
    username = request.session.get('username')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            result = 2
            username = username.lower()
            domain = get_domain()
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority1:
                result = 1
        else:
            result = 2
    except Exception as e:
        result = 2
        log.log(returnid=0, username=username, ip=ip, message='异常报错'+str(e),
               issuccess=0,
               methodname="IFadmin", types="JZAD")
    result = {'result': result,}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#判断是否有兼职账号权限,在前端显示
def jzhtml(request):
    username = request.session.get('username')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            result = 2
            username = username.lower()
            domain = get_domain()
            it_authority_group = get_PermissionsGrops()['part_time_group']
            authority = if_user_in_group(username, it_authority_group, domain)
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority == True or authority1 == True:
                result = 1
        else:
            result = 2
    except Exception as e:
        result = 2
        log.log(returnid=0, username=username, ip=ip, message='异常报错'+str(e),
               issuccess=0,
               methodname="jzhtml", types="JZAD")
    result = {'result': result,}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


# 有效账号管理
def Effective_account(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username = username.lower()
            domain = get_domain()
            it_authority_group = get_PermissionsGrops()['part_time_group']
            authority = if_user_in_group(username, it_authority_group, domain)
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority == True or authority1 == True:
                return render_to_response('jzaccount/Effectiveaccount.html', locals())
            else:
                log.log(returnid=0, username=username, ip=ip, message='没有权限',
                        issuccess=0,
                        methodname="Effective_account", types="JZAD")
                return render_to_response('index.html', locals())
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip, message='异常报错'+str(e),
               issuccess=0,
               methodname="Effective_account", types="JZAD")
        return False


# 兼职账号管理员
def Account_Management(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username = username.lower()
            domain = get_domain()
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority1:
                return render_to_response('jzaccount/AccountManagement.html', locals())
            else:
                log.log(returnid=0, username=username, ip=ip, message='没有权限',
                        issuccess=0,
                        methodname="Account_Management", types="JZAD")
                return render_to_response('index.html', locals())
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,message='异常报错'+str(e),
               issuccess=0,
               methodname="Account_Management", types="JZAD")
        return False

# 申请权限管理
def Account_AddManagement(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username = username.lower()
            domain = get_domain()
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority1:
                return render_to_response('jzaccount/AccountAddManagement.html', locals())
            else:
                log.log(returnid=0, username=username, ip=ip, message='没有权限',
                        issuccess=0,
                        methodname="Account_addManagement", types="JZAD")
                return render_to_response('index.html', locals())
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="Account_addManagement", types="JZAD")
        return False


# 导入
def handle_uploaded_file1(f):
    file_name = ""
    try:
        path = "upload/"
        file_name = path + f.name
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as e:

        print (e)
    return file_name


# Excel 上传
####################
# isSuccess=1 创建成功
# isSuccess=2 创建失败
# isSuccess=3 格式不是excel
##############
def fileupload(request):
    username = request.session.get('username')
    file = request.FILES.get('excelname')
    squsername = request.session.get('username')
    sqdisplayname = request.session.get('displayname')
    sqmail = request.session.get('mail')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    zjlist = []
    Success = 1
    if username:
        username = username.lower()
        domain = get_domain()
        it_authority_group = get_PermissionsGrops()['part_time_group']
        authority = if_user_in_group(username, it_authority_group, domain)
        jzound = get_PermissionsGrops()['jz_account_dn']
        it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
        authority1 = if_user_in_group(username, it_authority_group1, domain)
        if authority == True or authority1 == True:
            if file != None:
                mess = os.path.splitext(str(file))[1]
                if mess == '.xls' or mess == '.xlsx':
                    isSuccess = ''
                    filename = handle_uploaded_file1(file)
                    data = xlrd.open_workbook(filename)
                    table = data.sheet_by_index(0)
                    nrows = table.nrows  # 行数
                    ncols = table.ncols  # 列数
                    # colnames =  table.row_values(0) #某一行数据
                    try:
                        for i in range(1, nrows):
                            row_data = table.row_values(i)
                            row_data = row_data[0:3]  # 获取列表中的前3个
                            jzphone = row_data[0]
                            jzphone = int(jzphone)
                            jzphone = str(jzphone)
                            jzphone = jzphone.replace(' ', '')  # 去除账号中的空格
                            jzphone = re.findall(r"\d+\.?\d*", jzphone)  # 用正则取出字符串中的数字，组成列表。
                            jzphone = ''.join(jzphone)  # 将列表转换为字符串
                            jzname = row_data[1].replace("<", '').replace(">", '')
                            jzterm = row_data[2]
                            jzterm = int(jzterm)
                            jzterm = str(jzterm)
                            lejzp = len(jzphone)
                            jzterm = jzterm.replace(' ', '')  # 去除账号中的空格
                            if len(jzphone) == 11 and jzname != "" and (
                                        jzterm == "7" or jzterm == "14" or jzterm == "30"):
                                jzaccount = "jz" + jzphone
                                deadtime = datetime.datetime.now() + datetime.timedelta(days=int(jzterm))
                                deadtime = deadtime.strftime('%Y-%m-%d %H:%M:%S')
                                nowdatetime = datetime.datetime.now()
                                passwd = genpwd()  # 调取密码生成方法，自动生成密码
                                User = adapi().Initialapi('Createobject', objects=jzaccount, oudn=jzound,
                                                          objectClass='user',
                                                          sn=jzname, displayName=jzname, wWWHomePage=squsername,
                                                          password=passwd,
                                                          guid=sqmail)
                                if User['isSuccess']:
                                    ntstamp = getnttime(int(jzterm))  # 计算到期时间
                                    setntstamp = adapi().Initialapi('SetuserProperty', username=jzaccount,
                                                                    PropertyName='accountExpires',
                                                                    PropertyValue=ntstamp, )
                                    setdescription = adapi().Initialapi('SetuserProperty', username=jzaccount,
                                                                        PropertyName='description',
                                                                        PropertyValue=sqdisplayname, )
                                    if setntstamp['isSuccess']:
                                        status = 1
                                        msg = jzname + '您好，你的兼职AD账号为：' + jzaccount + '，初始密码为' + passwd + ',您的账号到期时间为' + deadtime
                                        msg1=jzname + '您好，你的兼职AD账号为：' + jzaccount + ',您的账号到期时间为' + deadtime
                                        Send_message(jzphone,msg)  #短信通知
                                        message = {}
                                        message['isSuccess'] = True
                                        message['account'] = jzaccount
                                        message['pwd'] = passwd
                                        message['deadtime'] = deadtime
                                        message['jznames'] = jzname
                                        zjlist.append(message)
                                        log.log(returnid=1, username=username, ip=ip, message=jzaccount + '创建成功',
                                                issuccess=1,
                                                methodname="fileupload", returnparameters=str(msg1), types="JZAD")
                                    else:
                                        status = 2
                                        Error = {}
                                        Error['isSuccess'] = False
                                        Error['message'] = jzaccount + '账号创建成功,到期时间修改失败，请通知管理员核实,并在AD中删除'
                                        zjlist.append(Error)
                                        log.log(returnid=0, username=username, ip=ip, message=jzaccount + '账号创建成功,到期时间修改失败，请通知管理员核实,并在AD中删除',
                                                issuccess=0,
                                                methodname="fileupload", returnparameters=str(Error), types="JZAD")
                                    writeDB = insert_jzcountlog(jzaccount, jzname, deadtime, nowdatetime, jzphone,
                                                                squsername, sqdisplayname, sqmail, status)
                                else:
                                    Error = {}
                                    Error['isSuccess'] = False
                                    Error['message'] = jzphone + User['message']['message']
                                    zjlist.append(Error)
                                    log.log(returnid=0, username=username, ip=ip,
                                            message=jzaccount + '账号创建失败，调用API异常',
                                            issuccess=0,
                                            methodname="fileupload", returnparameters=str(Error), types="JZAD")
                            else:
                                Error = {}  # 创建空的字典
                                Error["message"] = jzphone + "信息错误,请核实手机号码必须为11位，姓名不能为空，使用期限仅支持 7,15,30"  # 在字典中添加  key 等于 错误信息
                                Error["isSuccess"] = False  # 在字典中增加创建错误后，isSuccess=False，给前台判断取值
                                zjlist.append(Error)  # 向列表zjlist中添加创建错误的返回信息。
                                log.log(returnid=0, username=username, ip=ip,
                                        message=jzphone + '信息错误,请核实手机号码必须为11位，姓名不能为空，使用期限仅支持 7,15,30',
                                        issuccess=0,
                                        methodname="fileupload", returnparameters=str(Error), types="JZAD")
                                continue
                    except Exception as e:
                        Success = 2
                        print(e)
                        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                                issuccess=0,
                                methodname="fileupload", types="JZAD")

                else:
                    Success = 3
                    log.log(returnid=0, username=username, ip=ip,
                            message='文件格式错误',
                            issuccess=0,
                            methodname="fileupload", types="JZAD")
            else:
                log.log(returnid=0, username=username, ip=ip,
                        message='文件为空',
                        issuccess=0,
                        methodname="fileupload", types="JZAD")
                Success = 4
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message='没有权限',
                    issuccess=0,
                    methodname="fileupload",types="JZAD")
            Success = 2
            return render_to_response("index.html", locals())
    else:
        return render_to_response("portal.html", locals())
    result = {'message': zjlist, 'isSuccess': Success}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


# 兼职账号申请
def creatjzcount(request):
    squsername = request.session.get('username')
    sqdisplayname = request.session.get('displayname')
    sqmail = request.session.get('mail')
    post = request.POST
    jzphones = post.get('jzphones').split(';')
    jznames = post.get('jznames').split(';')
    jzterms = post.get('jzterms').split(';')
    zjlist = []
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if squsername:
            username = squsername.lower()
            domain = get_domain()
            it_authority_group = get_PermissionsGrops()['part_time_group']
            jzound = get_PermissionsGrops()['jz_account_dn']
            authority = if_user_in_group(username, it_authority_group, domain)
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority == True or authority1 == True:
                for i in range(len(jzphones) - 1):
                    jzname = (jznames[i]).replace("<", '').replace(">", '')
                    print(jzname)
                    passwd = genpwd()
                    deadtime = datetime.datetime.now() + datetime.timedelta(days=int(jzterms[i]))
                    deadtime = deadtime.strftime('%Y-%m-%d %H:%M:%S')
                    nowdatetime = datetime.datetime.now()
                    jzcount = 'jz' + jzphones[i].replace(' ', '')
                    User = adapi().Initialapi('Createobject', objects=jzcount, oudn=jzound, objectClass='user',
                                              sn=jzname, displayName=jzname, wWWHomePage=squsername,
                                              password=passwd,
                                              guid=sqmail)
                    if User['isSuccess']:
                        ntstamp = getnttime(int(jzterms[i]))  # 计算到期时间
                        setntstamp = adapi().Initialapi('SetuserProperty', username=jzcount,
                                                        PropertyName='accountExpires', PropertyValue=ntstamp, )
                        setdescription = adapi().Initialapi('SetuserProperty', username=jzcount,
                                                            PropertyName='description', PropertyValue=sqdisplayname, )
                        if setntstamp['isSuccess']:
                            status = 1
                            msg = jzname + '您好，你的兼职AD账号为：' + jzcount + '密码为' + passwd + ',您的账号到期时间为' + deadtime
                            msg1 = jzname + '您好，你的兼职AD账号为：' + jzcount+ ',您的账号到期时间为' + deadtime
                            Send_message(jzphones[i],msg)  #短信通知
                            message = {}
                            message['isSuccess'] = True
                            message['account'] = jzcount
                            message['pwd'] = passwd
                            message['deadtime'] = deadtime
                            message['jznames'] = jzname
                            zjlist.append(message)
                            log.log(returnid=1, username=username, ip=ip, message=jzcount + '创建成功',
                                    issuccess=1,
                                    methodname="creatjzcount", returnparameters=str(msg1), types="JZAD")
                        else:
                            status = 2
                            Error = {}
                            Error['isSuccess'] = False
                            Error['message'] = jzcount + '账号创建成功,到期时间修改失败，请通知管理员核实,并在AD中删除'
                            zjlist.append(Error)
                            log.log(returnid=0, username=username, ip=ip, message=jzcount + '账号创建成功,到期时间修改失败，请通知管理员核实,并在AD中删除',
                                    issuccess=0,
                                    methodname="creatjzcount", returnparameters=str(Error), types="JZAD")
                        writeDB = insert_jzcountlog(jzcount, jzname, deadtime, nowdatetime, jzphones[i], squsername,
                                                    sqdisplayname, sqmail, status)
                    else:
                        Error = {}
                        Error['isSuccess'] = False
                        Error['message'] = jzphones[i] + User['message']['message']
                        zjlist.append(Error)
                        log.log(returnid=0, username=username, ip=ip, message=jzcount + '账号创建失败，调用API异常',
                                issuccess=0,
                                methodname="creatjzcount", returnparameters=str(Error), types="JZAD")
            else:
                log.log(returnid=0, username=username, ip=ip, message= '没有权限',
                        issuccess=0,
                        methodname="creatjzcount",types="JZAD")
                return render_to_response("index.html", locals())
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        print(e)
        Error = {}
        Error['isSuccess'] = False
        Error['message'] = '程序异常'
        zjlist.append(Error)
        log.log(returnid=0,ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="creatjzcount", types="JZAD")
    result = {'message': zjlist}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


# 验证账号是否存在
def searphonesq(request):
    post = request.POST
    phone = post.get('phone')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        messa = adapi().Initialapi('ObjectExistAD', objectName='jz' + phone)
        searphon = searid_jzphone(phone)
        if messa == True or searphon != ():
            reslu = False
        else:
            reslu = True
    except Exception as e:
        reslu = False
        print(e)
        log.log(returnid=0,ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="searphonesq", types="JZAD")
    result = {'status': reslu}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#获取个人名下有效账号
def showjzcountmanger(request):
    username = request.session.get('username')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        temptable = get_Effective_account(username)
    except Exception as e:
        temptable=0
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="showjzcountmanger", types="JZAD")
    result = {'status': temptable}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, cls=DatetimeEncoder))
    return response

#获取所有有效账号
def showjzcountmangerALL(request):
    username = request.session.get('username')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        status = 1
        temptable = get_Effective_accountALL(status)
    except Exception as e:
        temptable=0
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="showjzcountmangerALL", types="JZAD")
    result = {'status': temptable}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, cls=DatetimeEncoder))
    return response

# 新关闭限定OU
def deljzcountmessage(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    getSelections = request.POST.get('getSelections')
    displayname = request.session.get('displayname')
    if username:
        domain = get_domain()
        it_authority_group = get_PermissionsGrops()['part_time_group']
        jzound = get_PermissionsGrops()['jz_account_dn']
        authority = if_user_in_group(username, it_authority_group, domain)
        it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
        authority1 = if_user_in_group(username, it_authority_group1, domain)
        dellist = []
        try:
            if authority == True or authority1 == True:
                if getSelections:
                    getSelectionsLists = eval(getSelections.replace("true", "'true'").replace("false", "'false'"))
                    for i in getSelectionsLists:
                        idValue = i['id']
                        jzcount = i['jzcount'].lower()
                        IFjzcountdn = adapi().Initialapi('ObjectExistsOU', objectName=jzcount, catalog='user',
                                                         ouname=jzound)
                        IFuser=adapi().Initialapi('ObjectExists',objectName=jzcount,catalog='user')
                        if IFuser != True:
                            message = {}
                            message['isSuccess'] = True
                            message['message'] = jzcount + '在AD中不存在,数据库已同步更新'
                            dellist.append(message)
                            updel_jzcountid('5', idValue)
                            log.log(returnid=1, username=username, ip=ip, message=jzcount + '在AD中不存在,数据库已同步更新状态',
                                    issuccess=1,
                                    methodname="deljzcountmessage", returnparameters=str(message), types="JZAD")
                        elif jzcount != 'administrator' and IFjzcountdn:
                            dejzcount = adapi().Initialapi('delaccount', username=jzcount)
                            if dejzcount['isSuccess']:
                                message = {}
                                message['isSuccess'] = True
                                message['message'] = jzcount + 'AD账号删除成功'
                                dellist.append(message)
                                updel_jzcountid('3', idValue)
                                log.log(returnid=1, username=username, ip=ip, message=jzcount + 'AD账号删除成功',
                                        issuccess=1,
                                        methodname="deljzcountmessage", returnparameters=str(message), types="JZAD")
                            else:
                                error = {}
                                error['isSuccess'] = True
                                error['message'] = jzcount + dejzcount['message']['message']
                                dellist.append(error)
                                log.log(returnid=0, username=username, ip=ip, message=jzcount + 'AD账号删除失败，接口调用失败',
                                        issuccess=0,
                                        methodname="deljzcountmessage", returnparameters=str(error), types="JZAD")
                        elif jzcount == 'administrator':
                            error = {}
                            error['isSuccess'] = True
                            error['message'] = 'administrator不能被删除'
                            dellist.append(error)
                            log.log(returnid=0, username=username, ip=ip, message='administrator不能被删除',
                                    issuccess=0,
                                    methodname="deljzcountmessage", returnparameters=str(error), types="JZAD")
                        elif jzcount != True:
                            error = {}
                            error['isSuccess'] = True
                            error['message'] = jzcount + '在指定OU中不存在'
                            dellist.append(error)
                            log.log(returnid=0, username=username, ip=ip, message=jzcount + '在指定OU中不存在',
                                    issuccess=0,
                                    methodname="deljzcountmessage", returnparameters=str(error), types="JZAD")
            else:
                error = {}
                error['isSuccess'] = False
                error['message'] = '你没有权限'
                dellist.append(error)
                log.log(returnid=0, username=username, ip=ip, message='没有权限',
                        issuccess=0,
                        methodname="deljzcountmessage",types="JZAD")
        except Exception as e:
            print(e)
            log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                    issuccess=0,
                    methodname="deljzcountmessage", types="JZAD")
        result = {'message': dellist}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return render_to_response("portal.html", locals())


# 兼职账号续期、
def updatejzdate(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    post = request.POST
    extension_account = post.get('idValue')
    extension_time = post.get('radiovalue')
    updatelist = []
    domain = get_domain()
    it_authority_group = get_PermissionsGrops()['part_time_group']
    authority = if_user_in_group(username, it_authority_group, domain)
    it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
    authority1 = if_user_in_group(username, it_authority_group1, domain)
    try:
        if username:
            if authority == True or authority1 == True:
                if extension_account:
                    extension_accountlist = eval(
                        extension_account.replace("true", "'true'").replace("false", "'false'"))
                    for i in extension_accountlist:
                        olddate = i['deadtime']
                        jzcount = i['jzcount']
                        accountID = i['id']
                        olddate = datetime.datetime.strptime(olddate, "%Y-%m-%d %H:%M:%S")  # 将时间字符串转换成datetime.date形式
                        newdeadtime = olddate + datetime.timedelta(days=int(extension_time))  # 到期时间
                        mintime = time.mktime(newdeadtime.timetuple())
                        namintime = int(mintime + 11644473600)
                        nowTime = lambda: int(round(namintime * 10000000))
                        newdeadtime1 = nowTime()
                        setntstamp = adapi().Initialapi('SetuserProperty', username=jzcount,
                                                        PropertyName='accountExpires',
                                                        PropertyValue=newdeadtime1)
                        if setntstamp['isSuccess']:
                            message = {}
                            message['isSuccess'] = True
                            message['message'] = jzcount + '续约成功'
                            updatelist.append(message)
                            update_jzcountid(newdeadtime, accountID)
                            log.log(returnid=1, username=username, ip=ip, message=jzcount + '续约成功', issuccess=1,
                                    methodname="updatejzdate", returnparameters=str(updatelist), types="JZAD")
                        else:
                            error = {}
                            error['isSuccess'] = True
                            error['message'] = jzcount + '续约失败' + setntstamp['message']['message']
                            updatelist.append(error)
                            log.log(returnid=0, username=username, ip=ip, message=jzcount + '续约失败,API调用异常', issuccess=0,
                                    methodname="updatejzdate", returnparameters=str(updatelist), types="JZAD")
            else:
                error = {}
                error['isSuccess'] = False
                error['message'] = '你没有权限'
                updatelist.append(error)
                log.log(returnid=0, username=username, ip=ip, message='你没有权限', issuccess=0,
                        methodname="updatejzdate", returnparameters=str(updatelist), types="JZAD")
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="updatejzdate", types="JZAD")
    result = {'message': updatelist}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


# 重置兼职账号密码
# 1重置成功
# 2重置失败
def jzresetpwd(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    post = request.POST
    idValue = post.get('id')
    jzcount = post.get('jzcount')
    phone = post.get('phone')
    log = logmanager()
    if username:
        domain = get_domain()
        it_authority_group = get_PermissionsGrops()['part_time_group']
        authority = if_user_in_group(username, it_authority_group, domain)
        it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
        authority1 = if_user_in_group(username, it_authority_group1, domain)
        if authority == True or authority1 == True:
            passwd = genpwd()
            jzrewpwd = adapi().Initialapi('ResetPasswordByOU', username=jzcount, newpassword=passwd)
            msg = jzcount + '的新密码为' + passwd
            if jzrewpwd['isSuccess']:
                status = 1
                Send_message(phone,msg)  #短信通知
                log.log(returnid=1, username=username, ip=ip, message=jzcount + '密码修改成功', issuccess=1,
                        methodname="jzresetpwd", returnparameters=str(jzcount+'密码重置成功'), types="JZAD")
            else:
                status = 2
                passwd = ''
                log.log(returnid=0, username=username, ip=ip, message=jzcount + '密码修失败'+"API调用失败", issuccess=0,
                        methodname="jzresetpwd", returnparameters=str(msg), types="JZAD")
        else:
            status = 3
            passwd = ''
            log.log(returnid=0, username=username, ip=ip, message='你没有权限', issuccess=0,
                    methodname="jzresetpwd",types="JZAD")
    else:
        return render_to_response("portal.html", locals())
    result = {'status': status, 'password': passwd, 'jzcount': jzcount}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 更改管理者
def upjzmanger(request):
    username = request.session.get('username')
    jzaccounts = request.POST.get('jzmeshow')
    newmanger = request.POST.get('pbmanger')
    domain = get_domain()
    zjlist = []
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            property = GetobjectProperty(newmanger, 'user', domain, tokenid=None, ip=None)
            domain = get_domain()
            it_authority_group = get_PermissionsGrops()['part_time_group']
            authority = if_user_in_group(username, it_authority_group, domain)
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority == True or authority1 == True:
                if property['isSuccess']:
                    newmangerAccount = property['message'][0]['sAMAccountName']
                    newmangerdisplayName = property['message'][0]['displayName']
                    newmangermail = property['message'][0]['mail']
                    if newmangerAccount and  newmangerdisplayName and newmangermail:
                        if jzaccounts:
                            jzaccounts = eval(jzaccounts.replace("true", "'true'").replace("false", "'false'"))
                            for i in jzaccounts:
                                jzcount = i['jzcount']
                                id = i['id']
                                setdescription = adapi().Initialapi('SetuserProperty', username=jzcount,
                                                                    PropertyName='description',
                                                                    PropertyValue=newmangerdisplayName, )
                                setphysicalDeliveryOfficeName = adapi().Initialapi('SetuserProperty', username=jzcount,
                                                                                   PropertyName='physicalDeliveryOfficeName',
                                                                                   PropertyValue=newmangermail,)
                                setwWWHomePage = adapi().Initialapi('SetuserProperty', username=jzcount,
                                                                    PropertyName='wWWHomePage',
                                                                    PropertyValue=newmangerAccount, )
                                if setdescription['isSuccess'] and setphysicalDeliveryOfficeName['isSuccess'] and setwWWHomePage['isSuccess']:
                                    upde_jzcountidmanger(newmangerAccount, newmangerdisplayName, newmangermail, id)
                                    message = {}
                                    message['message'] = jzcount + '修改成功'
                                    zjlist.append(message)
                                    log.log(returnid=1, username=username, ip=ip, message=jzcount + '管理者修改成功', issuccess=1,
                                            methodname="upjzmanger", returnparameters=str(message),types="JZAD")
                                else:
                                    message = {}
                                    message['message'] = jzcount + '修改失败'
                                    zjlist.append(message)
                                    log.log(returnid=0, username=username, ip=ip, message=jzcount + '管理者修改失败,数据库未更新', issuccess=0,
                                            methodname="upjzmanger", returnparameters=str(message),types="JZAD")
                        else:
                            message = {}
                            message['message'] = '账号为空'
                            zjlist.append(message)
                            log.log(returnid=0, username=username, ip=ip, message='账号为空', issuccess=0,
                                    methodname="upjzmanger", returnparameters=str(message), types="JZAD")
                    else:
                        message = {}
                        message['message'] = '新管理者信息缺失,无法更改,需保证新管理者以下字段在AD中不为空{sAMAccountName，displayName，mail}'
                        zjlist.append(message)
                        log.log(returnid=0, username=username, ip=ip, message='新管理者信息缺失,无法更改,需保证新管理者以下字段在AD中不为空{sAMAccountName，displayName，mai', issuccess=0,
                                methodname="upjzmanger", returnparameters=str(message), types="JZAD")
                else:
                    message = {}
                    message['message'] = '新管理者账号错误'
                    zjlist.append(message)
                    log.log(returnid=0, username=username, ip=ip, message='新管理者账号错误222222', issuccess=0,
                        methodname="upjzmanger", returnparameters=str(message), types="JZAD")
            else:
                message = {}
                message['message'] = '你没有权限'
                zjlist.append(message)
                log.log(returnid=0, username=username, ip=ip, message='你没有权限', issuccess=0,
                        methodname="upjzmanger", returnparameters=str(message), types="JZAD")
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="upjzmanger", types="JZAD")
    result = {'message': zjlist}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#有权限申请JZ账号管理
def getGetUserFromGroup(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    memberoflist = []
    try:
        it_authority_group = get_PermissionsGrops()['part_time_group']
        memberof = adapi().Initialapi('GetUserFromGroup', groupname=it_authority_group)
        if memberof['isSuccess']:
            memberofs=memberof['message']['message']
            for i in memberofs:
                member=i['member']
                propertys = adapi().Initialapi('GetPropertyFordistinguishedName', distinguishedName=member)
                property={}
                property['sAMAccountName']=propertys['message'][0]['sAMAccountName']
                property['displayName'] = propertys['message'][0]['displayName']
                memberoflist.append(property)
    except Exception as e:
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="getGetUserFromGroup", types="JZAD")
    result = {"message": memberoflist}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, cls=DatetimeEncoder))
    return response


#删除申请权限
def Delete_application_permission(request):
    getSelections = request.POST.get('getSelections')
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    dellist = []
    try:
        if username:
            domain = get_domain()
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            it_authority_group = get_PermissionsGrops()['part_time_group']
            if authority1 == True:
                if getSelections:
                    getSelectionsLists = eval(getSelections.replace("true", "'true'").replace("false", "'false'"))
                    for i in getSelectionsLists:
                        sAMAccountName = i['sAMAccountName']
                        messgae=adapi().Initialapi('RemoveUserFromGroup', sAMAccountName=sAMAccountName,groupname=it_authority_group)
                        dellist.append(messgae)
                        log.log(returnid=1, username=username, ip=ip, message=messgae['message'], issuccess=1,
                                methodname="Delete_application_permission", returnparameters=str(messgae), types="JZAD")
            else:
                message = {}
                message['message'] = '你没有权限'
                dellist.append(message)
                log.log(returnid=0, username=username, ip=ip, message='你没有权限', issuccess=0,
                        methodname="Delete_application_permission", returnparameters=str(message), types="JZAD")
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="Delete_application_permission", types="JZAD")
    result = {"message": dellist}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, cls=DatetimeEncoder))
    return response


# 添加兼职账号申请权限
def addjzmanger(request):
    username = request.session.get('username')
    sAMAccountName = request.POST.get('pbmanger')
    domain = get_domain()
    addlist = []
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            it_authority_group = get_PermissionsGrops()['part_time_group']
            domain = get_domain()
            it_authority_group1 = dbinfo_select_global_configuration()[0]['it_group']
            authority1 = if_user_in_group(username, it_authority_group1, domain)
            if authority1 == True:
                addgroup=adapi().Initialapi('AddUserToGroup', sAMAccountName=sAMAccountName,groupname=it_authority_group)
                addlist.append(addgroup)
                log.log(returnid=1, username=username, ip=ip, message=addgroup['message'] , issuccess=1,
                        methodname="addjzmanger", returnparameters=str(addgroup), types="JZAD")
            else:
                message = {}
                message['message'] = '你没有权限'
                addlist.append(message)
                log.log(returnid=0, username=username, ip=ip, message='你没有权限', issuccess=0,
                        methodname="addjzmanger", returnparameters=str(message), types="JZAD")
        else:
            return render_to_response("portal.html", locals())
    except Exception as e:
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="upjzmanger", types="JZAD")
    result = {'message': addlist}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response