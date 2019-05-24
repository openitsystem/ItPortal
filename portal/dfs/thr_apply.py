# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 20:33
# @Author  :
import threading
from datetime import datetime
#继承Thread，需要实现run方法
# 申请权限的多线程
from adapi.ad_api import GetobjectProperty, getmanger, adapi
from admin_account.dbinfo import dbinfo_select_global_configuration
from dfs.dbinfo import get_management_configuration, showtreeid, showgroupname, show_level2name, add_dfs_flow, showmyemailflowdir, checkflow, get_api
from dfs.thr_process import process_outgoing
from sendmail.sendmail import send_email_by_template


class thr_apply_up(threading.Thread):
    def __init__(self,adusername,level_id_list,read_m_list,account_list):
        self.adusername = adusername     #当前登陆用户的AD
        self.level_id_list = level_id_list   # 目录ID#
        self.read_m_list=read_m_list   ##list
        self.account_list=account_list  # AD账号
        mysqlallvalue = dbinfo_select_global_configuration()
        if mysqlallvalue:
            self.domain = str(mysqlallvalue[0]['ad_domain'])
        else:
            self.domain ="test"
        threading.Thread.__init__(self)
    def run(self):
        try:
            process = get_api("process")
            director_account_list =[]
            for i in range(len(self.account_list) - 1):
                username = self.account_list[i]
                if username:
                    GetobjectPropertys = GetobjectProperty(username, 'user', self.domain, tokenid=None, ip=None)
                    if GetobjectPropertys['isSuccess']:
                        displayName = GetobjectPropertys['message'][0].get('displayName','')
                    else:
                        displayName= ""
                    #获取treeid 和需要添加的权限组
                    treelists = self.level_id_list[i].split('-')
                    treeids = showtreeid(treelists[0], treelists[1], treelists[2])
                    tree_id= treeids.get('tree_id', '')
                    group_name = showgroupname(tree_id, self.read_m_list[i]).get("group_name",'')
                    #根据AD账号获取主管，AD ,姓名，邮箱
                    manger = getmanger(username, "dfsmanger")
                    get_management_configurations = get_management_configuration()
                    if process:
                        director_name ="系统"
                        director_account = "系统"
                        director_mail = "系统"
                    else:
                        if manger:
                            director_account = manger
                            mangervalue = adapi().Initialapi("GetobjectProperty", objects=manger, objectClass="user")
                            if mangervalue['isSuccess']:
                                director_mail = mangervalue['message'][0].get("mail",'')
                                director_name = mangervalue['message'][0].get("displayName", '')
                            else:
                                director_name = get_management_configurations.get('dfs_relation_name', '')
                                director_account = get_management_configurations.get('dfs_relation', '')
                                director_mail = get_management_configurations.get('dfs_relation_mail', '')
                        else:
                            director_name =get_management_configurations.get('dfs_relation_name','')
                            director_account = get_management_configurations.get('dfs_relation', '')
                            director_mail = get_management_configurations.get('dfs_relation_mail', '')
                    # 根据 level2_id 查找文件夹管理员 ，如果没有则使用默认
                    relations = show_level2name(treelists[1])
                    level2_manager_name = relations.get('level2_manager_name', '')
                    level2_manager = relations.get('level2_manager', '')
                    level2_manager_mail = relations.get('level2_manager_mail', '')
                    if not level2_manager:
                        level2_manager_name = get_management_configurations.get('dfs_relation_name', '')
                        level2_manager = get_management_configurations.get('dfs_relation', '')
                        level2_manager_mail = get_management_configurations.get('dfs_relation_mail', '')
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if tree_id and group_name and director_account and level2_manager:#确认数据无错，插数据库
                        flowidcounts = checkflow(username, group_name)# 检查flow表是否有相同数据
                        if flowidcounts['counts'] == 0:
                            add_dfs_flows = add_dfs_flow(username, displayName, treeids['tree_id'], group_name, now, director_name, director_account, level2_manager_name,level2_manager, 0,self.adusername ) #添加
                            if process and add_dfs_flows:
                                value = {"status":0, "message": {"id":add_dfs_flows['id'],"username":username,"displayname":displayName,"types":"DFS","applytype":"申请文件夹权限","applydetail":group_name}}
                                process_outgoing(value)
                        director_account_list.append([director_account,director_mail])

            if not process:
                for x in director_account_list:
                    while director_account_list.count(x) > 1:
                        del director_account_list[director_account_list.index(x)]  # 去除director_account 的重复项\
                # 发送邮件
                for i in range(len(director_account_list)):
                    emaillists = showmyemailflowdir(director_account_list[i][0]) #根据主管AD 账号获取工单
                    sendnumber = len(emaillists)
                    if sendnumber > 0:
                        subject = u'文件夹权限_主管审批'
                        email_data = {'emaillists': emaillists, 'username': self.adusername}
                        template = "dfsweb/common/directoremail.html"
                        if director_account_list[i][1]:
                            to_list = [director_account_list[i][1], ]
                            send_email_by_template(subject, template, email_data, to_list)
                        # 微信发送申请信息给主管
                        # sendjobnumber = oalistslist[i][3]
                        # sendmsg = '您有%' % (sendnumber) + '\n' + '请您登陆平台进行审批'
                        # sendwechat(sendjobnumber, sendmsg)
        except Exception as e:
            print(e)

#DFS 权限申请,异步
def thr_apply_update(adusername,level_id_list,read_m_list,account_list):
    updateauthority = thr_apply_up(adusername,level_id_list,read_m_list,account_list)
    updateauthority.start()