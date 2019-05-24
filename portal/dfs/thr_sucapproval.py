# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 16:30
# @Author  :

import threading
from datetime import datetime
#主管（代理人）一键审批同意的多线程
from adapi.ad_api import adapi
from dfs.dbinfo import *
from sendmail.sendmail import send_email_by_template


class thr_allsucapproval_up(threading.Thread):
    def __init__(self,username,firstcelllist):
        self.username = username
        self.firstcelllist = firstcelllist   # folw表ids list
        threading.Thread.__init__(self)
    def run(self):
        for i in range(len(self.firstcelllist)):
            sameadaccount = checkdiretorissamerelation(self.firstcelllist[i])
            sameadaccount_director_adaccount =sameadaccount.get('director_adaccount','')#主管的AD账号
            sameadaccount_relation_adaccount = sameadaccount.get('relation_adaccount', '')  # 文件夹管理员的AD账号
            sameadaccount_authority_applicant = sameadaccount.get('authority_applicant', '')  # 申请人的AD账号
            sameadaccount_username = sameadaccount.get('username', '')  # 使用人的AD账号
            sameadaccount_group_name = sameadaccount.get('group_name', '')  # 组名
            #判断主管和文件夹管理员 or 文件夹管理员和申请人，使用人  是同一人
            if sameadaccount_director_adaccount==sameadaccount_relation_adaccount or sameadaccount_relation_adaccount==sameadaccount_username or sameadaccount_relation_adaccount==sameadaccount_authority_applicant:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                approvalresult = directorapproval('1', now, '1', self.firstcelllist[i])
                relationapprovalresult = relationapprovaldb('1', now, '2', self.firstcelllist[i])
                if relationapprovalresult == 1 and approvalresult == 1:
                    #添加权限组
                    AddUserToGroups = adapi().Initialapi("AddUserToGroup", sAMAccountName=sameadaccount_username, groupname=sameadaccount_group_name)
                    if AddUserToGroups['isSuccess'] or "对象已存在" in AddUserToGroups['message']:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        opresult = operate(now, '3', self.firstcelllist[i])
                    else:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        opresults = operate(now, '6', self.firstcelllist[i])
                else:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    opresults = operate(now, '6', self.firstcelllist[i])
            else:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                approvalresult = directorapproval('1', now, '1', self.firstcelllist[i])
        if len(self.firstcelllist)==1:
            oneusername = showrelationemail(self.firstcelllist[0], 1) #主管已审批，发送给文件夹关联人
            threeusername =showrelationemail(self.firstcelllist[0], 3)#权限已开通，发送给用户
        else:
            oneusername = checkusernameissamerelation(tuple(self.firstcelllist),1)  # #主管已审批，发送给文件夹关联人
            threeusername = checkusernameissamerelation(tuple(self.firstcelllist),3)  # #权限已开通，发送给用户
        if oneusername:#主管已审批，发送给文件夹关联人
            relation_adaccounts = list()
            for i in range(len(oneusername)):
                relation_adaccounts.append(oneusername[i]['relation_adaccount'])
            for x in relation_adaccounts:
                while relation_adaccounts.count(x) > 1:
                    del relation_adaccounts[relation_adaccounts.index(x)]  # 去除文件夹管理员AD 的重复项
            for relation_adaccount in relation_adaccounts:
                emaillists = showrelationadaccountemail(relation_adaccount)
                subject = u'文件夹权限_文件夹管理员审批'
                email_data = {'emaillists': emaillists}
                template = "dfsweb/common/relationemail.html"
                GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=relation_adaccount, objectClass='user')
                if GetobjectPropertys['isSuccess']:
                    mail = GetobjectPropertys['message'][0].get("mail", "")
                    if mail:
                        to_list = [mail]
                        send_email_by_template(subject, template, email_data, to_list)
        if threeusername:##权限已开通，发送给用户
            sucapproval_usernames = list()
            for i in range(len(threeusername)):
                sucapproval_usernames.append(threeusername[i]['username'])
            for x in sucapproval_usernames:
                while sucapproval_usernames.count(x) > 1:
                    del sucapproval_usernames[sucapproval_usernames.index(x)]  # 去除文件夹管理员AD 的重复项
            if len(self.firstcelllist)==1:
                subject = u'文件夹权限_权限已开通'
                email_data = {'emaillists': threeusername}
                template = "dfsweb/common/successmail.html"
                GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=threeusername[0]['username'], objectClass='user')
                if GetobjectPropertys['isSuccess']:
                    mail = GetobjectPropertys['message'][0].get("mail", "")
                    if mail:
                        to_list = [mail]
                        send_email_by_template(subject, template, email_data, to_list)
            else:
                for sucapproval_username in sucapproval_usernames:
                    emaillists = showidemail(tuple(self.firstcelllist),sucapproval_username)
                    subject = u'文件夹权限_权限已开通'
                    email_data = {'emaillists': emaillists}
                    template = "dfsweb/common/successmail.html"
                    GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=sucapproval_username, objectClass='user')
                    if GetobjectPropertys['isSuccess']:
                        mail = GetobjectPropertys['message'][0].get("mail", "")
                        if mail:
                            to_list = [mail]
                            send_email_by_template(subject, template, email_data, to_list)


def thr_allsucapproval(username,firstcelllist):
    updateallsucapproval = thr_allsucapproval_up(username,firstcelllist)
    updateallsucapproval.start()