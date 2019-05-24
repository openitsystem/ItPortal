import ast
import json

from adapi.ad_api import getmanger
from adapi.dbinfo import updatepumailuser, insert_pubmailflow_process
from django.http import HttpResponse
from django.shortcuts import render, render_to_response


# Create your views here.
from Thr.Creatpubmail import UserCreatMail, adapi
from adapi.dbinfo import insert_pubmailflow, getdb_mail,getmailou_new
from adapi.pwd import genpwd
from dfs.dbinfo import get_management_configuration, get_api
from admin_account.dbinfo import dbinfo_select_global_configuration
from dfs.thr_process import process_outgoing
from logmanager.views import logmanager
from sendmail.sendmail import send_email_by_template


def applypublicmail(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('mail/applypublicmail.html', locals())

def applymailpermission(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('mail/applymailpermission.html', locals())



def applymailgroup(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('mail/applymailgroup.html', locals())

def findmail(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    return render_to_response('mail/findmail.html', locals())

def unlockmail(request):
    log = logmanager()
    username = request.session.get('username')
    mailaddress = request.session.get('mail')
    displayname = request.session.get('displayname')
    try:
        message=adapi().Initialapi('GetActiveSyncDevice', mailname=username, parametername='DeviceId')
        if message['isSuccess']:
            statu = True
            messageshow = message['message']
        else:
            statu = False
    except Exception as e:
        log.log(returnid=0, username=username,  message='获取用户手机邮箱信息异常', issuccess=0, methodname="unlockmail",
                types="exchange")
        statu = False
    return render_to_response('mail/unlockmail.html', locals())

#验证账号是否重复
def accountexist(request):
    post = request.POST
    mailadd = post.get('mailadd')
    try:
        messa=adapi().Initialapi('ObjectExistAD',objectName=mailadd)
        dbmail=getdb_mail(mailadd)
        if messa or dbmail!=():
            reslu=False
        else:
            reslu=True
    except Exception as e:
        reslu = True
        print(e)
    result = {'status': reslu}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def findmailgroup(request):
    post = request.POST
    mailgroupnamevalue = post.get('mailgroupnamevalue')
    try:
        groupmanagergroup = adapi().Initialapi('GetDistributionGroupSendto', pyname=mailgroupnamevalue,pyvalue="AcceptMessagesOnlyFromSendersOrMembers")
        if groupmanagergroup['isSuccess']:
            reslut = True
            if groupmanagergroup['message'] == []:
                message = False
            else:
                message = True
        else:
            reslut = False
            message = False
    except Exception as e:
        reslut = False
        message = False
    status = {'status': reslut,"message":message}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(status))
    return response

def findmailgroupmanager(request):
    post = request.POST
    mailgroupnamevalue = post.get('mailgroupnamevalue')
    try:
        groupmanagergroup = adapi().Initialapi('Showgroupname', groupname=mailgroupnamevalue)
        if groupmanagergroup['isSuccess']:
            if groupmanagergroup['message']['mail'] != None:
                reslut = True
                if groupmanagergroup['message']['managedBy'] == None:
                    message = [{"managervalue": "暂无管理者", "type": "邮箱群组", "mail": groupmanagergroup['message']['mail'],
                                "name": groupmanagergroup['message']['displayname'],
                                'todo': "<button type='button' onclick='tobemanager(\""+ groupmanagergroup['message']['sAMAccountName'] + "\")' class='btn btn-danger btn-border'>申请成为管理者</button>"}]
                else:
                    managervalue = adapi().Initialapi('GetPropertyFordistinguishedName', distinguishedName=groupmanagergroup['message']['managedBy'])
                    if managervalue['isSuccess']:
                        message = [{"managervalue":managervalue['message'][0]['sAMAccountName'],"type":"邮箱群组","mail":groupmanagergroup['message']['mail'],"name":groupmanagergroup['message']['displayname'],'todo':'联系管理者：'+(managervalue['message'][0]['displayName']).replace(">","&gt;").replace("<","&lt;")}]
                    else:
                        message = [
                            {"managervalue": "暂无管理者", "type": "邮箱群组", "mail": groupmanagergroup['message']['mail'],
                             "name": groupmanagergroup['message']['displayname'],
                             'todo': "<button type='button' onclick='tobemanager(\"" + groupmanagergroup['message'][
                                 'sAMAccountName'] + "\")' class='btn btn-danger btn-border'>申请成为管理者</button>"}]
            else:
                reslut = False
                message = []
        else:
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
                                  ldaps='(&(objectCategory=person)(objectClass=user)(mail=*) (sAMAccountName=' + mailgroupnamevalue + '))',
                                  path=ad_path)
            if publicmailvalue['isSuccess'] and publicmailvalue['Count'] != 0:
                reslut = True
                publicmailvaluemessage = publicmailvalue['message'][0]
                managervalue = publicmailvaluemessage.get(pubmailfencelastvalue.lower(), [None])[0]
                if managervalue == None:
                    message = [
                        {"managervalue": "暂无管理者", "type": "公共邮箱", "mail": publicmailvaluemessage.get("mail", ["无"])[0],
                         "name": publicmailvaluemessage.get("displayname", ["无"])[0],
                         'todo': "<button type='button' onclick='tobepublicmailmanager(\"" + publicmailvaluemessage.get("samaccountname", [mailgroupnamevalue])[0] + "\")' class='btn btn-danger btn-border'>申请成为管理者</button>"}]
                else:
                    managervaluemessage = adapi().Initialapi("GetobjectProperty",objects=managervalue,objectClass="user")
                    if managervaluemessage['isSuccess']:
                        message = [{"managervalue":managervaluemessage['message'][0]['sAMAccountName'],"type":"公共邮箱","mail":publicmailvaluemessage.get("mail", ["无"])[0],"name":publicmailvaluemessage.get("displayname", ["无"])[0],'todo':'联系管理者：'+(managervaluemessage['message'][0]['displayName']).replace(">","&gt;").replace("<","&lt;")}]
                    else:
                        message = [
                            {"managervalue": "暂无管理者", "type": "公共邮箱",
                             "mail": publicmailvaluemessage.get("mail", ["无"])[0],
                             "name": publicmailvaluemessage.get("displayname", ["无"])[0],
                             'todo': "<button type='button' onclick='tobepublicmailmanager(\"" +
                                     publicmailvaluemessage.get("samaccountname", [mailgroupnamevalue])[
                                         0] + "\")' class='btn btn-danger btn-border'>申请成为管理者</button>"}]
            else:
                reslut = False
                message = []
    except Exception as e:
        reslut = False
        message = ""
    status = {'status': reslut,"message":message}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(status))
    return response

def tobemanager(request):
    post = request.POST
    groupname = post.get('groupname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    try:
        applytype='成为邮箱群组管理者'
        types='EX'
        # manger=oajobumber('1012528')

        newgroupmessagevalue = {"groupname": groupname, "username": username}
        aa = str(newgroupmessagevalue)
        process = get_api("process")
        if process:
            insert_pubmailflow_processs = insert_pubmailflow_process(ip, username, displayname, types, applytype, groupname, director='系统', message=str(aa))
            if insert_pubmailflow_processs:
                process_outgoings = process_outgoing({"status": 0, "message": {"id":insert_pubmailflow_processs['id'], "username": username, "displayname": displayname, "types": types,"applytype": applytype, "applydetail": groupname}})
                if process_outgoings['status'] == 0:
                    status = True
                else:
                    status = False
            else:
                status = False
        else:
            manger = getmanger(username,"mailgroumanger")
            if manger != False:
                flowmail=insert_pubmailflow(ip,username,displayname,types,applytype,groupname,manger,aa)
                if flowmail==():
                    status= True
                    log.log(returnid=1,username=username,ip=ip,message=applytype+aa,issuccess=1,methodname="tobemanager",types="exchange")
                    mangervalue = adapi().Initialapi("GetobjectProperty",objects=manger,objectClass="user")
                    if mangervalue['isSuccess']:
                        subject = u'您有一个新申请单待审批'
                        emaillists = username + displayname +'申请成为邮箱群组'+ groupname +'的管理者，您可以登录平台对审批单进行审批！'
                        email_data = {'emaillists': emaillists}
                        template = "mailmould/sendmailpassword.html"
                        to_list = [mangervalue['message'][0]['mail']]
                        send_email_by_template(subject, template, email_data, to_list)
                else:
                    status =False
                    log.log(returnid=0,username=username,ip=ip,message=applytype+aa,issuccess=0,methodname="tobemanager",types="exchange")
            else:
                status = False
                log.log(returnid=0, message=username + "申请成为邮箱群组管理者出现异常", issuccess=0, inparameters="查询不到" + username + "主管",
                        methodname="tobemanager", types="exchange")
    except Exception as e:
        status = False
        log.log(returnid=0, message=username + "申请成为邮箱群组管理者", issuccess=0, inparameters=str(e),
                methodname="tobemanager", types="exchange")
    status = {'status': status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(status))
    return response


def tobepublicmailmanager(request):
    post = request.POST
    groupname = post.get('groupname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    log = logmanager()
    try:
        applytype='成为公共邮箱管理者'
        types='EX'
        newgroupmessagevalue = {"publicmail":groupname,"username":username}
        aa = str(newgroupmessagevalue)
        process = get_api("process")
        if process:
            insert_pubmailflow_processs = insert_pubmailflow_process(ip, username, displayname, types, applytype, groupname, director='系统', message=str(aa))
            if insert_pubmailflow_processs:
                process_outgoings = process_outgoing({"status": 0, "message": {"id":insert_pubmailflow_processs['id'], "username": username, "displayname": displayname, "types": types,"applytype": applytype, "applydetail": groupname}})
                if process_outgoings['status'] == 0:
                    status = True
                else:
                    status = False
            else:
                status = False
        else:
            mange=getmanger(username,"pubmailmanger")
            if mange != False:
                flowmail=insert_pubmailflow(ip,username,displayname,types,applytype,groupname,mange,aa)
                if flowmail==():
                    status= True
                    log.log(returnid=1,username=username,ip=ip,message=applytype+aa,issuccess=1,methodname="tobepublicmailmanager",types="exchange")
                    mangervalue = adapi().Initialapi("GetobjectProperty", objects=mange, objectClass="user")
                    if mangervalue['isSuccess']:
                        subject = u'您有一个新申请单待审批'
                        emaillists = username + displayname +'申请成为公共邮箱' + groupname + '的管理者，您可以登录平台对审批单进行审批！'
                        email_data = {'emaillists': emaillists}
                        template = "mailmould/sendmailpassword.html"
                        to_list = [mangervalue['message'][0]['mail']]
                        send_email_by_template(subject, template, email_data, to_list)
                else:
                    status =False
                    log.log(returnid=0,username=username,ip=ip,message=applytype+aa,issuccess=0,methodname="tobepublicmailmanager",types="exchange")
            else:
                status = False
                log.log(returnid=0, message=username + "申请成为公共邮箱管理者出现异常", issuccess=0,
                        inparameters="查询不到" + username + "主管",
                        methodname="tobepublicmailmanager", types="exchange")
    except Exception as e:
        status = False
        log.log(returnid=0, message=username + "申请成为公共邮箱管理者出现异常", issuccess=0,
                inparameters=str(e),
                methodname="tobepublicmailmanager", types="exchange")
    status = {'status': status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(status))
    return response

def submitApplication(request):
    post = request.POST
    sendtovalue = post.get('sendtovalue')
    groupname = post.get('groupname')
    creceivevalue = post.get('creceivevalue')
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    log = logmanager()
    try:
        dictvalue = {"sendtovalue":sendtovalue,"creceivevalue":creceivevalue,"groupname":groupname,"user":username}
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        types = "EX"
        applytype = "邮箱群组权限申请"
        pumail = groupname
        process = get_api("process")
        if process:
            insert_pubmailflow_processs = insert_pubmailflow_process(ip, username, displayname, types, applytype, pumail, director='系统', message=str(dictvalue))
            if insert_pubmailflow_processs:
                process_outgoings = process_outgoing({"status": 0, "message": {"id":insert_pubmailflow_processs['id'], "username": username, "displayname": displayname, "types": types,"applytype": applytype, "applydetail": pumail}})
                if process_outgoings['status'] == 0:
                    status = True
                else:
                    status = False
            else:
                status = False
        else:
            mange = getmanger(username,"mailgroumanger")
            if mange != False:
                flowmail = insert_pubmailflow(ip, username, displayname, types, applytype, pumail,mange, str(dictvalue))
                if flowmail == ():
                    status = True
                    log.log(returnid=1,username=username,ip=ip,message=username+"申请"+groupname+"群组权限"+str(dictvalue),issuccess=1,methodname="submitApplication",types="exchange")
                    mangervalue = adapi().Initialapi("GetobjectProperty", objects=mange, objectClass="user")
                    if mangervalue['isSuccess']:
                        if creceivevalue == 'true':
                            creceivevalue_message = "收件人权限，"
                        else:
                            creceivevalue_message = ""
                        if sendtovalue == 'true':
                            sendtovalue_message = "发件人权限，"
                        else:
                            sendtovalue_message = ""
                        subject = u'您有一个新申请单待审批'
                        emaillists = username + displayname +'申请邮箱群组' + groupname +creceivevalue_message +sendtovalue_message+'您可以登录平台对审批单进行审批！'
                        email_data = {'emaillists': emaillists}
                        template = "mailmould/sendmailpassword.html"
                        to_list = [mangervalue['message'][0]['mail']]
                        send_email_by_template(subject, template, email_data, to_list)
                else:
                    status = False
                    log.log(returnid=0,username=username,ip=ip,message=username+"申请"+groupname+"群组权限"+str(dictvalue),issuccess=0,methodname="submitApplication",types="exchange")
            else:
                status = False
                log.log(returnid=0, username=username, ip=ip, message=username + "申请" + groupname + "群组权限" + str(dictvalue),returnparameters="找不到"+username+"主管",
                        issuccess=0, methodname="submitApplication", types="exchange")
    except Exception as e:
        status = False
        log.log(returnid=0,username=username,ip=ip,message=username+"申请"+groupname+"群组权限"+str(e),issuccess=0,methodname="submitApplication",types="exchange")
    status = {'status': status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(status))
    return response

#验证AD
def acountad(request):
    post = request.POST
    user = post.get('user')
    try:
        messa = adapi().Initialapi('ObjectExistAD', objectName=user)
    except Exception as e:
        messa = False
        print(e)
    result = {'status': messa}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#手机邮箱解锁
def lockactive(request):
    log = logmanager()
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    post = request.POST
    mailid = post.get('mailid')
    messa=adapi().Initialapi('SetCASMailbox', mailname=username, id=mailid)
    try:
        if messa:
            status = {'isSuccess': True, 'message': '恭喜，您的移动设备解除阻止成功。:)'}
            log.log(returnid=1, ip=ip,message=username + "解锁手机邮箱，手机邮箱id为"+mailid ,
                    issuccess=1, inparameters=str(messa), methodname="lockactive", types="exchange")
        else:
            status = {'isSuccess': False, 'message': '抱歉,您的移动设备解除阻止失败，请重试。如多次解锁失败，请联系“IT”。'}
            log.log(returnid=0, ip=ip, message=username + "解锁手机邮箱，手机邮箱id为" + mailid,
                    issuccess=0, inparameters=str(messa), methodname="lockactive", types="exchange")
    except Exception as e:
        status = {'isSuccess': False, 'message': '出现异常'}
        log.log(returnid=0, ip=ip, message=username + "解锁手机邮箱，手机邮箱id为" + mailid,
                issuccess=0, inparameters=str(messa), methodname="lockactive", types="exchange")
        print(e)
    result = status
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def new_mailgroup(id,director,message):
    messagevalue = ast.literal_eval(message)
    getgroupdefuatouvalue = getmailou_new()[0]['mailgroupdefaultOU']
    if getgroupdefuatouvalue == None:
        OrganizationalUnit = "None"
    else:
        OrganizationalUnit = getgroupdefuatouvalue
    log = logmanager()
    creatgroupvalue = adapi().Initialapi("newDistributionGroup",Alias=messagevalue['mail'],DisplayName=messagevalue['displaynamevalue'],ManagedBy=messagevalue['usadaccount'],OrganizationalUnit = OrganizationalUnit)
    if messagevalue['hasout'] == None:
        hasout = False
    else:
        hasout = True
    changegroupdisplaynamevalue = adapi().Initialapi("SetDistributionGroupbybool", Identity=messagevalue['mail'],
                                                     pyname="RequireSenderAuthenticationEnabled",
                                                     pyvalue=hasout)
    if creatgroupvalue['isSuccess']:
        updatepumailuser(id, 1)
        log.log(returnid=1,message="新建群组"+str(creatgroupvalue),issuccess=1,inparameters=message,methodname="new_mailgroup",types="exchange")
        log.log(returnid=1,message="新建群组设置身份认证"+str(changegroupdisplaynamevalue),issuccess=1,inparameters=message,methodname="new_mailgroup",types="exchange")
    else:
        updatepumailuser(id, 2)
        log.log(returnid=0,message="新建群组"+str(creatgroupvalue),issuccess=0,inparameters=message,methodname="new_mailgroup",types="exchange")
        log.log(returnid=1,message="新建群组设置身份认证"+str(changegroupdisplaynamevalue),issuccess=1,inparameters=message,methodname="new_mailgroup",types="exchange")
    return 1

def allowtobemanager(id,director,message):
    log = logmanager()
    messagevalue = ast.literal_eval(message)
    groupname = messagevalue['groupname']
    groupmessagevalue = adapi().Initialapi("Showgroupname",groupname=groupname)
    managermessagevalue = adapi().Initialapi("GetobjectProperty",objects=messagevalue['username'],objectClass="user")
    if managermessagevalue['isSuccess']:
        managerDN = managermessagevalue['message'][0]['distinguishedName']
        if groupmessagevalue['isSuccess']:
            if groupmessagevalue['message']['managedBy'] == None:
                addmanagerment = adapi().Initialapi("SetobjectProperty",objects=groupname,objectClass="group",PropertyName="managedBy",PropertyValue=managerDN)
                if addmanagerment['isSuccess']:
                    log.log(returnid=1, message="成为群组管理者" + str(groupname), issuccess=1, inparameters=message,returnparameters=addmanagerment,
                            methodname="allowtobemanager", types="exchange")
                    updatepumailuser(id, 1)
                else:
                    log.log(returnid=0, message="成为群组管理者" + str(groupname), issuccess=0, inparameters=message,returnparameters=addmanagerment,
                            methodname="allowtobemanager", types="exchange")
                    updatepumailuser(id, 2)
            else:
                oldmanagervalue = adapi().Initialapi("GetPropertyFordistinguishedName",distinguishedName=groupmessagevalue['message']['managedBy'])
                if oldmanagervalue['isSuccess']:
                    log.log(returnid=0, message="成为群组管理者" + str(groupname)+"失败，原管理者是："+str(oldmanagervalue['message']), issuccess=0, inparameters=message,
                            methodname="allowtobemanager", types="exchange")
                    updatepumailuser(id, 2)
                else:
                    addmanagerment = adapi().Initialapi("SetobjectProperty",objects=groupname,objectClass="group",PropertyName="managedBy",PropertyValue=managerDN)
                    if addmanagerment['isSuccess']:
                        log.log(returnid=1, message="成为群组管理者" + str(groupname), issuccess=1, inparameters=message,returnparameters=addmanagerment,
                                methodname="allowtobemanager", types="exchange")
                        updatepumailuser(id, 1)
                    else:
                        log.log(returnid=0, message="成为群组管理者" + str(groupname), issuccess=0, inparameters=message,returnparameters=addmanagerment,
                                methodname="allowtobemanager", types="exchange")
                        updatepumailuser(id, 2)
        else:
            log.log(returnid=0, message="成为群组管理者" + str(groupname), issuccess=0, inparameters=message,returnparameters=str(groupmessagevalue),
                    methodname="allowtobemanager", types="exchange")
            updatepumailuser(id, 2)
    else:
        log.log(returnid=0, message="成为群组管理者" + str(groupname), issuccess=0, inparameters=message,returnparameters=str(managermessagevalue),
                methodname="allowtobemanager", types="exchange")
        updatepumailuser(id, 2)
    return 1

def allowtobepublicmailmanager(id,director,message):
    log = logmanager()
    messagevalue = ast.literal_eval(message)
    groupname = messagevalue['publicmail']
    groupmessagevalue = adapi().Initialapi("GetobjectProperty",objects=groupname,objectClass="user")
    managermessagevalue = adapi().Initialapi("GetobjectProperty",objects=messagevalue['username'],objectClass="user")
    if managermessagevalue['isSuccess']:
        managerDN = managermessagevalue['message'][0]['distinguishedName']
        if groupmessagevalue['isSuccess']:
            configsql = getmailou_new()
            pubmailfence = configsql[0]['pubmailfence']
            if pubmailfence != "" and pubmailfence != None:
                pubmailfencelastvalue = pubmailfence
            else:
                pubmailfencelastvalue = "physicalDeliveryOfficeName"
            publicmailmanagervalue = adapi().Initialapi("Getuseraccountfornovalue",objects=groupname,returnvalue=pubmailfencelastvalue)
            if publicmailmanagervalue['message'] == None:
                setpublicmailvalue = adapi().Initialapi("SetuserProperty",username=groupname,PropertyName=pubmailfencelastvalue,PropertyValue=messagevalue['username'])
                if setpublicmailvalue['isSuccess']:
                    updatepumailuser(id, 1)
                    log.log(returnid=1, message="审批"+messagevalue['username']+"成为公共邮箱"+ groupname+"管理者", issuccess=1,
                            inparameters=message, methodname="allowtobepublicmailmanager", returnparameters=str(setpublicmailvalue),types="exchange")
                else:
                    updatepumailuser(id, 2)
                    log.log(returnid=0, message="审批"+messagevalue['username']+"成为公共邮箱"+ groupname+"管理者", issuccess=0,
                            inparameters=message, methodname="allowtobepublicmailmanager", returnparameters=str(setpublicmailvalue),types="exchange")
            else:
                publicmailoldmanager = adapi().Initialapi("GetobjectProperty",objects=publicmailmanagervalue['message'],objectClass="user")
                if publicmailoldmanager['isSuccess']:
                    updatepumailuser(id, 2)
                    log.log(returnid=0, message="审批"+messagevalue['username']+"成为公共邮箱"+ groupname+"管理者", issuccess=0,
                            inparameters=message, methodname="allowtobepublicmailmanager", returnparameters="老管理者"+str(publicmailoldmanager),types="exchange")
                else:
                    setpublicmailvalue = adapi().Initialapi("SetuserProperty", username=groupname,
                                                            PropertyName=pubmailfencelastvalue,
                                                            PropertyValue=messagevalue['username'])
                    if setpublicmailvalue['isSuccess']:
                        updatepumailuser(id, 1)
                        log.log(returnid=1, message="审批"+messagevalue['username']+"成为公共邮箱"+ groupname+"管理者", issuccess=1,
                                inparameters=message, methodname="allowtobepublicmailmanager", returnparameters=str(setpublicmailvalue),types="exchange")
                    else:
                        updatepumailuser(id, 2)
                        log.log(returnid=0, message="审批"+messagevalue['username']+"成为公共邮箱"+ groupname+"管理者", issuccess=0,
                                inparameters=message, methodname="allowtobepublicmailmanager", returnparameters=str(setpublicmailvalue),types="exchange")
        else:
            log.log(returnid=0, message="成为群组管理者" + str(groupname), issuccess=0, inparameters=message,returnparameters=str(groupmessagevalue),
                    methodname="allowtobemanager", types="exchange")
            updatepumailuser(id, 2)
    else:
        log.log(returnid=0, message="审批"+messagevalue['username']+"成为公共邮箱"+ groupname+"管理者", issuccess=0, inparameters=message,returnparameters=str(managermessagevalue),
                methodname="allowtobepublicmailmanager", types="exchange")
        updatepumailuser(id, 2)
    return 1


def mailgrouppermession(id,director,message):
    messagevalue = ast.literal_eval(message)
    sendtovalue = messagevalue['sendtovalue']
    groupname = messagevalue['groupname']
    creceivevalue = messagevalue['creceivevalue']
    username = messagevalue['user']
    log = logmanager()
    if creceivevalue  == "true" and  sendtovalue == "false":
        addusertogroupvalue = adapi().Initialapi("AddUserToGroup",sAMAccountName=username,groupname=groupname)
        if addusertogroupvalue['isSuccess']:
            updatepumailuser(id, 1)
            log.log(returnid=1,message=username+"添加到"+groupname+"组中",issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
        else:
            if "对象已存在" in addusertogroupvalue['message']:
                updatepumailuser(id, 1)
                log.log(returnid=2,message=username+"添加到"+groupname+"组中"+addusertogroupvalue['message'],issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
            else:
                updatepumailuser(id, 2)
                log.log(returnid=0,message=username+"添加到"+groupname+"组中"+addusertogroupvalue['message'],issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
    if creceivevalue  == "false" and  sendtovalue == "true":
        hassendto = adapi().Initialapi('GetDistributionGroup', pyname=groupname,pyvalue="AcceptMessagesOnlyFromSendersOrMembers")
        if hassendto['isSuccess']:
            if hassendto['message'] == ["{'daname':''}"]:
                updatepumailuser(id, 1)
                log.log(returnid=2,message=username+"添加到"+groupname+"发件权限中，"+groupname+"没做权限限制，不作操作",issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
            else:
                addusertosendtogroup = adapi().Initialapi("SetDistributionGroupaddremove",mailname=groupname,projectname1="AcceptMessagesOnlyFrom",todo="add",id=username)
                if addusertosendtogroup['isSuccess']:
                    updatepumailuser(id, 1)
                    log.log(returnid=1,message=username+"添加到"+groupname+"发件权限中"+str(addusertosendtogroup),issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
                else:
                    updatepumailuser(id, 2)
                    log.log(returnid=0,message=username+"添加到"+groupname+"发件权限中"+str(addusertosendtogroup),issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
        else:
            updatepumailuser(id, 2)
            log.log(returnid=0,message=username+"添加到"+groupname+"发件权限中"+str(hassendto),issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
    else:
        addusertogroupvalue = adapi().Initialapi("AddUserToGroup",sAMAccountName=username,groupname=groupname)
        if addusertogroupvalue['isSuccess']:
            receiveadd = 1
            log.log(returnid=1,message=username+"添加到"+groupname+"组中",issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
        else:
            if "对象已存在" in addusertogroupvalue['message']:
                receiveadd = 1
                log.log(returnid=2,message=username+"添加到"+groupname+"组中"+addusertogroupvalue['message'],issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
            else:
                receiveadd = 2
                log.log(returnid=0,message=username+"添加到"+groupname+"组中"+addusertogroupvalue['message'],issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
        hassendto = adapi().Initialapi('GetDistributionGroup', pyname=groupname,pyvalue="AcceptMessagesOnlyFromSendersOrMembers")
        if hassendto['isSuccess']:
            if hassendto['message'] == ["{'daname':''}"]:
                sendtoadd = 1
                log.log(returnid=2,message=username+"添加到"+groupname+"发件权限中，"+groupname+"没做权限限制，不作操作",issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
            else:
                addusertosendtogroup = adapi().Initialapi("SetDistributionGroupaddremove",mailname=groupname,projectname1="AcceptMessagesOnlyFrom",todo="add",id=username)
                if addusertosendtogroup['isSuccess']:
                    sendtoadd = 1
                    log.log(returnid=1,message=username+"添加到"+groupname+"发件权限中"+str(addusertosendtogroup),issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
                else:
                    sendtoadd = 2
                    log.log(returnid=0,message=username+"添加到"+groupname+"发件权限中"+str(addusertosendtogroup),issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
        else:
            sendtoadd = 2
            log.log(returnid=0,message=username+"添加到"+groupname+"发件权限中"+str(hassendto),issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
        if receiveadd == 1 and sendtoadd == 1:
            updatepumailuser(id, 1)
            log.log(returnid=1,message=username+"添加到"+groupname+"收、发件权限成功",issuccess=1,inparameters=message,methodname="mailgrouppermession",types="exchange")
        else:
            updatepumailuser(id, 2)
            log.log(returnid=0,message=username+"添加到"+groupname+"收、发件权限失败",issuccess=0,inparameters=message,methodname="mailgrouppermession",types="exchange")
    return 1


def new_pubmail(id,applydetail,message):
    log = logmanager()
    evavalue=ast.literal_eval(message)
    pubmes = get_management_configuration()
    try:
        oufirst = pubmes['pubmailou']
        if oufirst:
            ou=oufirst
        else:
            ou = dbinfo_select_global_configuration()[0]['ad_path']
        mailbox = pubmes["pubmailDB"]
        mailpen = pubmes["pubmailfence"]
        passwd = genpwd()
        UserCreatMail(id, applydetail, ou, evavalue['usadaccount'], evavalue['displaynamevalue'], passwd, mailbox,mailpen)
        mangervalue = adapi().Initialapi("GetobjectProperty", objects=evavalue['usadaccount'], objectClass="user")
        subject = u'公共邮箱开通成功'
        emaillists = '您申请的公共邮箱，已审批同意。公共邮箱账号：'+applydetail+'，密码为'+passwd+'（请妥善保管密码，并且将密码同步给所有需要使用此账户的同事） '
        # emaillists = username+displayname + '申请新建公共邮箱：' + pumail + '，显示名称：'+maildisplay+'，公共邮箱管理者账号：'+usadaccount+'，您可以登录平台对审批单进行审批！'
        email_data = {'emaillists': emaillists}
        template = "mailmould/sendmailpassword.html"
        to_list = [mangervalue['message'][0]['mail']]
        send_email_by_template(subject, template, email_data, to_list)
        return True
    except Exception as e:
        log.log(returnid=0, message="公共邮箱创建异常"+str(evavalue), issuccess=0, inparameters=message,
                methodname="new_pubmail", types="exchange")
        print(e)





def mailgroupapply(request):
    post = request.POST
    hasout = post.get("mySwitch11")
    mail = post.get("mail")
    displaynamevalue = post.get("displaynamevalue")
    usadaccount = post.get("usadaccount")
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    applytype='新建邮箱群组'
    types='EX'
    log = logmanager()
    try:
        newgroupmessagevalue = {"hasout":hasout,"mail":mail,"displaynamevalue":displaynamevalue,"usadaccount":usadaccount}
        aa = str(newgroupmessagevalue)
        process = get_api("process")
        if process:
            insert_pubmailflow_processs = insert_pubmailflow_process(ip, username, displayname, types, applytype, mail, director='系统', message=str(aa))
            if insert_pubmailflow_processs:
                process_outgoings = process_outgoing({"status": 0, "message": {"id":insert_pubmailflow_processs['id'], "username": username, "displayname": displayname, "types": types,"applytype": applytype, "applydetail": mail}})
                if process_outgoings['status'] == 0:
                    status = True
                else:
                    status = False
            else:
                status = False
        else:
            mange = getmanger(username,"mailgroumanger")
            if mange != False:
                flowmail=insert_pubmailflow(ip,username,displayname,types,applytype,mail,mange,aa)
                if flowmail==():
                    status= True
                    log.log(returnid=1,username=usadaccount,ip=ip,message=applytype+aa,issuccess=1,methodname="mailgroupapply",types="exchange")
                    mangervalue = adapi().Initialapi("GetobjectProperty", objects=mange, objectClass="user")
                    if mangervalue['isSuccess']:
                        if hasout:
                            hasoutvalue = "开启群组身份验证"
                        else:
                            hasoutvalue = "不开启群组身份验证"
                        subject = u'您有一个新申请单待审批'
                        emaillists = username+displayname + '申请邮箱群组：' + mail + '，显示名称：'+displaynamevalue+'，管理者账号：'+usadaccount+'，'+hasoutvalue+'，您可以登录平台对审批单进行审批！'
                        email_data = {'emaillists': emaillists}
                        template = "mailmould/sendmailpassword.html"
                        to_list = [mangervalue['message'][0]['mail']]
                        send_email_by_template(subject, template, email_data, to_list)
                else:
                    status =False
                    log.log(returnid=1,username=usadaccount,ip=ip,message=applytype+aa,issuccess=0,methodname="mailgroupapply",types="exchange")
            else:
                status = False
                log.log(returnid=0, message=username + "申请新建邮箱群组", issuccess=0, inparameters="查询不到" + username + "主管",
                        methodname="mailgroupapply", types="exchange")
    except Exception as e:
        status = False
        log.log(returnid=0, message=username + "申请新建邮箱群组", issuccess=0, inparameters=str(e),
                methodname="mailgroupapply", types="exchange")
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#公共邮箱申请
def pumailuserapply(request):
    log = logmanager()
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    post = request.POST
    pumail = post.get("pumail")
    maildisplay = post.get("maildisplay")
    usadaccount = post.get("usadaccount")
    try:
        applytype='新建公共邮箱'
        types='EX'
        mailmess={"mail":pumail,"displaynamevalue":maildisplay,"usadaccount":usadaccount}
        process = get_api("process")
        if process:
            insert_pubmailflow_processs = insert_pubmailflow_process(ip, username, displayname, types, applytype, pumail, director='系统', message=str(mailmess))
            if insert_pubmailflow_processs:
                process_outgoings = process_outgoing({"status": 0, "message": {"id":insert_pubmailflow_processs['id'], "username": username, "displayname": displayname, "types": types,"applytype": applytype, "applydetail": pumail}})
                if process_outgoings['status'] == 0:
                    status = True
                else:
                    status = False
            else:
                status = False
        else:
            mange = getmanger(username,"pubmailmanger")
            if mange != False:
                flowmail=insert_pubmailflow(ip,username,displayname,types,applytype,pumail,mange,str(mailmess))
                # maillog=insert_pubmail(username,displayname,pumail,maildisplay,depment,usadaccount)
                if flowmail==():
                    log.log(returnid=1, username=usadaccount, ip=ip, message=username+applytype + str(mailmess), issuccess=1,
                            inparameters=str(flowmail),methodname="pumailuserapply", types="exchange")
                    status= True
                    mangervalue = adapi().Initialapi("GetobjectProperty", objects=mange, objectClass="user")
                    if mangervalue['isSuccess']:
                        subject = u'您有一个新申请单待审批'
                        emaillists = '账号' + username + '(' + displayname + ')' + ',申请新建公共邮箱：' + pumail + '，显示名称：' + maildisplay + '，公共邮箱管理者账号：' + usadaccount + '，您可以登录平台对审批单进行审批！'
                        # emaillists = username+displayname + '申请新建公共邮箱：' + pumail + '，显示名称：'+maildisplay+'，公共邮箱管理者账号：'+usadaccount+'，您可以登录平台对审批单进行审批！'
                        email_data = {'emaillists': emaillists}
                        template = "mailmould/sendmailpassword.html"
                        to_list = [mangervalue['message'][0]['mail']]
                        send_email_by_template(subject, template, email_data, to_list)
                else:
                    log.log(returnid=0, username=usadaccount, ip=ip, message=applytype + str(mailmess), issuccess=0,
                            inparameters=str(flowmail),methodname="pumailuserapply", types="exchange")
                    status =False
            else:
                log.log(returnid=0, message=username + "申请公共邮箱出现异常", issuccess=0, inparameters="查询不到"+username+"主管",
                        methodname="pumailuserapply", types="exchange")
                status = False
    except Exception as e:
        status = False
        log.log(returnid=0, message=usadaccount +"申请公共邮箱出现异常", issuccess=0, inparameters=str(e),
                methodname="pumailuserapply", types="exchange")
    result = {'status':status}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response
