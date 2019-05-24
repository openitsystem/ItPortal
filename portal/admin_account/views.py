
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ast
import uuid

import requests
from django.shortcuts import render, render_to_response

import urllib.parse
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, HttpResponseRedirect,HttpResponse
import os,json,random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from adapi.dbinfo import searchsendmail, insert_sendmail, genmangemessage, genmangemessageshow, mangersql, \
    insermangerstau, delmanger, insert_apimanger, genmangeurl, delapimanger, inserphonestau, \
    insert_phoneurl, genmuser, sendmeasage, sendmestaus, insert_sendphone, delmangeruser, delconfiger, \
    delsendconfig, shwotitle, insert_title, deltitleconfig, update_title, mangersqlupdate, update_config
from dbinfo_ad.newdbtest import dbinfotest
import hashlib
from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x

from dfs.dbinfo import get_management_configuration, get_api, insert_api, \
    update_management_configuration_changepwdremindertips, getconfiguration
from dfs.thr_folder import set_file_mysql
from itportal.settings import Identity_Exception, Identity_Exception_admin, administratorpassword
from admin_account.encrypt_decode import encrypt_and_decode
from  adapi.ad_api import iisservertest,adapi
from  admin_account.dbinfo import dbinfo_insert_iisvalue,dbinfo_select_global_configuration,dbinfo_insert_advalue,dbinfo_insert_exvalue,dbinfo_insert_skeyvalue,dbinfo_insert_itgroupvalue, \
    dbinfo_insert_adminvalue, dbinfo_insert_adipsvalue
from admin_account.Profile import readprofile,writeprofile
from logmanager.views import logmanager
from tools.views import MyThread


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        sessionusername = request.session.get("username")
        if sessionusername:
            for i in Identity_Exception_admin:
                if i in request.path:
                    if sessionusername.lower() != "administrator":
                        return HttpResponseRedirect('/portal/', request)
                    else:
                        response = self.get_response(request)
                        return response
        else:
            try:
                for i in Identity_Exception:
                    if i.lower() in (request.path).lower():
                        response = self.get_response(request)
                        if request.path.lower() == "/portal/":
                            request.session['returnbackurl'] = '/'
                        return response
                getCodeUrl = request.path
                request.session['returnbackurl'] = getCodeUrl
                return HttpResponseRedirect('/portal/',request)
            except Exception as e:
                return HttpResponseRedirect('/portal/', request)




def adminconfig(request):
    username = request.session.get('username')
    if username.lower() != 'administrator':
        return HttpResponseRedirect('/portal/', request)
    displayname = request.session.get('displayname')
    mysqlipvalue = readprofile('mysql','ip')
    mysqlusernamevalue = readprofile('mysql','username')
    mysqlPortevalue = readprofile('mysql','Port')
    mysqlPasswordvalue = readprofile('mysql','Password')
    if mysqlipvalue != 'None'and mysqlipvalue != "" and mysqlipvalue != None:
        mysqlallvalue = dbinfo_select_global_configuration()[0]
        iis_ip = mysqlallvalue['iis_ip']
        if iis_ip == '' or iis_ip == None:
            iis_ip = 'None'
        iis_port = mysqlallvalue['iis_port']
        if iis_port == '' or iis_port == None:
            iis_port = 'None'
        ad_ip = mysqlallvalue['ad_ip']
        if ad_ip == '' or ad_ip == None:
            ad_ip = 'None'
        ad_account = mysqlallvalue['ad_account']
        if ad_account == '' or ad_account == None:
            ad_account = 'None'
        ad_password = mysqlallvalue['ad_password']
        if ad_password == '' or ad_password == None:
            ad_password = 'None'
        ad_domain = mysqlallvalue['ad_domain']
        if ad_domain == '' or ad_domain == None:
            ad_domain = 'None'
        ad_path = mysqlallvalue['ad_path']
        if ad_path == '' or ad_path == None:
            ad_path = 'None'
        ex_ip = mysqlallvalue['ex_ip']
        if ex_ip == '' or ex_ip == None:
            ex_ip = 'None'
        ex_account = mysqlallvalue['ex_account']
        if ex_account == '' or ex_account == None:
            ex_account = 'None'
        ex_password = mysqlallvalue['ex_password']
        if ex_password == '' or ex_password == None:
            ex_password = 'None'
        ex_domain = mysqlallvalue['ex_domain']
        if ex_domain == '' or ex_domain == None:
            ex_domain = 'None'
        it_group = mysqlallvalue['it_group']
        if it_group == '' or it_group == None:
            it_group = 'None'
        # ad_ips = mysqlallvalue['ad_ips']
        # if ad_ips == '' or ad_ips == None or ad_ips == "None":
        #     ad_ips = 'None'
        # else:
        #     ad_ips = ad_ips.split(",")
    return render_to_response('admin/adminindex.html', locals())


# def admd5_skey():
#     m = hashlib.md5()
#     m.update(b'adapi@sssssss1111')
#     md5value = m.hexdigest()
#     skey = md5value.upper()
#     return skey

def admd5_skey(skeyvalue):
    m = hashlib.md5()
    m.update(skeyvalue.encode() )
    md5value = m.hexdigest()
    skey = md5value.upper()
    return skey


#xIIS信息配置
def iislinktest(request):
    post = request.POST
    iisinputip = post.get("iisinputip")
    iisinputport = post.get("iisinputport")
    skeyvalue = admd5_skey(str(uuid.uuid4()))
    dbinfo_insert_skeyvalue(skeyvalue)
    if iisservertest(iisinputip,iisinputport,server=readprofile('mysql','ip'),Database='itdev-portal',PORT=readprofile('mysql','Port'),Uid=readprofile('mysql','username'),password=readprofile('mysql','Password'),skey=skeyvalue):
        serverviistestvalue = 1
        dbinfo_insert_iisvalue(iisinputip,iisinputport)
    else:
        serverviistestvalue = 0
    result = {'serverviistestvalue': serverviistestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

def adlinktest(request):
    post = request.POST
    adinputip = post.get("adinputip")
    adinputaccount = post.get("adinputaccount")
    adinputpassword = post.get("adinputpassword")
    adinputdomain = post.get("adinputdomain")
    adinputpath = post.get("adinputpath")
    password = encrypt_and_decode().encrypted_text(adinputpassword)
    adapitestvalue = adapi().testapi('adlinktest',adip=adinputip,account=adinputaccount,password=adinputpassword,domain=adinputdomain,adpath=adinputpath)
    if adapitestvalue and ('isSuccess' in adapitestvalue):
        if adapitestvalue['isSuccess']:
            serverviistestvalue = 1
            dbinfo_insert_advalue(adinputip,adinputaccount,password,adinputdomain,adinputpath)
        else:
            serverviistestvalue = 0
    else:
        serverviistestvalue = 0
    result = {'serverviistestvalue': serverviistestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

def delitgroup(request):
    try:
        post = request.POST
        dbinfo_insert_itgroupvalue('None')
        searchvalue = 1
    except Exception as e:
        searchvalue = 0
    result = {'serverviistestvalue': searchvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def itgroupsearch(request):
    try:
        post = request.POST
        itgroupname = post.get("itgroupname")
        searchgroupvalue  = adapi().Initialapi("Showgroupname",groupname=itgroupname)
        if searchgroupvalue['isSuccess']:
            searchvalue = 1
            dbinfo_insert_itgroupvalue(itgroupname)
        else:
            searchvalue = 0
    except Exception as e:
        searchvalue = 0
    result = {'serverviistestvalue': searchvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def showitgroupmembers(request):
    try:
        post = request.POST
        itgroupname = post.get("groupname")
        username = request.session.get('username')
        if username.lower() == "administrator":
            groupmanager = adapi().Initialapi('Showgroupname', groupname=itgroupname)
            rows = list()
            # aa = MyThread(groupmanager['message']['member'])
            li = []
            groupmanagerlist = list()
            if type(groupmanager['message']['member']) != type(groupmanagerlist):
                groupmanagerlist.append(groupmanager['message']['member'])
            else:
                groupmanagerlist = groupmanager['message']['member']
            if groupmanagerlist != [None]:
                for i in groupmanagerlist:
                    t = MyThread(i)
                    li.append(t)
                    t.start()
                for t in li:
                    t.join()
                    rows.append(t.get_result())
                    # rows.append(adapi().Initialapi('GetPropertyFordistinguishedName', distinguishedName=i)['message'][0])
            a = {"total": len(rows), "rows": rows}
            return HttpResponse(json.dumps(a))
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        return HttpResponseRedirect('/adminconfig/', request)


def exlinktest(request):
    post = request.POST
    exinputip = post.get("exinputip")
    exinputaccount = post.get("exinputaccount")
    exinputpassword = post.get("exinputpassword")
    exinputdomain = post.get("exinputdomain")
    password = encrypt_and_decode().encrypted_text(exinputpassword)
    exapitestvalue = adapi().testapi('testexlink',exip=exinputip,exaccount=exinputaccount,expassword=exinputpassword,domain=exinputdomain)
    # exapitestvalue = adapi().testapi('GetActiveSyncDevice',mailname='administrator',parametername='11',domain=exinputdomain)
    if exapitestvalue and ('isSuccess' in exapitestvalue) :
        if  exapitestvalue['isSuccess']:
            serverviistestvalue = 1
            dbinfo_insert_exvalue(exinputip,exinputaccount,password,exinputdomain)
        else:
            serverviistestvalue = 0
    else:
        serverviistestvalue = 0
    result = {'serverviistestvalue': serverviistestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#
def mysqllinktest(request):
    post = request.POST
    myysqlip = post.get("inputip")
    myysqlusername = post.get("inputusername")
    myysqlpassword = post.get("inputpassword")
    myysqlport = post.get("inputport")
    if dbinfotest(myysqlip,myysqlusername,myysqlpassword,myysqlport):
        # dir_now = os.path.dirname(os.path.abspath("settings.py"))
        writeprofile("mysql", "ip", myysqlip)
        writeprofile("mysql", "username", myysqlusername)
        writeprofile("mysql", "Password", encrypt_and_decode().encrypted_text(myysqlpassword))
        writeprofile("mysql", "Port", myysqlport)
        try:
            set_file_mysql()
        except:
            servervmsqltestvalue = 1
        servervmsqltestvalue = 1
    else:
        servervmsqltestvalue = 0
    result = {'servervmsqltestvalue': servervmsqltestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response
#


def changeadminpwd(request):
    try:
        post = request.POST
        adminoldpwd = post.get("adminoldpwd")
        adminnewpwd = post.get("adminnewpwd")
        adminrealnewpwd = post.get("adminrealnewpwd")
        username = request.session.get('username')
        if username.lower() == "administrator":
            if adminoldpwd !='' and adminnewpwd != '' and adminrealnewpwd != '':
                if adminnewpwd == adminrealnewpwd:
                    adminsqlpassword = dbinfo_select_global_configuration()[0]['adminpwd']
                    if adminsqlpassword == '' or adminsqlpassword == None or adminsqlpassword == "None":
                        adminoldassword = administratorpassword
                    else:
                        adminoldassword = adminsqlpassword
                    if check_password(adminoldpwd, adminoldassword):
                        realpassword = make_password(adminnewpwd)
                        dbinfo_insert_adminvalue(realpassword)
                        isSuccess = 1
                        message = ''
                    else:
                        isSuccess = 0
                        message = "请输入正确的密码"
                else:
                    isSuccess = 0
                    message = "两次密码不一致"
            else:
                isSuccess = 0
                message = "请输入完整"
        else:
            isSuccess = 0
            message = "越权"
    except Exception as e:
        isSuccess = 0
        message = "系统异常"
    result = {'isSuccess': isSuccess,"message":message}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


# def addadips(request):
#     try:
#         post = request.POST
#         addadips_value = post.getlist("adips")
#         addadips_value = list(set(addadips_value))
#         lastadips = ','.join(addadips_value)
#         username = request.session.get('username')
#         if username.lower() == "administrator":
#             if len(addadips_value):
#                 dbinfo_insert_adipsvalue(lastadips)
#                 isSuccess = 1
#                 message = ""
#             else:
#                 isSuccess = 0
#                 message = "请输入完整"
#         else:
#             isSuccess = 0
#             message = "越权"
#     except Exception as e:
#         isSuccess = 0
#         message = "系统异常"
#     result = {'isSuccess': isSuccess,"message":message}
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     response.write(json.dumps(result))
#     return response
#
# def deladdadips(request):
#     try:
#         post = request.POST
#         username = request.session.get('username')
#         if username.lower() == "administrator":
#             dbinfo_insert_adipsvalue("None")
#             isSuccess = 1
#             message = ""
#         else:
#             isSuccess = 0
#             message = "越权"
#     except Exception as e:
#         isSuccess = 0
#         message = "系统异常"
#     result = {'isSuccess': isSuccess,"message":message}
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     response.write(json.dumps(result))
#     return response

def delmysqllink(request):
    try:
        # dir_now = os.path.dirname(os.path.abspath("settings.py"))
        writeprofile("mysql", "ip", "None")
        writeprofile("mysql", "username", "None")
        writeprofile("mysql", "Password", "None")
        writeprofile("mysql", "Port", "None")
        servervmsqltestvalue = 1
    except Exception as e:
        servervmsqltestvalue = 0
    result = {'servervmsqltestvalue':servervmsqltestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response



def deliislink(request):
    try:
        # dir_now = os.path.dirname(os.path.abspath("settings.py"))
        dbinfo_insert_iisvalue('None','None')
        servervmsqltestvalue = 1
    except Exception as e:
        servervmsqltestvalue = 0
    result = {'servervmsqltestvalue':servervmsqltestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

def deladlink(request):
    try:
        # dir_now = os.path.dirname(os.path.abspath("settings.py"))
        dbinfo_insert_advalue('None', 'None','None','None','None')
        servervmsqltestvalue = 1
    except Exception as e:
        servervmsqltestvalue = 0
    result = {'servervmsqltestvalue':servervmsqltestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

def delexlink(request):
    try:
        # dir_now = os.path.dirname(os.path.abspath("settings.py"))
        dbinfo_insert_exvalue('None', 'None','None','None')
        servervmsqltestvalue = 1
    except Exception as e:
        servervmsqltestvalue = 0
    result = {'servervmsqltestvalue':servervmsqltestvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def basisite(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    try:
        message=searchsendmail()
        mangerapiin=get_api('process')
        mangermess=genmangemessage()
        phonemess=genmuser()
        messagesend=sendmeasage()
        confmess=getconfiguration()
        titleshowmessage=shwotitle()
        if mangermess==None or mangermess==False :
            mangermess='fasle'
        elif mangermess['status']=='0':
            mangermshow = genmangemessageshow()
        else:
            apiurl = genmangeurl()
        if phonemess == None or phonemess == False:
            phonemess = 'fasle'
        if messagesend == None or messagesend == False:
            messagesend = 'fasle'
        if message == None or message == False:
            message = 'fasle'
        if confmess==() or confmess==False:
            confstatus='fasle'
        elif confmess[0]['internet_group']==None or confmess[0]['internet_group']=='None':
            confstatus = 'fasle'
        else:
            confmess=get_management_configuration()
            net=ast.literal_eval(confmess['internet_group'])
            wifi=ast.literal_eval(confmess['wifi_group'])
            vpn=ast.literal_eval(confmess['vpn_group'])
    except Exception as e:
        print(e)
    return render_to_response('admin/basisite.html', locals())



# Create your views here.
#邮件发送测试
def sendmailtest(request):
    post = request.POST
    inputadd = post.get("inputadd")
    myysqlusername = post.get("inputusername")
    myysqlpassword = post.get("inputpassword")
    inputserver = post.get("inputserver")
    inputtestmail = post.get("inputtestmail")
    try:
        mail=mailtest(inputadd,myysqlusername,myysqlpassword,inputserver,inputtestmail)
        if mail:
            password = encrypt_and_decode().encrypted_text(myysqlpassword)
            insert_sendmail(myysqlusername, password, inputserver, inputadd)
            mailstauts = True
        else:
            mailstauts = False
    except Exception as e:
        mailstauts=False
    result = {'status':mailstauts }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response






def mangeronelyupdate(request):
    post = request.POST
    inputpub = post.get("inputpub")
    inputgroup = post.get("inputgroup")
    inputdfs = post.get("inputdfs")
    inputnetwork = post.get("inputnetwork")
    inputvpn = post.get("inputvpn")
    try:
        mangersave=mangersqlupdate(inputpub,inputgroup,inputdfs,inputnetwork,inputvpn)
        if mangersave==():
            mailstauts = True
        else:
            mailstauts = False
    except Exception as e:
        mailstauts=False
    result = {'status':mailstauts }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#固定上级
def mangeronelysave(request):
    post = request.POST
    inputpub = post.get("inputpub")
    inputgroup = post.get("inputgroup")
    inputdfs = post.get("inputdfs")
    inputnetwork = post.get("inputnetwork")
    inputvpn = post.get("inputvpn")
    try:
        insermangerstau(0)
        mangersave=mangersql(inputpub,inputgroup,inputdfs,inputnetwork,inputvpn)
        if mangersave==():
            mailstauts = True
        else:
            mailstauts = False
    except Exception as e:
        mailstauts=False
    result = {'status':mailstauts }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#上级接口
def apimanger(request):
    post = request.POST
    apiurl = post.get("inputapiurl")
    testuer = post.get("inputestuser")
    try:
        url = apiurl + '&username=' + testuer
        data = requests.get(url)
        directorlist = data.json()
    except Exception as e:
        directorlist=False
    result = {'status':str(directorlist) }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#保存
def saveapimanger(request):
    post = request.POST
    apiurl = post.get("inputapiurl")
    try:
        messone=insermangerstau(1)
        meatwo=insert_apimanger(apiurl)
        if messone==() and meatwo==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response



def mailtest(inputadd,myysqlusername,myysqlpassword,inputserver,inputtestmail):
    # 第三方 SMTP 服务
    mail_host = inputserver # 设置服务器
    mail_user = myysqlusername # 用户名
    mail_pass = myysqlpassword  # 口令
    sender = inputadd
    receivers =  inputtestmail # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText('平台测试邮件内容', 'plain', 'utf-8')
    subject = '测试邮件主题'
    message['Subject'] = Header(subject, 'utf-8')
    message['To'] = Header(inputtestmail, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False


def delmysqlmanger(request):
    try:
        meass1=delmangeruser('getmanger')
        mess=delmanger()
        if meass1==() and mess==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def removeallgroupmemberfromadmin(request):
    try:
        log = logmanager()
        post = request.POST
        itgroupname = post.get("groupname")
        username = request.session.get('username')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        if username.lower() == "administrator":
            removeallgroupmembervalue = adapi().Initialapi("RemoveAllUserFromGroup", groupname=itgroupname)
            result = {"isSuccess": removeallgroupmembervalue['isSuccess'],
                      "message": removeallgroupmembervalue['message']}
            log.log(returnid=1, username=username, ip=ip,
                    message="清空" + itgroupname + "群组成员", returnparameters=str(removeallgroupmembervalue), issuccess=1,
                    methodname="removeallgroupmemberfromadmin", types="other")
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        return HttpResponseRedirect('/adminconfig/', request)


def addgroupmembersfromadmin(request):
    try:
        log = logmanager()
        post = request.POST
        itgroupname = post.get("groupname")
        username = request.session.get('username')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        groupmembersvalue = request.POST.get('groupmembersvalue')

        if username.lower() == "administrator":
            groupmembersvaluelist = groupmembersvalue.split("\n")
            if len(groupmembersvaluelist) == 0:
                isSuccess = False
                message = ""
                lenerrorlist = 0
                log.log(returnid=1, username=username, ip=ip,
                        message="添加" + itgroupname + "收件人权限", returnparameters=str(groupmembersvalue),
                        issuccess=1,
                        methodname="addgroupmembers", types="exchange")
            else:
                erruserlist = list()
                for i in groupmembersvaluelist:
                    if i != "":
                        memberadvalue = adapi().Initialapi_noskey("ObjectExists", objectName=i, catalog="user")
                        if memberadvalue:
                            addreturnvalue = adapi().Initialapi("AddUserToGroup", sAMAccountName=i, groupname=itgroupname)
                            log.log(returnid=1, username=username, ip=ip,
                                    message="添加" + itgroupname + "收件人权限"+str(i), returnparameters=str(addreturnvalue),
                                    issuccess=1,
                                    methodname="addgroupmembers", types="exchange")
                            if not (addreturnvalue['isSuccess']) and "对象已存在" not in addreturnvalue['message']:
                                if i not in erruserlist:
                                    erruserlist.append(i)
                        else:
                            membergroupadvalue = adapi().Initialapi_noskey("ObjectExists", objectName=i,
                                                                           catalog="group")
                            if membergroupadvalue:
                                addreturnvalue = adapi().Initialapi("AddUserToGroup", sAMAccountName=i,
                                                                    groupname=itgroupname)
                                log.log(returnid=1, username=username, ip=ip,
                                        message="添加" + itgroupname + "收件人权限" + str(i), returnparameters=str(addreturnvalue),
                                        issuccess=1,
                                        methodname="addgroupmembers", types="exchange")
                                if not (addreturnvalue['isSuccess']) and "对象已存在" not in addreturnvalue['message']:
                                    if i not in erruserlist:
                                        erruserlist.append(i)
                            else:
                                log.log(returnid=0, username=username, ip=ip,
                                        message="添加" + itgroupname + "收件人权限" + str(i), returnparameters="找不到"+str(i),
                                        issuccess=0,
                                        methodname="addgroupmembers", types="exchange")
                                if i not in erruserlist:
                                    erruserlist.append(i)
                isSuccess = True
                message = '&#10;'.join(erruserlist)
                lenerrorlist = len(erruserlist)
            result = {"isSuccess": isSuccess, "message": message, "lenerrorlist": lenerrorlist}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        return HttpResponseRedirect('/adminconfig/', request)

def delmailmemberfromadmin(request):
    try:
        log = logmanager()
        post = request.POST
        itgroupname = post.get("groupname")
        username = request.session.get('username')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        groupmembersvalue = request.POST.get('groupmembersvalue')

        if username.lower() == "administrator":
            removevalue = adapi().Initialapi("RemoveUserFromGroup",sAMAccountName=groupmembersvalue,groupname=itgroupname)
            if removevalue['isSuccess']:
                lastvalue = True
                message = ""
                log.log(returnid=1, username=username, ip=ip,
                        message="删除" + itgroupname + "群组信息成员"+str(groupmembersvalue), returnparameters=str(removevalue),
                        issuccess=1,
                        methodname="delmailmember", types="exchange")
            else:
                lastvalue = False
                message = removevalue['message']
                log.log(returnid=0, username=username, ip=ip,
                        message="删除" + itgroupname + "群组信息成员"+str(groupmembersvalue), returnparameters=str(removevalue),
                        issuccess=0,
                        methodname="delmailmember", types="exchange")
            result = {"lastvalue":lastvalue,"message":message}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        return HttpResponseRedirect('/adminconfig/', request)

#删除api
def delmysqlapi(request):
    try:
        meass1=delmangeruser('getmanger')
        mess=delapimanger('getmanger')
        if meass1==() and mess==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#删除用户转手机api
def deluserphoneapi(request):
    try:
        meass1=delmangeruser('usertophone')
        mess=delapimanger('getuserphone')
        if meass1==() and mess==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#删除短信接口
def delsendmesspi(request):
    try:
        meass1=delmangeruser('Sendmessage')
        mess=delapimanger('Sendmessage')
        if meass1==() and mess==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#删除基础配置接口
def delsqlconfig(request):
    try:
        message=delconfiger()
        if message==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#删除发送邮件
def delmailsend(request):
    try:
        message=delsendconfig()
        if message==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#用户名转手机测试
def getusermobile(request):
    post = request.POST
    apiurl = post.get("inputapiurl")
    testuer = post.get("inputestuser")
    try:
        url = apiurl + '&username=' + testuer
        data = requests.get(url)
        phoneretuen=data.json()
    except Exception as e:
        print(e)
        phoneretuen=False
    result = {'status':str(phoneretuen) }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#保存用户转手机接口
def saveusertophone(request):
    post = request.POST
    apiurl = post.get("inputapiurl")
    try:
        messone=inserphonestau(1)
        meatwo=insert_phoneurl(apiurl)
        if messone==() and meatwo==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#短信接口测试
def testmobilesend(request):
    post = request.POST
    inputphoneapi = post.get("inputphoneapi")
    inputestphone = post.get("inputestphone")
    inputesmessage = post.get("inputesmessage")
    try:
        url = inputphoneapi +'&message='+inputesmessage +'&moblie=' + inputestphone
        data = requests.get(url)
        phoneretuen = data.json()
    except Exception as e:
        print(e)
        phoneretuen=False
    result = {'status':str(phoneretuen) }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#短信接口保存
def savephonesend(request):
    post = request.POST
    apiurl = post.get("inputphoneapi")
    try:
        messone=sendmestaus(1)
        meatwo=insert_sendphone(apiurl)
        if messone==() and meatwo==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def pwdremindertips(request):
    post = request.POST
    try:
        tab = get_management_configuration()['pwdremindertips']
        if tab == '' or tab == None or tab == "false":
            status = False
        else:
            status = True
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response



def changepwdremindertips(request):
    post = request.POST
    mailgroupissendvalue = post.get("mailgroupissendvalue")
    try:
        update_management_configuration_changepwdremindertips(mailgroupissendvalue)
        status = True
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#网站标题保存
def titlesaveqsl(request):
    post = request.POST
    inputtitle = post.get("inputtitle")
    inputheard = post.get("inputheard")
    try:
        meatwo=insert_title(inputtitle,inputheard)
        if meatwo==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#网站标题更新
def titleupdateqsl(request):
    post = request.POST
    inputtitle = post.get("inputtitle")
    inputheard = post.get("inputheard")
    try:
        returnmessage=update_title(inputtitle,inputheard)
        if returnmessage==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#删除网站标题
def deltitlesql(request):
    try:
        message=deltitleconfig()
        if message==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#删除获取审批接口
def deloutapi(request):
    try:
        message=delapimanger('process')
        if message==():
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#基础信息保存
def saveallmessage(request):
    post = request.POST
    WiFiname = post.getlist("WiFiname")
    WiFilist = post.getlist("WiFilist")
    vnplist = post.getlist("vnplist")
    vpnname = post.getlist("vpnname")
    networklist = post.getlist("networklist")
    networkname = post.getlist("networkname")
    inputpubmailou = post.get("inputpubmailou")
    inputmailgroupou = post.get("inputmailgroupou")
    inputpwdlen = post.get("inputpwdlen")
    inputjzou = post.get("inputjzou")
    inputjzgroup = post.get("inputjzgroup")
    inputunlockgroup = post.get("inputunlockgroup")
    inputpubmailDB = post.get("inputpubmailDB")
    inputpubmaillanwei = post.get("inputpubmaillanwei")
    inputewge='regex:^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{'+inputpwdlen+',}$;'
    inputips='至少有'+inputpwdlen+'个字符长'
    try:
        ad_domain=dbinfo_select_global_configuration()[0]['ad_domain']
        network = list()
        vpn = list()
        wifi = list()
        for i in range(len(WiFiname)):
            wifi.append({"description":WiFiname[i],"name":WiFilist[i]})
        for i in range(len(vpnname)):
            vpn.append({"description": vpnname[i], "name": vnplist[i]})
        for i in range(len(networkname)):
            network.append({"description": networkname[i], "name": networklist[i]})
        savecon=update_config(ad_domain,str(network),str(vpn),str(wifi),inputpubmailou,inputmailgroupou,inputewge,inputips,inputjzou,inputjzgroup,inputunlockgroup,inputpubmailDB,inputpubmaillanwei,inputpwdlen)
        if savecon==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#基础信息更新
def updateconfigall(request):
    post = request.POST
    WiFiname = post.getlist("WiFiname")
    WiFilist = post.getlist("WiFilist")
    vnplist = post.getlist("vnplist")
    vpnname = post.getlist("vpnname")
    networklist = post.getlist("networklist")
    networkname = post.getlist("networkname")
    inputpubmailou = post.get("inputpubmailou")
    inputmailgroupou = post.get("inputmailgroupou")
    inputpwdlen = post.get("inputpwdlen")
    inputjzou = post.get("inputjzou")
    inputjzgroup = post.get("inputjzgroup")
    inputunlockgroup = post.get("inputunlockgroup")
    inputpubmailDB = post.get("inputpubmailDB")
    inputpubmaillanwei = post.get("inputpubmaillanwei")
    inputewge='regex:^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{'+inputpwdlen+',}$;'
    inputips='至少有'+inputpwdlen+'个字符长'
    try:
        ad_domain=dbinfo_select_global_configuration()[0]['ad_domain']
        network = list()
        vpn = list()
        wifi = list()
        for i in range(len(WiFiname)):
            wifi.append({"description":WiFiname[i],"name":WiFilist[i]})
        for i in range(len(vpnname)):
            vpn.append({"description": vpnname[i], "name": vnplist[i]})
        for i in range(len(networkname)):
            network.append({"description": networkname[i], "name": networklist[i]})
        savecon=update_config(ad_domain,str(network),str(vpn),str(wifi),inputpubmailou,inputmailgroupou,inputewge,inputips,inputjzou,inputjzgroup,inputunlockgroup,inputpubmailDB,inputpubmaillanwei,inputpwdlen)
        if savecon==():
            status=True
        else:
            status=False
    except Exception as e:
        status=False
    result = {'status':status }
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response
#审批流接口测试
def testapinprocess(request):
    post = request.POST
    inputhasapion = post.get("inputhasapion")
    inputuseron = {"status": 0, "message": {"id": "1", "username": "测试", "displayname": "测试", "types": "测试", "applytype": "测试",
                              "applydetail": "测试"}}
    try:
        url = inputhasapion
        value = json.dumps(inputuseron)
        headers = {
            "Content-Type": "application/json"
        }
        r = requests.post(url, data=value, headers=headers)
        status = r.json()
    except Exception as e:
        status=False
    result = {'status':str(status)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#审批流接口保存
def savemangeapiin(request):
    post = request.POST
    inputhasapion = post.get("inputhasapion")
    try:
        message = insert_api(inputhasapion,'process')
        if message:
            status = True
        else:
            status = False
    except Exception as e:
        status=False
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response