# -*- coding: utf-8 -*-
import threading

#继承Thread，需要实现run方法
from urllib import request, parse
from adapi.dbinfo import getmangerapi



class flow_agree_class(threading.Thread):
    def __init__(self,jzphone, message):
        self.jzphone = jzphone
        self.message = message
        threading.Thread.__init__(self)
    def run(self):
        try:
            url = getmangerapi('Sendmessage')['mess']
            value = {
                "mobile": self.jzphone,
                "message": self.message,
            }
            querystring = parse.urlencode(value)
            u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
            return u
        except Exception as e:
            return e


def Send_message_thr(jzphone, message):
    send_Exc = flow_agree_class(jzphone, message)
    send_Exc.start()