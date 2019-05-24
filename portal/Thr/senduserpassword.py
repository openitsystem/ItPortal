# -*- coding: utf-8 -*-
import threading
from datetime import datetime
#继承Thread，需要实现run方法
from adapi.ad_api import adapi


class senduserpassword_agree_class(threading.Thread):
    def __init__(self,samaccountname,passwordexpirationdate):
        self.samaccountname = samaccountname
        self.passwordexpirationdate = passwordexpirationdate
        threading.Thread.__init__(self)
    def run(self):
        self.returnvalue = False
        try:
            start_date = datetime.strptime(self.passwordexpirationdate, "%Y/%m/%d %H:%M:%S")
            today = datetime.now()
            differencedays = (start_date - today).days
            if differencedays == 14 or differencedays == 7 or differencedays == 3 or differencedays == 2 or differencedays == 0:
                usrenamevalue = adapi().Initialapi("GetobjectProperty",objects=self.samaccountname,objectClass="user")
                if usrenamevalue['isSuccess']:
                    if usrenamevalue['message'][0]['mail'] != None:
                        self.returnvalue = {"name":self.samaccountname,"differencedays":differencedays,"mail":usrenamevalue['message'][0]['mail']}
        except Exception as e:
            self.returnvalue = False
    def senduserpassword_thr(self):
        try:
            return  self.returnvalue
        except Exception:
            return None
