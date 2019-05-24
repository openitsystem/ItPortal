# -*- coding: utf-8 -*-
import threading
from time import sleep



from adapi.ad_api import *

#继承Thread，需要实现run方法
from adapi.dbinfo import updatepumailuser
from logmanager.views import logmanager


class user_to_exc(threading.Thread):
    """send wechat"""
    def __init__(self,id,count,ou,manger,maildisname,passwd,db,mailpen):
        self.id = id
        self.count = count
        self.ou = ou
        self.manger = manger
        self.maildisname = maildisname
        self.passwd = passwd
        self.db = db
        self.mailpen = mailpen
        threading.Thread.__init__(self)
    def run(self):
        try:
            User = adapi().Initialapi('Createobject', objects=self.count, oudn=self.ou, objectClass='user',
                                      sn=self.manger,displayName=self.maildisname, wWWHomePage='None', password=self.passwd,
                                      guid='None')
            if User['isSuccess']:
                logmanager().log(returnid=1, message="新建公共邮箱，账号创建完成", issuccess=1, inparameters=str(User),
                                 methodname="new_pubmail", types="exchange")
                Changeporty=adapi().Initialapi('SetuserProperty', username=self.count, PropertyName=self.mailpen,PropertyValue=self.manger)
                if Changeporty['isSuccess']:
                    logmanager().log(returnid=1, message="新建公共邮箱，管理员栏位属性修改完成", issuccess=1, inparameters=str(User),
                                     methodname="new_pubmail", types="exchange")
                    sleep(60)
                    Usermail = adapi().Initialapi('UserToExc', username=self.count, dbname=self.db)
                    if  Usermail['isSuccess']:
                        logmanager().log(returnid=1, message="新建公共邮箱，邮件创建完成", issuccess=1, inparameters=str(Usermail),
                                         methodname="new_pubmail", types="exchange")
                        updatepumailuser(self.id,1)

                    else:
                        logmanager().log(returnid=0, message="新建公共邮箱，邮件创建失败", issuccess=0, inparameters=str(Usermail),
                                         methodname="new_pubmail", types="exchange")
                        updatepumailuser(self.id, 2)
                else:
                    logmanager().log(returnid=0, message="新建公共邮箱，管理员栏位属性修改失败", issuccess=0, inparameters=str(User),
                                     methodname="new_pubmail", types="exchange")
                    updatepumailuser(self.id, 2)
            else:
                logmanager().log(returnid=0, message="新建公共邮箱，账号创建失败", issuccess=0, inparameters=str(User),
                                 methodname="new_pubmail", types="exchange")
                updatepumailuser(self.id, 2)
        except Exception as e:
            logmanager().log(returnid=0, message="新建公共邮箱，创建出现异常", issuccess=0, inparameters=str(e),
                             methodname="new_pubmail", types="exchange")
            updatepumailuser(self.id, 2)

def UserCreatMail(id,count,ou,manger,maildisname,passwd,db,mailpen):
    send_Exc = user_to_exc(id,count,ou,manger,maildisname,passwd,db,mailpen)
    send_Exc.start()

