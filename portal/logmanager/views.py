from datetime import datetime
from Thr.writelog import writelog_thr


class logmanager():
    def log(self,returnid=0,username=None,ip=None,message=None,issuccess=None,inparameters=None,methodname=None,returnparameters=None,types=None):
        datetimevalue = datetime.now()
        writelog_thr(username,datetimevalue,ip,returnid,message,issuccess,inparameters,methodname,returnparameters,types)

