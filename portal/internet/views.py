# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 16:44
# @Author  :
import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from adapi.ad_api import adapi, getmanger
from adapi.dbinfo import insert_pubmailflow, updatepumailuser, insert_pubmailflow_process
from dfs.dbinfo import *
from dfs.thr_process import process_outgoing
from logmanager.views import logmanager
import ast

#网络权限申请页面
from sendmail.sendmail import send_email_by_template


def access(request):
    try:
        username = request.session.get('username')
        displayname = request.session.get('displayname')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        if username:
            internet_group_now = []
            wifi_group_now = []
            vpn_group_now = []
            internet_group_now_des = []
            wifi_group_now_des = []
            vpn_group_now_des = []
            internet_group_list = []
            wifi_group_list = []
            vpn_group_list = []
            get_management_configurations = get_management_configuration()
            if get_management_configurations :
                if get_management_configurations.get('internet_group',''):
                    internet_group_list= ast.literal_eval(get_management_configurations.get('internet_group','').replace("true", "'true'").replace("false", "'false'").replace("null", "'null'")) #上网权限，
                if get_management_configurations.get('wifi_group', ''):
                    wifi_group_list = ast.literal_eval(get_management_configurations.get('wifi_group', '').replace("true", "'true'").replace("false", "'false'").replace("null", "'null'")) #无线权限
                if get_management_configurations.get('vpn_group', ''):
                    vpn_group_list = ast.literal_eval(get_management_configurations.get('vpn_group', '').replace("true", "'true'").replace("false", "'false'").replace("null", "'null'"))  #VPN权限
                #确定用户权限
                #获取用户属性
                GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=username, objectClass='user')
                if GetobjectPropertys['isSuccess']:
                    memberof = GetobjectPropertys['message'][0].get("memberof", '')
                    if memberof:
                        for member in memberof:
                            for internet_group in internet_group_list:
                                internet_group_name = internet_group.get("name",'')
                                internet_group_cn = "CN=" + str(internet_group_name) + ","
                                if internet_group_cn in member:
                                    internet_group_now.append(internet_group)
                            for wifi_group in wifi_group_list:
                                wifi_group_name = wifi_group.get("name",'')
                                wifi_group_cn = "CN=" + str(wifi_group_name) + ","
                                if wifi_group_cn in member:
                                    wifi_group_now.append(wifi_group)
                            for vpn_group in vpn_group_list:
                                vpn_group_name = vpn_group.get("name",'npne')
                                vpn_group_cn = "CN=" + str(vpn_group_name) + ","
                                if vpn_group_cn in member:
                                    vpn_group_now.append(vpn_group)
                if internet_group_list and internet_group_now:
                    for internet_group_now_str in internet_group_now:
                        internet_group_now_des.append(internet_group_now_str.get("description",''))
                        # internet_group_list.remove(internet_group_now_str)
                if wifi_group_list and wifi_group_now:
                    for wifi_group_now_str in wifi_group_now:
                        wifi_group_now_des.append(wifi_group_now_str.get("description", ''))
                        # wifi_group_list.remove(wifi_group_now_str)
                if vpn_group_list and vpn_group_now:
                    for vpn_group_now_str in vpn_group_now:
                        vpn_group_now_des.append(vpn_group_now_str.get("description", ''))
                        # vpn_group_list.remove(vpn_group_now_str )

            return render_to_response('internetweb/access.html', locals())
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        logmanager().log(returnid=0, username=username, ip=ip, message="access,网络权限申请页面："+str(e), issuccess=0, methodname="access",returnparameters = str(request.POST), types="internet")
        return HttpResponseRedirect('/', request)

# 申请网络权限
def saveInternet(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    old_internet_now = request.POST.get('old_internet_now',"") #旧权限组可为空
    new_internet = request.POST.get('new_internet',"") #新权限组，不可为空
    type_internet = request.POST.get('type_internet', "")  # 权限类型，不可为空
    if username:
        try:
            if new_internet and type_internet:
                types = 'internet'
                if type_internet =="access":
                    manger = getmanger(username, "networkmanger")
                    applytype = "申请上网权限组权限"
                elif type_internet =="wifi":
                    manger = getmanger(username, "networkmanger")
                    applytype = "申请无线权限组权限"
                elif type_internet =="vpn":
                    manger = getmanger(username, "vnpmanger")
                    applytype = "申请VPN权限组权限"
                else:
                    manger = getmanger(username, "networkmanger")
                    applytype = "申请权限组权限"
                process = get_api("process")
                message = str({'old_internet_now': old_internet_now, "new_internet": new_internet, "type_internet": type_internet, "username": username})
                if process:
                    insert_pubmailflow_processs = insert_pubmailflow_process(ip, username, displayname, types, applytype, new_internet, director='系统', message=message)
                    if insert_pubmailflow_processs:
                        value = {"status": 0,
                                 "message": {"id": insert_pubmailflow_processs['id'], "username": username, "displayname": displayname, "types": types, "applytype": applytype, "applydetail": new_internet}}
                        process_outgoings = process_outgoing(value)
                        if process_outgoings['status']==0:
                            result = {'isSuccess': True, "message": "权限申请成功"}
                        else:
                            result = {'isSuccess': False, "message": "插入数据库,调用流程接口失败"}
                    else:
                        result = {'isSuccess': False, "message": "未能插入数据库"}
                elif manger:
                    insert_pubmailflowds = insert_pubmailflow(ip, username, displayname, types, applytype, new_internet, director=manger, message=message)
                    if insert_pubmailflowds==():#申请权限插入数据库成功
                        mangervalue = adapi().Initialapi("GetobjectProperty", objects=manger, objectClass="user")
                        if mangervalue['isSuccess']:
                            subject = u'您有一个新申请单待审批'
                            submit_time = datetime.now()
                            emaillists = [{"username":username,"displayname":displayname,"applytype":applytype,"new_internet":new_internet,"submit_time":submit_time}]
                            email_data = {'emaillists': emaillists,"username":username}
                            template = "internetweb/interdirectoremail.html"
                            to_list = [mangervalue['message'][0]['mail']]
                            send_email_by_template(subject, template, email_data, to_list)
                        result = {'isSuccess': True, "message": "权限申请成功"}
                    else:
                        result = {'isSuccess': False, "message": "未能插入数据库"}
                else:
                    result = {'isSuccess': False, "message": "没有获取到主管"}
            else:
                result = {'isSuccess': False, "message": "传入空值"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="saveInternet,申请网络权限：", issuccess=0, methodname="saveInternet", returnparameters=str(request.POST),
                                 types="internet")
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="saveInternet,申请网络权限：" + str(e), issuccess=0, methodname="saveInternet", returnparameters=str(request.POST),
                             types="internet")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#主管审批同意网络权限
def allowtobeIntrenet(id,message):
    try:
        if id and message:
            message_dict=ast.literal_eval(message)
            old_internet_now = message_dict.get("old_internet_now",'')
            new_internet = message_dict.get("new_internet", '')
            message_username = message_dict.get("username", '')
            if new_internet:
                if old_internet_now:
                    for old_internet_dict in ast.literal_eval(old_internet_now.replace("true","'true'").replace("false","'false'").replace("null","'null'")):
                        if old_internet_dict.get("name",''):
                            RemoveUserFromGroups = adapi().Initialapi("RemoveUserFromGroup", sAMAccountName=message_username, groupname=old_internet_dict.get("name",''))
                AddUserToGroups = adapi().Initialapi("AddUserToGroup", sAMAccountName=message_username, groupname=new_internet)
                if AddUserToGroups['isSuccess'] or ("对象已存在" in AddUserToGroups['message']):
                    updatepumailuser(id, 1)
                    result = {'isSuccess': True, "message": "主管审批同意网络权限"}
                else:
                    updatepumailuser(id, 2)
                    result = {'isSuccess': False, "message": "主管审批同意网络权限,加组失败"}
            else:
                updatepumailuser(id, 2)
                result = {'isSuccess': False, "message": "主管审批同意网络权限,传入空值"}
        else:
            result = {'isSuccess': False, "message": "主管审批同意网络权限,传入空值"}
        if not result['isSuccess']:
            logmanager().log(returnid=2, username='系统', ip='172.0.0.0', message="allowtobeIntrenet,主管审批同意网络权限：", issuccess=0, methodname=id, returnparameters=str(message),
                             types="internet")
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
        logmanager().log(returnid=0, username='系统', ip='172.0.0.0', message="allowtobeIntrenet,主管审批同意网络权限：" + str(e), issuccess=0, methodname=id, returnparameters=str(message),
                         types="internet")
    return result