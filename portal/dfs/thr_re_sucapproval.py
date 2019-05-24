# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 16:30
# @Author  :

import threading
from datetime import datetime
#主管（代理人）一键审批同意的多线程
from adapi.ad_api import adapi
from dfs.dbinfo import *
from sendmail.sendmail import send_email_by_template


class thr_re_sucapproval_up(threading.Thread):
    def __init__(self,username,firstcelllist):
        self.username = username
        self.firstcelllist = firstcelllist   # folw表ids list
        threading.Thread.__init__(self)
    def run(self):
        for i in range(len(self.firstcelllist)):
            sameadaccount = checkdiretorissamerelation(self.firstcelllist[i])
            sameadaccount_username = sameadaccount.get('username', '')  # 使用人的AD账号
            sameadaccount_group_name = sameadaccount.get('group_name', '')  # 组名
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            relationapprovalresult = relationapprovaldb('1', now, '2', self.firstcelllist[i])
            if relationapprovalresult == 1 :
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
        if len(self.firstcelllist)==1:
            threeusername =showrelationemail(self.firstcelllist[0], 3)#权限已开通，发送给用户
            subject = u'文件夹权限_权限已开通'
            email_data = {'emaillists': threeusername}

            template = "dfsweb/common/successmail.html"
            GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=threeusername[0]['username'], objectClass='user')
            if GetobjectPropertys['isSuccess']:
                to_list = [GetobjectPropertys['message'][0]['mail'], ]

                send_email_by_template(subject, template, email_data, to_list)
        else:
            threeusername = checkusernameissamerelation(tuple(self.firstcelllist),3)  # #权限已开通，发送给用户
            sucapproval_usernames = list()
            for i in range(len(threeusername)):
                sucapproval_usernames.append(threeusername[i]['username'])
            for x in sucapproval_usernames:
                while sucapproval_usernames.count(x) > 1:
                    del sucapproval_usernames[sucapproval_usernames.index(x)]  # 去除文件夹管理员AD 的重复项
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


def thr_all_re_sucapproval(username,firstcelllist):
    updateallsucapproval = thr_re_sucapproval_up(username,firstcelllist)
    updateallsucapproval.start()
    


#流程审批一键同意
class thr_process_sucapproval(threading.Thread):
    def __init__(self,id):
        self.id = id
        threading.Thread.__init__(self)

    def run(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        approvalresult = directorapproval('1', now, '1', self.id)
        relationapprovalresult = relationapprovaldb('1', now, '2', self.id)
        if relationapprovalresult == 1 and approvalresult == 1:
            # 添加权限组
            sel_folder_dfs_flow_ids = sel_folder_dfs_flow_id(self.id)
            if sel_folder_dfs_flow_ids:
                AddUserToGroups = adapi().Initialapi("AddUserToGroup", sAMAccountName=sel_folder_dfs_flow_ids.get('username', ''), groupname=sel_folder_dfs_flow_ids.get('group_name', ''))
                if AddUserToGroups['isSuccess'] or "对象已存在" in AddUserToGroups['message']:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    opresult = operate(now, '3', self.id)
                else:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    opresults = operate(now, '6', self.id)
            else:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                opresults = operate(now, '6', self.id)
        else:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            opresults = operate(now, '6', self.id)
        return True
        
    
def thr_all_process_sucapproval(id):
    updateallsucapproval = thr_process_sucapproval(id)
    updateallsucapproval.start()