import datetime
import re
import threading

from urllib3 import request

from adapi.ad_api import Send_message, adapi
from adapi.dbinfo import Remind_due, get_Close_account, get_PermissionsGrops, updel_jzcountid
from apscheduler.scheduler import Scheduler

from logmanager.views import logmanager
from sendmail.sendmail import send_email_by_template, send_html_email
from tools.passwordreminder import senduserpassword


def triggerjob():
    return 1

#获取3天内到期账号
def Sendsched_account():
    deadtime = datetime.datetime.now() + datetime.timedelta(days=int(3))
    deadtime_new = deadtime.strftime('%Y-%m-%d %H:%M:%S')
    status='1'
    account =Remind_due(status,deadtime_new)
    return account

#获取过期关闭账号
def getCloseaccount():
    nowdeadtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # deadtime_new = deadtime.strftime('%Y-%m-%d %H:%M:%S')
    status='1'
    account =get_Close_account(status,nowdeadtime)
    return account



#账号到期提醒
class Sendsched(threading.Thread):
    """send wechat"""
    def __init__(self,):
        threading.Thread.__init__(self)
    def run(self):
        log = logmanager()
        account=Sendsched_account()
        today = datetime.datetime.now()  # 获取当天时间
        today_new = today.strftime('%Y-%m-%d')  # 将时间格式转换为字符串
        tomorrow = today + datetime.timedelta(days=1)  # 拼接明天时间（到期前1天）
        tomorrow = tomorrow.strftime('%Y-%m-%d')  # 对时间格式化,转换成字符串
        The_day_after_tomorrow = today + datetime.timedelta(days=2)  # 拼接后天时间（到期前2天）
        The_day_after_tomorrow = The_day_after_tomorrow.strftime('%Y-%m-%d')  # 对时间格式化,转换成字符串
        Three_days_from_now = today + datetime.timedelta(days=3)  # 拼接大后天时间（到期前3天）
        Three_days_from_now = Three_days_from_now.strftime('%Y-%m-%d')  # 对时间格式化,转换成字符串
        if account!='':
            for i in account:
                deadtime=i['deadtime']
                deadtime_new=deadtime.strftime('%Y-%m-%d %H:%M:%S')
                expire=deadtime
                jzcount = i['jzcount']
                displayname = i['displayname']
                phone=i['phone']
                sqname=i['sqname']
                sqmail=i['sqmail']
                expire = expire.strftime('%Y-%m-%d')  # 将datetime.date形式 转换成字符串
                message= '您好，您的兼职账号'+jzcount+'将于'+ deadtime_new +'到期，如需继续使用请联系'+sqname+'进行续约,到期后将会被删除,并无法恢复,如不需使用，请忽略此条信息'
                mailmessage='您好，兼职账号'+jzcount+'将于'+ deadtime_new +'到期，如需继续请及时续约,到期后将会被删除,并无法恢复,如不需使用请及时关闭或等待自动关闭'
                if expire == today_new :
                   subject = "兼职账号关闭当天提醒"
                   Send_message(phone,message)
                   tolist=[sqmail]
                   Send_mail=send_html_email(subject,mailmessage,tolist)
                   log.log(returnid=1, username='定时任务到期通知',message=jzcount+"兼职账号关闭当天提醒"+'通知手机'+phone+'通知MAIL'+tolist,
                           methodname="Sendsched",types="AD", issuccess=1)
                if expire == tomorrow:  # 到期前1天提醒，时间字符串对比
                    subject = "兼职账号关闭前一天提醒"
                    Send_message(phone, message)
                    tolist = [sqmail]
                    Send_mail = send_html_email(subject, mailmessage, tolist)
                    log.log(returnid=1, username='定时任务到期通知',
                            message=jzcount + "兼职账号关闭前一天提醒" + '通知手机' + phone + '通知MAIL' + tolist,
                            methodname="Sendsched", types="AD", issuccess=1)
                if expire == The_day_after_tomorrow:  # 到期前2天提醒，时间字符串对比
                    subject = "兼职账号关闭前两天提醒"
                    Send_message(phone, message)
                    tolist = [sqmail]
                    Send_mail = send_html_email(subject, mailmessage, tolist)
                    log.log(returnid=1, username='定时任务到期通知',
                            message=jzcount + "兼职账号关闭前两天提醒" + '通知手机' + phone + '通知MAIL' + tolist,
                            methodname="Sendsched", types="AD", issuccess=1)
                if expire == Three_days_from_now:  # 到期前3天提醒，时间字符串对比
                    subject = "兼职账号关闭前三天提醒"
                    Send_message(phone, message)
                    tolist = [sqmail]
                    Send_mail = send_html_email(subject, mailmessage, tolist)
                    log.log(returnid=1, username='定时任务到期通知',
                           message=jzcount + "兼职账号关闭前三天提醒" + '通知手机' + phone + '通知MAIL' + tolist,
                           methodname="Sendsched", types="AD", issuccess=1)
            result = False
            return result
        else:
            log.log(returnid=0, username='定时任务',
                    message='账号为空，没有执行',
                    methodname="Sendsched", types="AD", issuccess=0)
            result = False
            return result



#关闭到期账号
class Close_account(threading.Thread):
    """send wechat"""
    def __init__(self,):
        threading.Thread.__init__(self)
    def run(self):
        account =getCloseaccount()
        log = logmanager()
        if account != '':
            for i in account:
                Closeaccount= i['jzcount']
                id=i['id']  #数据库ID
                status='4' # 4到期自动关闭
                nowdeadtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前时间
                jzound = get_PermissionsGrops()['jz_account_dn']  #获取兼职DN
                jzcountdn=adapi().Initialapi('ObjectExistsOU',objectName=Closeaccount,catalog='user',ouname=jzound) #判断账号是否在兼职账号OU中
                property = adapi().Initialapi('GetuseraccountExpires', objects=Closeaccount)
                if property['isSuccess']:
                    propertydate=property['message'] #从AD中获取账号到期时间
                    propertydate=datetime.datetime.strptime(propertydate, "%Y/%m/%d %H:%M:%S") # 将时间字符串转换成datetime.date形式
                    propertydate=propertydate.strftime('%Y-%m-%d %H:%M:%S') # 将datetime.date形式 转换成字符串
                    if jzcountdn==True and propertydate <= nowdeadtime:
                        dejzcount = adapi().Initialapi('delaccount', username=Closeaccount)
                        log.log(returnid=1, username='定时任务删除账号',
                                message=Closeaccount + '调用API删除账号，状态未知',
                                methodname="Close_account", types="AD", issuccess=1)
                        if dejzcount['isSuccess']:
                            log.log(returnid=1, username='定时任务删除账号',
                                    message=Closeaccount + '账号删除成功',
                                    methodname="Close_account", types="AD", issuccess=1)
                            updel_jzcountid(status,id)
                        else:
                            print('账号删除失败')
                            log.log(returnid=0, username='定时任务删除账号',
                                    message=Closeaccount + '账号删除失败',
                                    methodname="Close_account", types="AD", issuccess=0)
                    else:
                        print('账号不在特定OU或账号在AD中未到期')
                        log.log(returnid=0, username='定时任务删除账号',
                                message=Closeaccount + '删除失败，账号不在特定OU或账号在AD中未到期',
                                methodname="Close_account", types="AD", issuccess=0)
                else:
                    print ('未知错误')
                    log.log(returnid=0, username='定时任务删除账号',
                            message=Closeaccount + '未知错误',
                            methodname="Close_account", types="AD", issuccess=0)
        else:
             print('账号为空')





#发送兼职账户到期定时提醒
def sendjzsch():
    send_wechat = Sendsched()
    send_wechat.start()
    log = logmanager()
    log.log(returnid=1, username='定时通知',
            message='启动调用定时通知',
            methodname="Close_account", types="AD", issuccess=1)
#关闭到期账号
def close_account():
    close=Close_account()
    close.start()
    log = logmanager()
    log.log(returnid=1, username='定时任务删除账号',
            message='启动定时任务删除账号',
            methodname="Close_account", types="AD", issuccess=1)

# 定时任务
# 不使用守护线程
schedudler = Scheduler(daemonic=False)

# 每天11点15点，执行到期提醒
@schedudler.cron_schedule(day_of_week='0-6', hour='10', minute='01')
def quote_send_sh_job_1():
    sendjzsch()
    senduserpassword()

#定时关闭到期账号
@schedudler.cron_schedule(day_of_week='0-6', hour='23', minute='05')
def quote_send_sh_job_2():
    close_account()
schedudler.start()
#





