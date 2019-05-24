import pymysql
from datetime import datetime
from dbinfo_ad.newdbtest import dbinfo


def dbinfo_insert_iisvalue(ip,port):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET iis_ip = %s , iis_port = %s  WHERE id = 1"
        conncur.execute(connsql, (ip,port))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def dbinfo_insert_itgroupvalue(groupname):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET it_group = %s  WHERE id = 1"
        conncur.execute(connsql, (groupname))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def dbinfo_insert_advalue(ip,account,password,domain,path):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET ad_ip = %s , ad_account = %s , ad_password = %s, ad_domain = %s, ad_path = %s WHERE id = 1"
        conncur.execute(connsql, (ip,account,password,domain,path))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def dbinfo_insert_skeyvalue(skey):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET skey = %s  WHERE id = 1"
        conncur.execute(connsql, (skey))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def dbinfo_insert_exvalue(ip,account,password,domain):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET ex_ip = %s , ex_account = %s , ex_password = %s, ex_domain = %s WHERE id = 1"
        conncur.execute(connsql, (ip,account,password,domain))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def dbinfo_insert_adminvalue(adminpwd):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET adminpwd = %s WHERE id = 1"
        conncur.execute(connsql, (adminpwd))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def dbinfo_insert_adipsvalue(adminpwd):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "UPDATE global_configuration SET ad_ips = %s WHERE id = 1"
        conncur.execute(connsql, (adminpwd))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def dbinfo_insert_log(username,datetimevalue,ip,resultvalue,message,issuccess,inparameters,methodname,returnparameters,types):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT  INTO systemlog (username,datetimevalue,ip,resultvalue,message,issuccess,inparameters,methodname,returnparameters,types) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        conncur.execute(connsql, (username,datetimevalue,ip,resultvalue,message,issuccess,inparameters,methodname,returnparameters,types))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def dbinfo_select_global_configuration():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from global_configuration "
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False
