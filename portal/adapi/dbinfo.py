# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 10:10
from datetime import datetime
from dbinfo_ad.newdbtest import dbinfo


def get_md5(domain):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT MD5 from api_configuration where domain= %s"
        conncur.execute(connsql, domain)
        MD5 = conncur.fetchone()
        conn.commit()
        conn.close()
        return MD5['MD5']
    except Exception as e:
        print(e)
        return None


def insert_sendmail(mailcount,password, mailserver,mailaddress):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from sendmailsite"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE sendmailsite SET mailcount=%s,password=%s, mailserver=%s,mailaddress=%s,datetime=%s WHERE id =%s"
            conncur.execute(connsql, (mailcount,password, mailserver,mailaddress,createtime,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO sendmailsite (mailcount,password, mailserver,mailaddress,datetime) VALUES (%s,%s,%s,%s,%s) "
            conncur.execute(connsql, (mailcount, password, mailserver, mailaddress, createtime))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False



#配置项保存
# def saveconfig(ad_domain,network,vpn,wifi,inputpubmailou,inputmailgroupou,inputewge,inputips,inputjzou,inputjzgroup,inputunlockgroup,inputpubmailDB,inputpubmaillanwei,inputpwdlen):
#     conn = dbinfo()
#     try:
#         conncur = conn.cursor()
#         connsql = "INSERT INTO management_configuration (domain,internet_group,wifi_group,vpn_group,part_time_group,NoLockGroup,jz_account_dn,mailgroupdefaultOU,pubmailfence,pubmailou,pubmailDB,passwordlength,pwdtips,lengthpwd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
#         conncur.execute(connsql, (ad_domain,network,wifi,vpn,inputjzgroup,inputunlockgroup,inputjzou,inputmailgroupou,inputpubmaillanwei,inputpubmailou,inputpubmailDB,inputewge,inputips,inputpwdlen))
#         histroycounts = conncur.fetchall()
#         conn.commit()
#         conn.close()
#         return histroycounts
#     except Exception as e:
#         print(e)
#         return False

#更新基础信息
def update_config(ad_domain,network,vpn,wifi,inputpubmailou,inputmailgroupou,inputewge,inputips,inputjzou,inputjzgroup,inputunlockgroup,inputpubmailDB,inputpubmaillanwei,inputpwdlen):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from management_configuration"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE management_configuration SET domain=%s,internet_group=%s,wifi_group=%s,vpn_group=%s,part_time_group=%s,NoLockGroup=%s,jz_account_dn=%s,mailgroupdefaultOU=%s,pubmailfence=%s,pubmailou=%s,pubmailDB=%s,passwordlength=%s,pwdtips=%s,lengthpwd=%s WHERE id =%s"
            conncur.execute(connsql, (ad_domain,network,wifi,vpn,inputjzgroup,inputunlockgroup,inputjzou,inputmailgroupou,inputpubmaillanwei,inputpubmailou,inputpubmailDB,inputewge,inputips,inputpwdlen,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO management_configuration (domain,internet_group,wifi_group,vpn_group,part_time_group,NoLockGroup,jz_account_dn,mailgroupdefaultOU,pubmailfence,pubmailou,pubmailDB,passwordlength,pwdtips,lengthpwd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            conncur.execute(connsql, (ad_domain, network, wifi, vpn, inputjzgroup, inputunlockgroup, inputjzou, inputmailgroupou,inputpubmaillanwei, inputpubmailou, inputpubmailDB, inputewge, inputips, inputpwdlen))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#保存固定审批人
def mangersql(inputpub,inputgroup,inputdfs,inputnetwork,inputvpn):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO fixmanger (pubmailmanger,mailgroumanger, dfsmanger,networkmanger,vnpmanger,status,date) VALUES (%s,%s,%s,%s,%s,1,%s) "
        conncur.execute(connsql, (inputpub,inputgroup,inputdfs,inputnetwork,inputvpn,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
#更新固定审批人
def mangersqlupdate(inputpub,inputgroup,inputdfs,inputnetwork,inputvpn):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from fixmanger"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE fixmanger SET pubmailmanger=%s,mailgroumanger=%s, dfsmanger=%s,networkmanger=%s,vnpmanger=%s,date=%s WHERE id =%s"
            conncur.execute(connsql, (inputpub,inputgroup,inputdfs,inputnetwork,inputvpn,createtime,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO fixmanger (pubmailmanger,mailgroumanger, dfsmanger,networkmanger,vnpmanger,status,date) VALUES (%s,%s,%s,%s,%s,1,%s) "
            conncur.execute(connsql, (inputpub,inputgroup,inputdfs,inputnetwork,inputvpn,createtime))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#审批人状态
def insermangerstau(id):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO apimessage (titlename,status, date) VALUES ('getmanger',%s,%s) "
        conncur.execute(connsql, (id,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#获取手机号接口状态
def inserphonestau(id):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO apimessage (titlename,status, date) VALUES ('usertophone',%s,%s) "
        conncur.execute(connsql, (id,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#发送短信接口状态
def sendmestaus(id):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO apimessage (titlename,status, date) VALUES ('Sendmessage',%s,%s) "
        conncur.execute(connsql, (id,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def insert_interface_c_log(ip,isSuccess, tokenid,apiname,parameter,message):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO interface_c_log (ip,isSuccess, tokenid,apiname,parameter,message,times) VALUES (%s,%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (ip,isSuccess, tokenid,apiname,parameter,message,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_apimanger(url):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO api (mess,title) VALUES (%s,'getmanger') "
        conncur.execute(connsql, (url))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_phoneurl(url):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO api (mess,title) VALUES (%s,'getuserphone') "
        conncur.execute(connsql, (url))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_sendphone(url):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO api (mess,title) VALUES (%s,'Sendmessage') "
        conncur.execute(connsql, (url))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def insert_title(title,heard):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO titleshow (title,heard,date) VALUES (%s,%s,%s) "
        conncur.execute(connsql, (title,heard,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def update_title(title,heard):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from titleshow"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE titleshow SET title=%s,heard=%s,date=%s WHERE id =%s"
            conncur.execute(connsql, (title,heard,createtime,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO titleshow (title,heard,date) VALUES (%s,%s,%s) "
            conncur.execute(connsql, (title, heard, createtime))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False



def searchmind():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from remind "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def searchsendmail():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from sendmailsite limit1"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
#审批条数
def searchflowdcount(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select count(* ) from flow_director where director=%s and directorstatus=0"
        conncur.execute(connsql, (username))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

#获取域名
def get_domain():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT domain from management_configuration limit1 "
        conncur.execute(connsql,)
        domain = conncur.fetchone()
        conn.commit()
        conn.close()
        return domain['domain']
    except Exception as e:
        print(e)
        return None

#获取权限组名
def get_PermissionsGrops():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * from management_configuration"
        conncur.execute(connsql,)
        PermissionsGrops = conncur.fetchone()
        conn.commit()
        conn.close()
        return PermissionsGrops
    except Exception as e:
        print(e)
        return None

#获取审批人接口状态
def genmangemessage():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from  apimessage where titlename='getmanger'"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#获取审批人接口api
def genmangeurl():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from  api where title='getmanger'"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#获取审批人接口api
def genmuser():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from  api where title='getuserphone'"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#获取审批人接口api
def sendmeasage():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from  api where title='Sendmessage'"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#获取网页标题
def shwotitle():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from titleshow "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#用户接口状态
def delmangeruser(title):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = " Delete from apimessage where titlename=%s"
        conncur.execute(connsql, (title))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False




#删除api
def delapimanger(tips):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = " Delete from api where title=%s"
        conncur.execute(connsql, (tips))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False




#删除
def delmanger():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = " Delete from fixmanger"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#删除
def delconfiger():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE management_configuration SET domain=NULL,internet_group=NULL,wifi_group=NULL,vpn_group=NULL,part_time_group=NULL,NoLockGroup=NULL,jz_account_dn=NULL,mailgroupdefaultOU=NULL,pubmailfence=NULL,pubmailou=NULL,pubmailDB=NULL,passwordlength=NULL,pwdtips=NULL,lengthpwd=NULL"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#删除
def delsendconfig():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = " Delete from sendmailsite"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
#删除标题
def deltitleconfig():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = " Delete from titleshow"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#获取审批人接口
def genmangemessageshow():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from  fixmanger "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#固定审批人接口查询
def genmangehow(type):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select %s from  fixmanger" %(type)
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
#兼职账号写入数据库
def insert_jzcountlog(jzcount,displayname,deadtime,datetime,phone,sqaccount,sqname,sqmail,status):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO jztimecount (jzcount,displayname,deadtime,datetime,phone,sqaccount,sqname,sqmail,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (jzcount,displayname,deadtime,datetime,phone,sqaccount,sqname,sqmail,status))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#有效账号查询
def get_Effective_account(sqaccount):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where sqaccount=%s and status=1 "
        conncur.execute(connsql, (sqaccount))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#有效账号查询
def get_Effective_accountALL(status):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where status=%s "
        conncur.execute(connsql, (status))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def searid_jzphone(phone):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where phone=%s and status=1 "
        conncur.execute(connsql, (phone))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#根据数据库ID查ZJ账号属性
def searid_jzcountid(id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where id=%s  "
        conncur.execute(connsql, (id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def update_jzcountid(now,id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE jztimecount SET deadtime=%s WHERE id =%s "
        conncur.execute(connsql, (now,id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#更新数据库账号状态
#############数据库status含义+############
# status = 1  正常账号
# status= 2   创建成功，修改到期时间失败（需从AD中把账号删除）
# status = 3  申请人主动关闭
# status = 4  自动关闭
#status = 5  AD账号被管理员从AD中手动删除，同时申请人或管理员在页面执行关闭操作
#########################################
def updel_jzcountid(status,id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE jztimecount SET status=%s WHERE id =%s "
        conncur.execute(connsql, (status,id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def upde_jzcountidmanger(sqaccount,sqname,sqmail,id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE jztimecount SET sqaccount=%s,sqname=%s,sqmail=%s WHERE id =%s "
        conncur.execute(connsql, (sqaccount,sqname,sqmail,id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False



def updel_jzpwd(id,password):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE jztimecount SET password=%s WHERE id =%s "
        conncur.execute(connsql, (password,id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def sear_jzcount(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where username=%s and status=1 "
        conncur.execute(connsql, (username))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
#获取3天内到期账号
def Remind_due(status,deadtime):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where status=%s and deadtime <= %s"
        conncur.execute(connsql, (status,deadtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#获取到期账号 ('%Y-%m-%d %H:%M:%S') 对比
def get_Close_account(status,nowdeadtime):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from jztimecount where status=%s and deadtime <= %s"
        conncur.execute(connsql, (status,nowdeadtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False




def updatepumailuser(id,status):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE flow_director SET directorstatus=1,flowstatus=%s ,endtime=%s WHERE id =%s "
        conncur.execute(connsql, (status,createtime,id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)

def updatepumailuser_allow(id, status):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE flow_director SET directorstatus=2,flowstatus=%s ,endtime=%s WHERE id =%s "
        conncur.execute(connsql, (status, createtime, id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)


#申请信息查看
def searchover(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from flow_director where adaccount=%s order by submittime desc "
        conncur.execute(connsql, (username))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#申请信息详情查看
def showid(id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from flow_director where id=%s"
        conncur.execute(connsql, (id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
#条数查询
def searchcount(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select count(* ) from flow_director where adaccount=%s"
        conncur.execute(connsql, (username))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#审批信息查看
def searchrevier(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from flow_director where director=%s and directorstatus =0  order by submittime desc"
        conncur.execute(connsql, (username))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#孙浩日志
def searchreviersystemlog(startPos,size):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from systemlog order by datetimevalue DESC LIMIT %s ,%s"
        conncur.execute(connsql, (startPos,size))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#条数查询
def searchreviercont(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select count(* ) from flow_director where director=%s and directorstatus =0 "
        conncur.execute(connsql, (username))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

# 系统日志总数查询
def searchrsystemlog():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select count(* ) from systemlog"
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#获取数据库邮箱信息
def getdb_mail(mail):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * from flow_director where types='EX' and applydetail=%s and directorstatus =0 "
        conncur.execute(connsql,(mail))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False



# 查询账号建立信息
def getmailou_new():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * from management_configuration"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#更新公共邮箱状态
def updatepumail(mailadd):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE mail_publicmail SET status=1,datetime=%s WHERE pubmail =%s "
        conncur.execute(connsql, (createtime,mailadd))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
#接口查询
def getmangerapi(getmanger):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT mess from api where title =%s"
        conncur.execute(connsql,(getmanger))
        histroycounts = conncur.fetchall()[0]
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False



def insert_pubmailflow(ip,adaccount,displayname,types,applytype,applydetail,director=None,message=None):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO flow_director (ip,adaccount,displayname,types,applytype,applydetail,submittime,directorstatus,flowstatus,director,message) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (ip,adaccount,displayname,types,applytype,applydetail,createtime,0,0,director,message))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_pubmailflow_process(ip, adaccount, displayname, types, applytype, applydetail, director=None, message=None):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO flow_director (ip,adaccount,displayname,types,applytype,applydetail,submittime,directorstatus,flowstatus,director,message) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (ip, adaccount, displayname, types, applytype, applydetail, createtime, 0, 0, director, message))
        conn.commit()
        connsql = "SELECT * from flow_director where adaccount=%s and applydetail=%s and submittime = %s"
        conncur.execute(connsql, (adaccount, applydetail, createtime))
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#
# def insert_pubmail(username, displayname, pumail, maildisplay, depment, usadaccount):
#     createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     conn = dbinfo()
#     try:
#         conncur = conn.cursor()
#         connsql = "INSERT INTO mail_publicmail (username,displayname,pubmail,maildisname,depment,manger,status,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
#         conncur.execute(connsql, (username, displayname, pumail, maildisplay, depment, usadaccount, 0, createtime))
#         histroycounts = conncur.fetchall()
#         conn.commit()
#         conn.close()
#         return histroycounts
#     except Exception as e:
#         print(e)
#         return False