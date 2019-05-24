import pymysql,os
import configparser
from admin_account.encrypt_decode import encrypt_and_decode
from admin_account.Profile import readprofile

def dbinfotest(ip,username,password,port):
    try:
        conn = ""
        #测试
        conn = pymysql.connect(host=ip, port=int(port), user=username, password=password,
                               database='itdev-portal',
                               charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        if not cur:
            return False
        else:
            return True
    except Exception as e:
        return False

def dbinfo():
    try:
        # dir_now = os.path.dirname(os.path.dirname(os.path.abspath("settings.py")))
        mysqlipvalue = readprofile('mysql', 'ip')
        mysqlusernamevalue = readprofile('mysql', 'username')
        mysqlPortevalue = readprofile('mysql', 'Port')
        mysqlPasswordvalue = encrypt_and_decode().decrypted_text(readprofile('mysql', 'Password'))
        conn = ""
        #测试
        conn = pymysql.connect(host=mysqlipvalue, port=int(mysqlPortevalue), user=mysqlusernamevalue, password=mysqlPasswordvalue,
                               database='itdev-portal',
                               charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        if not cur:
            return False
        else:
            return conn
    except Exception as e:
        return False

