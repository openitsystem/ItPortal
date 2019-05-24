#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 11:36
# @Author  : Center
from Thr.senduserpassword import senduserpassword_agree_class
from adapi.ad_api import *
import datetime

from dfs.dbinfo import get_management_configuration
from sendmail.sendmail import *


def retime(setdate):
    dutydatetime = datetime.datetime.strptime(setdate, '%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.now()
    remindate = (dutydatetime - today).days
    return remindate


def senduserpassword():
    try:

        tab = get_management_configuration()['pwdremindertips']
        if tab == '' or tab == None or tab == "false":
            status = False
        else:
            status = True
            mysqlallvalue = dbinfo_select_global_configuration()[0]
            ad_domain = mysqlallvalue['ad_path']
            if ad_domain != '' and ad_domain != None and ad_domain != "None":
                alluserdatetimevalue  = adapi().postapi('GetUserpasswordexpirationdate', ldaps='(&(objectCategory=person)(objectClass=user))',
                                    path=ad_domain, Properties=["sAMAccountName","passwordexpirationdate"])
                shisidaysvalue = list()
                qidaysvalue = list()
                sandaysvalue = list()
                erdaysvalue = list()
                yidaysvalue = list()
                lingdaysvalue = list()
                if alluserdatetimevalue['isSuccess']:
                    if alluserdatetimevalue['Count'] != 0:
                        rows = list()
                        li = []
                        for i in alluserdatetimevalue['message']:
                            t = senduserpassword_agree_class(i['samaccountname'][0],i['passwordexpirationdate'][0])
                            li.append(t)
                            t.start()
                        for t in li:
                            t.join()
                            thrreturnvalue = t.senduserpassword_thr()
                            if thrreturnvalue:
                                if thrreturnvalue['mail'] != None:
                                    if thrreturnvalue['differencedays'] == 14:
                                        shisidaysvalue.append(thrreturnvalue['mail'])
                                    elif thrreturnvalue['differencedays'] == 7:
                                        qidaysvalue.append(thrreturnvalue['mail'])
                                    elif thrreturnvalue['differencedays'] ==3:
                                        sandaysvalue.append(thrreturnvalue['mail'])
                                    elif thrreturnvalue['differencedays'] ==2:
                                        erdaysvalue.append(thrreturnvalue['mail'])
                                    elif thrreturnvalue['differencedays'] ==1:
                                        yidaysvalue.append(thrreturnvalue['mail'])
                                    # elif thrreturnvalue['differencedays'] ==0:
                                    #     lingdaysvalue.append(thrreturnvalue['mail'])
                        subject = u'密码即将过期提醒'
                        emaillists14 = "你的开机（邮箱）密码还有 14 天过期，请及时更改！"
                        emaillists7 = "你的开机（邮箱）密码还有 7 天过期，请及时更改！"
                        emaillists3 = "你的开机（邮箱）密码还有 3 天过期，请及时更改！"
                        emaillists2 = "你的开机（邮箱）密码还有 2 天过期，请及时更改！"
                        emaillists1 = "你的开机（邮箱）密码还有 1 天过期，请及时更改！"
                        # emaillists0 = "你的开机（邮箱）密码还有 0 天过期，请及时更改！"
                        email_data14 = {'emaillists': emaillists14}
                        email_data7 = {'emaillists': emaillists7}
                        email_data3 = {'emaillists': emaillists3}
                        email_data2 = {'emaillists': emaillists2}
                        email_data1 = {'emaillists': emaillists1}
                        # email_data0 = {'emaillists': emaillists0}
                        template = "mailmould/sendmailpassword.html"
                        to_list14 = shisidaysvalue
                        to_list7 = qidaysvalue
                        to_list3 = sandaysvalue
                        to_list2 = erdaysvalue
                        to_list1 = yidaysvalue
                        to_list0 = lingdaysvalue
                        send_email_by_template(subject, template, email_data14, to_list14)
                        send_email_by_template(subject, template, email_data7, to_list7)
                        send_email_by_template(subject, template, email_data3, to_list3)
                        send_email_by_template(subject, template, email_data2, to_list2)
                        send_email_by_template(subject, template, email_data1, to_list1)
    except Exception as e:
        pass
    return 1

# senduserpassword()


