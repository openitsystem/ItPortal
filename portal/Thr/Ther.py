# -*- coding: utf-8 -*-
import threading

#继承Thread，需要实现run方法
from adapi.ad_api import adapi
from adapi.dbinfo import updatepumailuser
from internet.views import allowtobeIntrenet
from logmanager.views import logmanager

from mail.views import new_mailgroup, mailgrouppermession, new_pubmail

from mail.views import new_mailgroup,mailgrouppermession,allowtobemanager,allowtobepublicmailmanager
from sendmail.sendmail import send_email_by_template


def sendmailtouser(emaillistsvalue,applydetail,useraccount):
        subject = u'申请单有了新进度！'
        emaillists = "你的申请单"+str(emaillistsvalue)+applydetail+'有了新的审批进度，请登录平台查看！ '
        email_data = {'emaillists': emaillists}
        template = "mailmould/sendmailpassword.html"
        adapi().Initialapi("GetobjectProperty",objects=useraccount,objectClass="user")
        to_list = [adapi().Initialapi("GetobjectProperty",objects=useraccount,objectClass="user")['message'][0]['mail']]
        send_email_by_template(subject, template, email_data, to_list)

class flow_agree_class(threading.Thread):
    def __init__(self,folowvalue):
        self.id = folowvalue['id']
        self.ip = folowvalue['ip']
        self.adaccount = folowvalue['adaccount']
        self.displayname = folowvalue['displayname']
        self.types = folowvalue['types']
        self.applytype = folowvalue['applytype']
        self.applydetail = folowvalue['applydetail']
        self.submittime = folowvalue['submittime']
        self.director = folowvalue['director']
        self.directorstatus = folowvalue['directorstatus']
        self.flowstatus = folowvalue['flowstatus']
        self.endtime = folowvalue['endtime']
        self.message = folowvalue['message']
        threading.Thread.__init__(self)
    def run(self):
        try:
            applytypevalue = None
            if self.applytype == "新建邮箱群组":
                applytypevalue = "新建邮箱群组"
                new_mailgroup(self.id, self.applydetail, self.message)
            elif self.applytype == "新建公共邮箱":
                applytypevalue = "新建公共邮箱"
                new_pubmail(self.id, self.applydetail, self.message)
            elif self.applytype == "邮箱群组权限申请":
                applytypevalue = "邮箱群组权限申请"
                mailgrouppermession(self.id, self.applydetail, self.message)
            elif self.applytype == "成为邮箱群组管理者":
                applytypevalue = "成为邮箱群组管理者"
                allowtobemanager(self.id, self.applydetail, self.message)
            elif self.applytype == "成为公共邮箱管理者":
                applytypevalue = "成为公共邮箱管理者"
                allowtobepublicmailmanager(self.id, self.applydetail, self.message)
            elif self.applytype == "申请上网权限组权限" or self.applytype == "申请无线权限组权限" or self.applytype == "申请VPN权限组权限" or self.applytype == "申请权限组权限":
                applytypevalue = self.applytype
                allowtobeIntrenet(self.id, self.message)
            sendmailtouser(applytypevalue,self.applydetail,self.adaccount)

        except Exception as e:
            log = logmanager()
            log.log(returnid=0, message="审批"+self.id+"申请单", issuccess=0, methodname="flow_agree", returnparameters=str(e),types="other")
            updatepumailuser(self.id, 2)


def flow_agree(folowvalue):
    send_Exc = flow_agree_class(folowvalue)
    send_Exc.start()