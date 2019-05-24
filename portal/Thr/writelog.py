# -*- coding: utf-8 -*-
import threading
from time import sleep
from admin_account.dbinfo import dbinfo_insert_log



class writelog(threading.Thread):
    """send wechat"""
    def __init__(self,username,datetimevalue,ip,returnid,message,issuccess,inparameters,methodname,returnparameters,types):
        self.username = username
        self.datetimevalue = datetimevalue
        self.returnid = returnid
        self.message = message
        self.issuccess = issuccess
        self.ip = ip
        self.inparameters = inparameters
        self.methodname = methodname
        self.returnparameters = returnparameters
        self.types = types
        threading.Thread.__init__(self)
    def run(self):
        dbinfo_insert_log(self.username,self.datetimevalue,self.ip,self.returnid,self.message,self.issuccess,self.inparameters,self.methodname,self.returnparameters,self.types)


def writelog_thr(username,datetimevalue,ip,returnid,message,issuccess,inparameters,methodname,returnparameters,types):
    send_Exc = writelog(username,datetimevalue,ip,returnid,message,issuccess,inparameters,methodname,returnparameters,types)
    send_Exc.start()

