import threading
from adapi.ad_api import *
import datetime,time
#继承Thread，需要实现run方法
class CMailgroup(threading.Thread):
    def __init__(self,username,adaccount,groupname,time,domain):
        self.groupname = groupname
        self.username = username
        self.adaccount=adaccount
        self.time=time
        self.domain=domain
        threading.Thread.__init__(self)

    def run(self):
        timevalue = int(self.time)*60
        time.sleep(timevalue)
        result = RemoveUserFromGroup(self.adaccount,self.groupname,self.domain)
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取当前时间


def delpwdnolock(username,adaccount,groupname,time,domain):
    create_mail = CMailgroup(username,adaccount,groupname,time,domain)
    create_mail.start()
