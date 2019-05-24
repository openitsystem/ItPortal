
import json
from django.http import HttpResponse
from django.shortcuts import  render_to_response,HttpResponseRedirect
from threading import Thread
from adapi.dbinfo import searchmind, get_domain, get_PermissionsGrops
from adapi.pwd import genpwd
from dfs.dbinfo import get_management_configuration
from sendmail.sendmail import send_email_by_template
from tools.delpwdnolock import delpwdnolock, adapi,  ObjectExist, GetobjectProperty, VerifyUserLogin,UnlockAccount, AddUserToGroup, \
    dbinfo_select_global_configuration
from logmanager.views import logmanager
# Create your views here.
#更改密码页面



def changepwd(request):
    username = request.session.get('username')
    mailaddress = request.session.get('mail')
    displayname = request.session.get('displayname')
    tab=get_management_configuration()
    return render_to_response('tools/changepwd.html', locals())





def resetpwd(request):
    username = request.session.get('username')
    mailaddress = request.session.get('mail')
    displayname = request.session.get('displayname')
    return render_to_response('tools/resetpwd.html', locals())

def checkgroupmanager(groupmanager,DN):
    try:
        ismanager = False
        if groupmanager and 'isSuccess' in groupmanager:
            if groupmanager['isSuccess']:
                #防止越权
                if groupmanager['message']['managedBy'] == DN:
                    ismanager = True
    except Exception as e:
        ismanager = False
    return ismanager

def managershowsendtomailgroup(request):
    try:
        username = request.session.get('username')
        DN = request.session.get('DN')
        groupname = request.GET.get('groupname')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager,DN)
        if ismanager:
            groupdisplayname = groupmanager['message']['displayname']
            return render_to_response('mail/managershowsendtomailgroup.html', locals())
        else:
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/mailgroupmanagement/', request)



def managershowmailgroup(request):
    try:
        username = request.session.get('username')
        DN = request.session.get('DN')
        groupname = request.GET.get('groupname')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager,DN)
        if ismanager:
            groupdisplayname = groupmanager['message']['displayname']
            return render_to_response('mail/managershowmailgroup.html', locals())
        else:
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        return HttpResponseRedirect('/mailgroupmanagement/', request)



def mailgroupmanagement(request):
    username = request.session.get('username')
    mailaddress = request.session.get('mail')
    displayname = request.session.get('displayname')
    distinguishedName = request.session.get('distinguishedName')
    return render_to_response('mail/mailgroupmanagement.html', locals())



def searchuserbydn(request):
    userdn = request.POST.get('name')
    value = request.POST.get('value')
    uservalue = adapi().Initialapi('GetPropertyFordistinguishedName',distinguishedName=userdn)
    result = {'value':uservalue['message'][0][value]}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


class MyThread(Thread):

    def __init__(self, parameter1):
        Thread.__init__(self)
        self.parameter1 = parameter1

    def run(self):
        self.result1  = adapi().Initialapi('GetPropertyFordistinguishedName', distinguishedName=self.parameter1)
        self.result = (self.result1)['message'][0]


    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def getmailgroupsendto(request):
    log = logmanager()
    groupname = request.POST.get('name')
    username = request.session.get('username')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        mailgroupvalue = adapi().Initialapi("GetDistributionGroup",pyname=groupname,pyvalue="AcceptMessagesOnlyFromSendersOrMembers")
        if mailgroupvalue['message'][0] == "{'daname':''}":
            result = False
        else:
            result = True
        log.log(returnid=1,username=username,ip=ip,message="查询"+groupname+"是否限制发件权限"+str(mailgroupvalue), issuccess=1,methodname="getmailgroupsendto", types="exchange")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    except Exception as e:
        result = False
        log.log(returnid=0,username=username,ip=ip,message="查询"+groupname+"是否限制发件权限"+str(e), issuccess=0,methodname="getmailgroupsendto", types="exchange")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response

#管理者展示群组发件人权限列表
def showmailsendtogroupmembers(request):
    log = logmanager()
    username = request.session.get('username')
    groupname = request.GET.get('groupname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        DN = request.session.get('DN')
        groupmanagergroup = adapi().Initialapi('GetDistributionGroupSendto', pyname=groupname,pyvalue="AcceptMessagesOnlyFromDLMembers")
        groupmanageruser = adapi().Initialapi('GetDistributionGroupSendto', pyname=groupname,pyvalue="AcceptMessagesOnlyFrom")
        lastvalue = list()
        if groupmanagergroup['isSuccess'] and groupmanageruser['isSuccess']:
            for uservalue in groupmanageruser['message']:
                aa = adapi().Initialapi("GetMailBox",mailname=uservalue)
                if aa['isSuccess']:
                    lastvalue.append(aa['message'][0])
            for groupvalue in groupmanagergroup['message']:
                bb = adapi().Initialapi("GetDistributionGroupselect",pyname=groupvalue)
                if bb['isSuccess']:
                    lastvalue.append(bb['message'][0])
            a = {"total": len(lastvalue), "rows": lastvalue}
            log.log(returnid=1,username=username,ip=ip,message="查询"+groupname+"发件权限列表"+str(groupmanagergroup)+str(groupmanageruser), issuccess=1,methodname="showmailsendtogroupmembers", types="exchange")
            return HttpResponse(json.dumps(a))
        else:
            log.log(returnid=0,username=username,ip=ip,message="查询"+groupname+"发件权限列表"+str(groupmanagergroup)+str(groupmanageruser), issuccess=0,methodname="showmailsendtogroupmembers", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="查询" + groupname + "发件权限列表" + str(e), issuccess=0,
                methodname="showmailsendtogroupmembers", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)


#管理者删除群组发件权限组成员
def delmailsendtomember(request):
    log = logmanager()
    groupname = request.POST.get('groupname')
    PrimarySmtpAddress = request.POST.get('PrimarySmtpAddress')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            adapi().Initialapi("SetDistributionGroupaddremove",mailname=groupname,projectname1="AcceptMessagesOnlyFrom",id=PrimarySmtpAddress,todo="remove")
            adapi().Initialapi("SetDistributionGroupaddremove",mailname=groupname,projectname1="AcceptMessagesOnlyFromDLMembers",id=PrimarySmtpAddress,todo="remove")
            lastvalue = 1
            log.log(returnid=1,username=username,ip=ip,message="删除"+groupname+"发件权限列表成员"+str(PrimarySmtpAddress), issuccess=1,methodname="delmailsendtomember", types="exchange")

            result = {"lastvalue":lastvalue}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0,username=username,ip=ip,returnparameters="越权！",message="删除"+groupname+"发件权限列表成员"+str(PrimarySmtpAddress), issuccess=0,methodname="delmailsendtomember", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="删除"+groupname+"发件权限列表成员"+str(PrimarySmtpAddress), returnparameters=str(e),issuccess=0,
                methodname="showmailsendtogroupmembers", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#删除群组
def delmailgroup(request):
    log = logmanager()
    groupname = request.POST.get('groupname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            changegroupdisplaynamevalue = adapi().Initialapi("delgroupbyname",groupname=groupname)
            if changegroupdisplaynamevalue['isSuccess']:
                isSuccess = True
                message = ""
                log.log(returnid=1, username=username, ip=ip,
                        message="删除"+groupname+"群组", returnparameters=str(changegroupdisplaynamevalue),issuccess=1,
                        methodname="delmailgroup", types="exchange")
                groupmessagevalue = adapi().Initialapi("GetobjectProperty", objects=username, objectClass="user")
                subject = u'邮箱群组删除通知'
                emaillists = '您已经删除邮箱群组:' + str(groupname) + '！ '
                email_data = {'emaillists': emaillists}
                template = "mailmould/sendmailpassword.html"
                to_list = [groupmessagevalue['message'][0]['mail']]
                send_email_by_template(subject, template, email_data, to_list)
            else:
                isSuccess = False
                log.log(returnid=0, username=username, ip=ip,
                        message="删除"+groupname+"群组", returnparameters=str(changegroupdisplaynamevalue),issuccess=0,
                        methodname="delmailgroup", types="exchange")
                message = changegroupdisplaynamevalue['message']
            result = {"isSuccess":isSuccess,"message":message}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="删除"+groupname+"群组", returnparameters=str("越权"),issuccess=0,
                    methodname="delmailgroup", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="删除"+groupname+"群组", returnparameters=str(e),issuccess=0,
                methodname="delmailgroup", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#更改群组是否开启身份认证
def changemailgrouphasoutvalue(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    mailgroupissendvalue = request.POST.get('mailgroupissendvalue')
    groupsamaccountvalues = request.POST.get('groupsamaccountvalues')
    try:
        groupemailvalue = request.POST.get('groupemailvalue')
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupsamaccountvalues)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            changegroupdisplaynamevalue = adapi().Initialapi("SetDistributionGroupbybool",Identity=groupsamaccountvalues,pyname="RequireSenderAuthenticationEnabled",pyvalue=mailgroupissendvalue)
            if changegroupdisplaynamevalue['isSuccess']:
                isSuccess = True
                message = ""
                log.log(returnid=1, username=username, ip=ip,
                        message="设置"+groupsamaccountvalues+"群组身份认证"+str(mailgroupissendvalue), returnparameters=str(changegroupdisplaynamevalue),issuccess=1,
                        methodname="changemailgrouphasoutvalue", types="exchange")
            else:
                isSuccess = False
                message = changegroupdisplaynamevalue['message']
                log.log(returnid=0, username=username, ip=ip,
                        message="设置"+groupsamaccountvalues+"群组身份认证"+str(mailgroupissendvalue), returnparameters=str(changegroupdisplaynamevalue),issuccess=0,
                        methodname="changemailgrouphasoutvalue", types="exchange")
            result = {"isSuccess":isSuccess,"message":message}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="设置"+groupsamaccountvalues+"群组身份认证"+str(mailgroupissendvalue), returnparameters="越权！",issuccess=0,
                    methodname="changemailgrouphasoutvalue", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="设置"+groupsamaccountvalues+"群组身份认证"+str(mailgroupissendvalue), returnparameters=str(e),issuccess=0,
                methodname="changemailgrouphasoutvalue", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#更改群组显示名称
def changemailgroupdisplaynamevalue(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    groupdisplaynamevalue = (request.POST.get('groupdisplaynamevalue')).replace(" ","")
    groupsamaccountvalues = request.POST.get('groupsamaccountvalues')
    try:
        groupemailvalue = request.POST.get('groupemailvalue')
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupsamaccountvalues)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            changegroupdisplaynamevalue = adapi().Initialapi("SetobjectProperty",objects=groupsamaccountvalues,objectClass="group",PropertyName="displayName",PropertyValue=groupdisplaynamevalue)
            if changegroupdisplaynamevalue['isSuccess']:
                isSuccess = True
                message = ""
                log.log(returnid=1, username=username, ip=ip,
                        message="设置"+groupsamaccountvalues+"群组显示名称"+str(groupdisplaynamevalue), returnparameters=str(changegroupdisplaynamevalue),issuccess=1,
                        methodname="changemailgroupdisplaynamevalue", types="exchange")
            else:
                isSuccess = False
                message = changegroupdisplaynamevalue['message']['message']
                log.log(returnid=0, username=username, ip=ip,
                        message="设置"+groupsamaccountvalues+"群组显示名称"+str(groupdisplaynamevalue), returnparameters=str(changegroupdisplaynamevalue),issuccess=0,
                        methodname="changemailgroupdisplaynamevalue", types="exchange")
            result = {"isSuccess":isSuccess,"message":message}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="设置"+groupsamaccountvalues+"群组显示名称"+str(groupdisplaynamevalue), returnparameters="越权！",issuccess=0,
                    methodname="changemailgroupdisplaynamevalue", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="设置"+groupsamaccountvalues+"群组显示名称"+str(groupdisplaynamevalue), returnparameters=str(e),issuccess=0,
                methodname="changemailgroupdisplaynamevalue", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#转移管理者权限
def changemailgroupamanagerhangevalue(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    managerinputvalue = request.POST.get('managerinputvalue')
    groupsamaccountvalues = request.POST.get('groupsamaccountvalues')
    try:
        groupemailvalue = request.POST.get('groupemailvalue')
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupsamaccountvalues)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            managerDNvalue = adapi().Initialapi("GetobjectProperty",objects=managerinputvalue,objectClass="user")
            if managerDNvalue['isSuccess']:
                changegroupdisplaynamevalue = adapi().Initialapi("SetobjectProperty", objects=groupsamaccountvalues,
                                                                 objectClass="group", PropertyName="managedBy",
                                                                 PropertyValue=managerDNvalue['message'][0]['distinguishedName'])
                if changegroupdisplaynamevalue['isSuccess']:
                    isSuccess = True
                    message = ""
                    log.log(returnid=1, username=username, ip=ip,
                            message="设置"+str(groupsamaccountvalues)+"群组管理者"+str(managerinputvalue), returnparameters=str(changegroupdisplaynamevalue),issuccess=1,
                            methodname="changemailgroupamanagerhangevalue", types="exchange")
                    subject = u'邮箱群组管理者权限变更'
                    emaillists = '您已经拥有邮箱群组:' + str(groupsamaccountvalues) + '的权限,如果想要维护邮箱群组，请登录平台！ '
                    email_data = {'emaillists': emaillists}
                    template = "mailmould/sendmailpassword.html"
                    to_list = [managerDNvalue['message'][0]['mail']]
                    send_email_by_template(subject, template, email_data, to_list)
                else:
                    isSuccess = False
                    message = changegroupdisplaynamevalue['message']['message']
                    log.log(returnid=0, username=username, ip=ip,
                            message="设置"+groupsamaccountvalues+"群组管理者"+str(managerinputvalue), returnparameters=str(changegroupdisplaynamevalue),issuccess=0,
                            methodname="changemailgroupamanagerhangevalue", types="exchange")
            else:
                isSuccess = False
                message = "找不到"+managerinputvalue
                logmanager().log(returnid=0, username=username, ip=ip,
                                 message="设置"+groupsamaccountvalues+"群组管理者"+str(managerinputvalue), returnparameters=str(message),issuccess=0,
                                 methodname="changemailgroupamanagerhangevalue", types="exchange")
            result = {"isSuccess": isSuccess, "message": message}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="设置"+groupsamaccountvalues+"群组管理者"+str(managerinputvalue), returnparameters="越权！",issuccess=0,
                    methodname="changemailgroupamanagerhangevalue", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="设置"+groupsamaccountvalues+"群组管理者"+str(managerinputvalue), returnparameters=str(e),issuccess=0,
                methodname="changemailgroupamanagerhangevalue", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#清空所有群组成员
def removeallgroupmember(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    groupname = request.POST.get('groupname')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            removeallgroupmembervalue = adapi().Initialapi("RemoveAllUserFromGroup", groupname=groupname)
            result = {"isSuccess": removeallgroupmembervalue['isSuccess'],
                      "message": removeallgroupmembervalue['message']}
            log.log(returnid=1, username=username, ip=ip,
                    message="清空"+groupname+"群组成员", returnparameters=str(removeallgroupmembervalue),issuccess=1,
                    methodname="removeallgroupmember", types="exchange")
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="清空"+groupname+"群组成员", returnparameters="越权！",issuccess=0,
                    methodname="removeallgroupmember", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="清空"+groupname+"群组成员", returnparameters=str(e),issuccess=0,
                methodname="removeallgroupmember", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#清空群组发件人权限
def removeallsnedtogroupmember(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    groupname = request.POST.get('groupname')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            removeallgroupmembervalue = adapi().Initialapi("SetDistributionGroup", Identity=groupname,
                                                           pyname="AcceptMessagesOnlyFromSendersOrMembers",
                                                           pyvalue="")
            result = {"isSuccess": removeallgroupmembervalue['isSuccess'],
                      "message": removeallgroupmembervalue['message']}
            log.log(returnid=1, username=username, ip=ip,
                    message="清空"+groupname+"发件人权限", returnparameters=str(removeallgroupmembervalue),issuccess=1,
                    methodname="removeallsnedtogroupmember", types="exchange")

            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="清空"+groupname+"发件人权限", returnparameters="越权！",issuccess=0,
                    methodname="removeallsnedtogroupmember", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="清空"+groupname+"发件人权限", returnparameters=str(e),issuccess=0,
                methodname="removeallsnedtogroupmember", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#添加发件人权限
def addgroupsendtomembers(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    groupname = request.POST.get('groupname')
    groupmembersvalue = request.POST.get('groupmembersvalue')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            groupmembersvaluelist = groupmembersvalue.split("\n")
            if len(groupmembersvaluelist) == 0:
                isSuccess = False
                message = ""
                lenerrorlist = 0
                log.log(returnid=1, username=username, ip=ip,
                        message="添加"+groupname+"发件人权限", returnparameters=str(groupmembersvalue),issuccess=1,
                        methodname="addgroupsendtomembers", types="exchange")
            else:
                erruserlist = list()
                for i in groupmembersvaluelist:
                    if i != "":
                        memberadvalue = adapi().Initialapi_noskey("ObjectExists", objectName=i, catalog="user")
                        if memberadvalue:
                            addreturnvalue = adapi().Initialapi("SetDistributionGroupaddremove", id=i,
                                                                mailname=groupname,
                                                                projectname1="AcceptMessagesOnlyFrom", todo="add")
                            log.log(returnid=1, username=username, ip=ip,
                                    message="添加" + groupname + "发件人权限"+i, returnparameters=str(addreturnvalue),
                                    issuccess=1,
                                    methodname="addgroupsendtomembers", types="exchange")
                            if not (addreturnvalue['isSuccess']):
                                if i not in erruserlist:
                                    erruserlist.append(i)
                        else:
                            membergroupadvalue = adapi().Initialapi_noskey("ObjectExists", objectName=i,
                                                                           catalog="group")
                            if membergroupadvalue:
                                addreturnvalue = adapi().Initialapi("SetDistributionGroupaddremove", id=i,
                                                                    mailname=groupname,
                                                                    projectname1="AcceptMessagesOnlyFromDLMembers",
                                                                    todo="add")
                                log.log(returnid=1, username=username, ip=ip,
                                        message="添加" + groupname + "发件人权限" + i, returnparameters=str(addreturnvalue),
                                        issuccess=1,
                                        methodname="addgroupsendtomembers", types="exchange")
                                if not (addreturnvalue['isSuccess']):
                                    if i not in erruserlist:
                                        erruserlist.append(i)
                            else:
                                log.log(returnid=0, username=username, ip=ip,
                                        message="添加" + groupname + "发件人权限"+i, returnparameters="找不到"+i,
                                        issuccess=0,
                                        methodname="addgroupsendtomembers", types="exchange")
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
            log.log(returnid=0, username=username, ip=ip,
                    message="添加" + groupname + "发件人权限"+str(groupmembersvalue), returnparameters="越权！",
                    issuccess=0,
                    methodname="addgroupsendtomembers", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="添加" + groupname + "发件人权限"+str(groupmembersvalue), returnparameters=str(e),
                issuccess=0,
                methodname="addgroupsendtomembers", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

#添加收件人权限
def addgroupmembers(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    groupname = request.POST.get('groupname')
    groupmembersvalue = request.POST.get('groupmembersvalue')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            groupmembersvaluelist = groupmembersvalue.split("\n")
            if len(groupmembersvaluelist) == 0:
                isSuccess = False
                message = ""
                lenerrorlist = 0
                log.log(returnid=1, username=username, ip=ip,
                        message="添加" + groupname + "收件人权限", returnparameters=str(groupmembersvalue),
                        issuccess=1,
                        methodname="addgroupmembers", types="exchange")
            else:
                erruserlist = list()
                for i in groupmembersvaluelist:
                    if i != "":
                        memberadvalue = adapi().Initialapi_noskey("ObjectExists", objectName=i, catalog="user")
                        if memberadvalue:
                            addreturnvalue = adapi().Initialapi("AddUserToGroup", sAMAccountName=i, groupname=groupname)
                            log.log(returnid=1, username=username, ip=ip,
                                    message="添加" + groupname + "收件人权限"+str(i), returnparameters=str(addreturnvalue),
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
                                                                    groupname=groupname)
                                log.log(returnid=1, username=username, ip=ip,
                                        message="添加" + groupname + "收件人权限" + str(i), returnparameters=str(addreturnvalue),
                                        issuccess=1,
                                        methodname="addgroupmembers", types="exchange")
                                if not (addreturnvalue['isSuccess']) and "对象已存在" not in addreturnvalue['message']:
                                    if i not in erruserlist:
                                        erruserlist.append(i)
                            else:
                                log.log(returnid=0, username=username, ip=ip,
                                        message="添加" + groupname + "收件人权限" + str(i), returnparameters="找不到"+str(i),
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
            log.log(returnid=0, username=username, ip=ip,
                    message="添加" + groupname + "收件人权限" + str(groupmembersvalue), returnparameters="越权！",
                    issuccess=0,
                    methodname="addgroupmembers", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="添加" + groupname + "收件人权限" + str(groupmembersvalue), returnparameters=str(e),
                issuccess=0,
                methodname="addgroupmembers", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)


def getmailgroupvalue(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    groupname = request.POST.get('groupname')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            # 暂时取消获取发件人权限
            # if  (adapi().Initialapi('GetDistributionGroup', pyname=groupname,pyvalue="AcceptMessagesOnlyFromSendersOrMembers"))["message"][0] == "{'daname':''}":
            #     AcceptMessagesOnlyFromSendersOrMembers = 0
            # else:
            #     AcceptMessagesOnlyFromSendersOrMembers = 1
            if  (adapi().Initialapi('GetDistributionGroup', pyname=groupname,pyvalue="RequireSenderAuthenticationEnabled"))["message"][0] == "{'daname':'False'}":
                RequireSenderAuthenticationEnabled = False
            else:
                RequireSenderAuthenticationEnabled = True
            managervalue = adapi().Initialapi("GetPropertyFordistinguishedName",distinguishedName=groupmanager['message']['managedBy'])
            if managervalue['isSuccess']:
                managerusername = managervalue['message'][0]['sAMAccountName']
            else:
                managerusername = "空"
            result = {"managerusername":managerusername,"sAMAccountName":groupmanager['message']['sAMAccountName'],"displayname":groupmanager['message']['displayname'],"mail":groupmanager['message']['mail'],"RequireSenderAuthenticationEnabled":RequireSenderAuthenticationEnabled}
            log.log(returnid=1, username=username, ip=ip,
                    message="管理者获取" + groupname + "群组信息", returnparameters=str(result),
                    issuccess=1,
                    methodname="getmailgroupvalue", types="exchange")
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=username, ip=ip,
                    message="管理者获取" + groupname + "群组信息", returnparameters="越权！",
                    issuccess=0,
                    methodname="getmailgroupvalue", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=username, ip=ip,
                message="管理者获取" + groupname + "群组信息", returnparameters=str(e),
                issuccess=0,
                methodname="getmailgroupvalue", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)

def delmailmember(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    usernameaccount = request.session.get('username')
    groupname = request.POST.get('groupname')
    username = request.POST.get('username')
    try:
        DN = request.session.get('DN')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
            removevalue = adapi().Initialapi("RemoveUserFromGroup",sAMAccountName=username,groupname=groupname)
            if removevalue['isSuccess']:
                lastvalue = True
                message = ""
                log.log(returnid=1, username=usernameaccount, ip=ip,
                        message="删除" + groupname + "群组信息成员"+str(username), returnparameters=str(removevalue),
                        issuccess=1,
                        methodname="delmailmember", types="exchange")
            else:
                lastvalue = False
                message = removevalue['message']
                log.log(returnid=0, username=usernameaccount, ip=ip,
                        message="删除" + groupname + "群组信息成员"+str(username), returnparameters=str(removevalue),
                        issuccess=0,
                        methodname="delmailmember", types="exchange")
            result = {"lastvalue":lastvalue,"message":message}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            log.log(returnid=0, username=usernameaccount, ip=ip,
                    message="删除" + groupname + "群组信息成员"+str(username), returnparameters="越权！",
                    issuccess=0,
                    methodname="delmailmember", types="exchange")
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        log.log(returnid=0, username=usernameaccount, ip=ip,
                message="删除" + groupname + "群组信息成员" + str(username), returnparameters=str(e),
                issuccess=0,
                methodname="delmailmember", types="exchange")
        return HttpResponseRedirect('/mailgroupmanagement/', request)



def showmailgroupmembers(request):
    try:
        username = request.session.get('username')
        DN = request.session.get('DN')
        groupname = request.GET.get('groupname')
        groupmanager = adapi().Initialapi('Showgroupname', groupname=groupname)
        ismanager = checkgroupmanager(groupmanager, DN)
        if ismanager:
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
            return HttpResponseRedirect('/mailgroupmanagement/', request)
    except Exception as e:
        return HttpResponseRedirect('/mailgroupmanagement/', request)



#管理者展示权限下的邮箱群组
def showmailgroup(request):
    DN = request.session.get('DN')
    allgroupvalue = adapi().Initialapi('ShowgroupnamebymanagedBy',managedBy=DN)
    rows = list()
    if allgroupvalue['isSuccess']:
        if len(allgroupvalue['message']) != 0:
            for i in allgroupvalue['message']:
                rows.append({'displayname':i['Properties']['displayname'],'mail':i['Properties']['mail'],'samaccountname':i['Properties']['samaccountname']})
    rerturnvalue = {"total": len(rows), "rows": rows}
    return HttpResponse(json.dumps(rerturnvalue))




#更改密码方法
def userpwdchange(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    psw1 = request.POST.get('psw1')
    psw2 = request.POST.get('psw2')
    try:
        if psw1==psw2:
            message=adapi().Initialapi('ResetPasswordByOU', username=username,newpassword=psw1)
            if message['isSuccess']:
                log.log(returnid=1, username=username, ip=ip,
                        message= username + "修改密码" , returnparameters='密码修改成功',
                        issuccess=1,
                        methodname="userpwdchange", types="AD")
            else:
                log.log(returnid=0, username=username, ip=ip,
                        message=username + "修改密码", returnparameters=str(message),
                        issuccess=0,
                        methodname="userpwdchange", types="AD")
        else:
            message = {'message': {'message': '俩次密码不一致。'}, 'isSuccess': False}
            log.log(returnid=0, username=username, ip=ip,
                    message=username + "修改密码", returnparameters=str(message),
                    issuccess=0,
                    methodname="userpwdchange", types="AD")
    except Exception as e:
        message = {'message': {'message': '异常。'}, 'isSuccess': False}
        log.log(returnid=0, username=username, ip=ip,
                message=username + "修改密码", returnparameters=str(e),
                issuccess=0,
                methodname="userpwdchange", types="AD")
        print(e)
    result = message
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#重置密码方法
def usersetchange(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    try:
        passwd=genpwd()
        message=adapi().Initialapi('ResetPasswordByOU', username=username,newpassword=passwd)
        if message['isSuccess']:
            log.log(returnid=1, username=username, ip=ip,
                    message=username + "重置密码", returnparameters='密码修改成功',
                    issuccess=1,
                    methodname="usersetchange", types="AD")
        else:
            message = {'message': {'message': '重置密码出现错误'}, 'isSuccess': False}
            log.log(returnid=0, username=username, ip=ip,
                    message=username + "重置密码", returnparameters=str(message),
                    issuccess=0,
                    methodname="usersetchange", types="AD")
    except Exception as e:
        message = {'message': {'message': '异常。'}, 'isSuccess': False}
        log.log(returnid=0, username=username, ip=ip,
                message=username + "重置密码", returnparameters=str(e),
                issuccess=0,
                methodname="usersetchange", types="AD")
        print(e)
    result = message
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#账号查询
def user_query(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('tools/userquery.html', locals())



#权限组拆分
def Permissions_group(username):
    username = (username.strip()).lower()
    domain=get_domain() #数据库获取域名
    vpn_groups=get_PermissionsGrops()['vpn_group']  #获取VPN组
    vpn_groups = eval(vpn_groups.replace("true", "'true'").replace("false", "'false'").replace("null", "'null'"))
    internet_group=get_PermissionsGrops()['internet_group'] #获取上网权限组
    internet_group = eval(internet_group.replace("true", "'true'").replace("false", "'false'").replace("null", "'null'"))
    wifi_groups=get_PermissionsGrops()['wifi_group']  #获取VPN组
    wifi_groups = eval(wifi_groups.replace("true", "'true'").replace("false", "'false'").replace("null", "'null'"))
    # mail_group=get_PermissionsGrops()['mail_group'] #获取邮箱群组
    dfs_group=get_PermissionsGrops()['dfs_group'] #获取dfs群组
    log = logmanager()
    try:
        ObjectExist1=ObjectExist(username, "user", domain)
        if ObjectExist1:
            accountProperty = GetobjectProperty(username, "user", domain)  # 获取用户属性信息
            memberof = accountProperty['message'][0]['memberof'] # 组信息
            intgroup = []
            mailgroup = []
            vpngroup = []
            dfsgroup = []
            wifigroup=[]
            allgroup=[]
            isSuccess = True
            message={'intgroup':intgroup,'mailgroup':mailgroup,'vpngroup':vpngroup,'dfsgroup':dfsgroup,'allgroup':allgroup,'wifigroup':wifigroup}
            if memberof != None:
                if isinstance(memberof,str):
                    memberof=[memberof]
                for i in memberof:
                    member = (i.split(',')[0].split('=')[1]).lower()
                    groupDN=i
                    if internet_group:
                        for group in internet_group:  # 上网
                            if group['name'].lower()== member:
                                intgroup.append(group['description'])
                    if vpn_groups:
                        for group in vpn_groups:  #VPN
                            if group['name'].lower()== member:
                                vpngroup.append(group['description'])#VPN
                    if wifi_groups:
                        for group in wifi_groups:  #无线
                            if group['name'].lower()== member:
                                wifigroup.append(group['description'])
                    if dfs_group:
                        if dfs_group.lower() in groupDN.lower():
                            dfsgroup1 = (groupDN.split(',')[0].split('=')[1])
                            dfsgroup.append(dfsgroup1)
                    propertys = adapi().Initialapi('GetPropertyFordistinguishedName', distinguishedName=i)
                    propertymail = propertys['message'][0]['mail']
                    if propertymail:
                        # propertys = propertys['message'][0]['sAMAccountName']
                        mailgroup.append(propertys['message'][0]['sAMAccountName'])
                        # if mail_group.lower() in i.lower():
                        #     mailgroup1 = (i.split(',')[0].split('=')[1])
                        #     mailgroup.append(mailgroup1)
                for i in memberof:
                    allgroup1= (i.split(',')[0].split('=')[1])
                    allgroup.append(allgroup1)
        else:
            isSuccess = False
            message='账号不存在'
    except Exception as e:
        print(e)
        log.log(returnid=0,message='异常报错'+str(e),
                issuccess=0,
                methodname="Permissions_group", types="AD")
    result = {'isSuccess': isSuccess, 'message': message,}
    return result


#账户信息汇总（账号查询）
def user_profile(request):
    post = request.POST
    username=post.get('username')
    password=post.get('password')
    domain=get_domain() #数据库获取域名
    username=(username.strip()).lower()
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        ObjectExist1=ObjectExist(username, "user", domain)
        if ObjectExist1:
            account = username   #账号信息
            Permissions = Permissions_group(username)
            vpngroup=Permissions['message']['vpngroup'] #vpn 组
            mailgroup=Permissions['message']['mailgroup'] #mialou
            dfsgroup = Permissions['message']['dfsgroup'] #dfs ou
            intgroup = Permissions['message']['intgroup'] #int 组
            intgroup = Permissions['message']['intgroup']  # int 组
            wifigroup = Permissions['message']['wifigroup']  # wifi 组
            allgroup = Permissions['message']['allgroup'] # all  all
            accountProperty=GetobjectProperty(username,"user",domain)  #获取用户属性信息
            mail=accountProperty['message'][0]['mail'] #邮箱
            homeMDB=accountProperty['message'][0]['homeMDB'] #邮箱数据库
            PasswordExpirationDate=accountProperty['message'][0]['PasswordExpirationDate']  #密码到期时间
            IsAccountLocked=accountProperty['message'][0]['IsAccountLocked'] #是否锁定
            pwd=''#密码是否正确
            if IsAccountLocked !='0':
                IsAccountLocked = '已锁定' + " 锁定IP" + IsAccountLocked
                if password != '':
                    pwd = '账户已锁定，无法验证密码'
            else:
                IsAccountLocked='未锁定'
                if password != '':
                    pwd = VerifyUserLogin(username, password, domain)['isSuccess']  # 判断密码是否正确
                    if pwd:
                        pwd = "密码正确"
                    else:
                        pwd = '密码错误'
                else:
                    pwd = '未验证密码'
        else:
            account='账号错误,请核实'
    except Exception as e:
        print(e)
        log.log(returnid=0, ip=ip, message='异常报错'+str(e),
                issuccess=0,
                methodname="user_profile", types="AD")
    return render_to_response('tools/userquery.html', locals())


#返回所有组信息不带DN
def all_gropu(username,domain):
    log = logmanager()
    try:
        ObjectExist1=ObjectExist(username, "user", domain)
        if ObjectExist1:
            memberof = GetobjectProperty(username, "user", domain)['message'][0]['memberof']  # 获取用户属性信息
            allgroup=[]
            if memberof != None:
                if isinstance(memberof,str):
                    allgroup.append(memberof.split(',')[0].split('=')[1])
                    result = {'message': {'allgroup': allgroup}, 'isSuccess': True}
                    return result
                else:
                    for i in memberof:
                        allgroup1= (i.split(',')[0].split('=')[1])
                        allgroup.append(allgroup1)
                    result = {'message': {'allgroup': allgroup}, 'isSuccess': True}
                return result
            else:
                result = {'message': {'allgroup': '无群组'}, 'isSuccess': False}
            return result
        else:
            result = {'message': {'allgroup': '账号不存在'}, 'isSuccess': False}
        return result
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="all_gropu", types="AD")
        result = {'message': {'allgroup': '未知错误'}, 'isSuccess': False}
        return result


#返回所有组信息带DN
def all_gropuDN(username,domain):
    log = logmanager()
    try:
        ObjectExist1=ObjectExist(username, "user", domain)
        if ObjectExist1:
            memberof = GetobjectProperty(username, "user", domain)['message'][0]['memberof']  # 获取用户属性信息
            allgroup=[]
            if memberof != None:
                isSuccess = True
                if isinstance(memberof,str):
                    allgroup=[memberof]
                else:
                    allgroup=memberof
            else:
                isSuccess = False
                allgroup='无群组'
        else:
            isSuccess = False
            allgroup='账号不存在'
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="all_gropuDN", types="AD")
    result = {'isSuccess': isSuccess, 'message': {'allgroup': allgroup}}
    return result



#判断用户是否在某个组中不带DN，精确匹配组
def if_user_in_group(username,group,domain):
    log = logmanager()
    try:
        ObjectExist1 = ObjectExist(username, "user", domain)
        if ObjectExist1:
            allgropu = all_gropu(username, domain)
            if allgropu['isSuccess']:
                groups=allgropu['message']['allgroup']
                for i in groups:
                    if group.lower() == i.lower():
                        return True
        return False
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="if_user_in_group", types="AD")



# 判断用户是否在某个组中带DN，可匹配OU
def if_user_in_groupDN(username, group, domain):
    log = logmanager
    try:
        ObjectExist1 = ObjectExist(username, "user", domain)
        if ObjectExist1:
            allgropu = all_gropuDN(username, domain)
            if allgropu['isSuccess']:
                groups = allgropu['message']['allgroup']
                for i in groups:
                    if group.lower() in i.lower():
                        return True
        return False
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="if_user_in_groupDN", types="AD")

#解锁页面
def user_unlock(request):
    username = request.session.get('username')
    displyname=request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username=username.lower()
            domain = get_domain()
            it_authority_group=dbinfo_select_global_configuration()[0]['it_group']
            authority=if_user_in_group(username, it_authority_group, domain)
            if authority:
                return render_to_response('tools/userunlock.html',locals())
            else:
                log.log(returnid=0, username=username, ip=ip, message=username + '没有权限', issuccess=0,
                        methodname="user_unlock",types="AD")
                return render_to_response('portal.html', locals())
        else:
            return HttpResponseRedirect("portal.html")
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="user_unlock", types="AD")
        return False
#解锁
def unlock(request):
    username=request.session.get('username')
    post = request.POST
    account = post.get('account','')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        domain = get_domain()
        if username:
            username=username.lower()
            domain = get_domain()
            it_authority_group=dbinfo_select_global_configuration()[0]['it_group']
            authority=if_user_in_group(username, it_authority_group, domain)
            if authority:
                result=UnlockAccount(account,domain)
                log.log(returnid=1, username=username, ip=ip, message=username+'对'+account + '进行解锁', issuccess=1,
                        methodname="unlock", returnparameters=str(result), types="AD")
            else:
                result = {'message': {'message': '你没有权限'}, 'isSuccess': False}
                log.log(returnid=0, username=username, ip=ip, message=username + '没有权限对' + account + '解锁', issuccess=0,
                        methodname="unlock", returnparameters=str(result), types="AD")
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect("portal.html")
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="unlock", types="AD")
        return HttpResponseRedirect("portal.html")

#添加防锁定页面
def addPwdNoLock(request):
    username = request.session.get('username')
    displyname = request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username=username.lower()
            domain = get_domain()
            it_authority_group=dbinfo_select_global_configuration()[0]['it_group']
            authority=if_user_in_group(username, it_authority_group, domain)
            if authority:
                return render_to_response('tools/addpwdnolock.html',locals())
            else:
                return render_to_response('portal.html', locals())
        else:
            return HttpResponseRedirect("portal.html")
    except Exception as e:
            print(e)
            log.log(returnid=0, message='异常报错'+str(e),
                    issuccess=0,
                    methodname="addPwdNoLock", types="AD")
            return False

#添加防锁定
def addPwdNoLockGroup(request):
    username=request.session.get('username')
    post = request.POST
    account = post.get('account','')
    time=post.get('radios','')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        domain = get_domain()
        if username:
            username=username.lower()
            domain = get_domain()
            it_authority_group=dbinfo_select_global_configuration()[0]['it_group']
            authority=if_user_in_group(username, it_authority_group, domain)
            if authority:
                NoLockGroup = get_PermissionsGrops()['NoLockGroup']
                account_in_NoLockGroup=if_user_in_group(account, NoLockGroup, domain)
                if time !='':
                    if account_in_NoLockGroup == False:
                        AddUserToGroups = AddUserToGroup(account, NoLockGroup, domain)
                        if AddUserToGroups:
                            result={'isSuccess': True, 'message':account+"添加防锁定成功,"+time+"分后失效"}
                            # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
                            delpwdnolock(username, account, NoLockGroup, time,domain)
                            log.log(returnid=1, username=username, ip=ip, message=username + '对' + account + '成功添加'+ time+'分钟防锁定',
                                    issuccess=1,
                                    methodname="addPwdNoLockGroup", returnparameters=str(result), types="AD")
                        else:
                            result=AddUserToGroups
                            log.log(returnid=0, username=username, ip=ip,
                                    message=username + '对' + account + '添加防锁定失败',
                                    issuccess=0,
                                    methodname="addPwdNoLockGroup", returnparameters=str(result), types="AD")
                    else:
                        result={'isSuccess': False, 'message': '此用户已添加防锁定，请勿重复添加'}
                        log.log(returnid=0, username=username, ip=ip,
                                message=username + '对' + account + '添加防锁定失败,因用户已添加防锁定，请勿重复添加',
                                issuccess=0,
                                methodname="addPwdNoLockGroup", returnparameters=str(result), types="AD")
                else:
                    result = {'isSuccess': False, 'message': '请选择添加防锁定的时间'}
            else:
                log.log(returnid=0, username=username, ip=ip,
                        message=username + '对' + account + '添加防锁定失败,因用户没有添锁定权限',
                        issuccess=0,
                        methodname="addPwdNoLockGroup", types="AD")
                result = {'isSuccess': False, 'message': '你没有权限'}

            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect("portal.html")
    except Exception as e:
        print (e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="addPwdNoLockGroup", types="AD")
        return HttpResponseRedirect("portal.html")

#admin重置密码页面
def ad_resetpwd(request):
    username = request.session.get('username')
    displyname=request.session.get('displayname')
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    try:
        if username:
            username=username.lower()
            domain = get_domain()
            it_authority_group=dbinfo_select_global_configuration()[0]['it_group']
            authority=if_user_in_group(username, it_authority_group, domain)
            if authority:
                return render_to_response('tools/adresetpwd.html',locals())
            else:
                log.log(returnid=0, username=username, ip=ip, message=username + '没有权限', issuccess=0,
                        methodname="ad_resetpwd",types="AD")
                return render_to_response('portal.html', locals())
        else:
            return HttpResponseRedirect("portal.html")
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="ad_resetpwd", types="AD")
        return False

#重置密码
def user_resetpwd(request):
    username=request.session.get('username')
    post = request.POST
    account = post.get('account','')
    account=(account.strip()).lower()
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    passwd = genpwd()
    try:
        domain = get_domain()
        if username:
            username=username.lower()
            domain = get_domain()
            it_authority_group=dbinfo_select_global_configuration()[0]['it_group']
            authority=if_user_in_group(username, it_authority_group, domain)
            if authority:
                if account !='administrator':
                    result = adapi().Initialapi('ResetPasswordByOU', username=account, newpassword=passwd)
                    result1=result['message']['message']
                    log.log(returnid=1, username=username, ip=ip, message=username+'对'+account + '进行密码重置', issuccess=1,
                            methodname="user_resetpwd", returnparameters=str(result1), types="AD")
                else:
                    result = {'message': {'message': '不允许重置administrator密码'}, 'isSuccess': False}
                    log.log(returnid=0, username=username, ip=ip, message=username + '没有权限对' + account + '进行行密码重置',
                            issuccess=0,
                            methodname="user_resetpwd", returnparameters=str(result), types="AD")
            else:
                result = {'message': {'message': '你没有权限'}, 'isSuccess': False}
                log.log(returnid=0, username=username, ip=ip, message=username + '没有权限对' + account + '进行密码重置', issuccess=0,
                        methodname="user_resetpwd", returnparameters=str(result), types="AD")
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect("portal.html")
    except Exception as e:
        print(e)
        log.log(returnid=0, message='异常报错'+str(e),
                issuccess=0,
                methodname="user_resetpwd", types="AD")
        return HttpResponseRedirect("portal.html")

