#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import pymysql
from folder_api.Profile import readprofile
from folder_api.encrypt_decode import encrypt_and_decode

def dbinfotest(mysql_host,mysql_port,mysql_user,mysql_password,mysql_database):
    try:
        conn = ""
        #测试
        conn = pymysql.connect(host=mysql_host, port=int(mysql_port), user=mysql_user, password=mysql_password,
                               database=mysql_database,
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
        mysql_host = readprofile('mysql', 'mysql_host')
        mysql_port = readprofile('mysql', 'mysql_port')
        mysql_user = readprofile('mysql', 'mysql_user')
        mysql_password = encrypt_and_decode().decrypted_text(readprofile('mysql', 'mysql_password'))
        mysql_database = readprofile('mysql', 'mysql_database')
        if mysql_host and mysql_port and mysql_user and mysql_password and mysql_database:
            conn = ""
            conn = pymysql.connect(host=mysql_host, port=int(mysql_port), user=mysql_user, password=mysql_password,database=mysql_database,charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            cur = conn.cursor()
            if not cur:
                return False
            else:
                return conn
        else:
            return False
    except:
        return False

#插folder_api_log 日志



def insert_folder_api_log(username,isSuccess, optype,parameter,message):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO folder_api_log (username,isSuccess, optype,parameter,message,times) VALUES (%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (username,isSuccess, optype,parameter,message,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

#插watchdog_log 日志
def insert_watchdog_log(isSuccess, optype,src_path,dest_path,message):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "INSERT INTO watchdog_log (isSuccess, optype,src_path,dest_path,message,times) VALUES (%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (isSuccess, optype,src_path,dest_path,message,createtime))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

#get 获取dfs 设置limit1
def get_management_configuration():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from management_configuration limit1 "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

#get 获取dfs 首选项
def get_folder_first_chiice():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from folder_first_choice"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

#根据level1_id 查找id
def show_filder_level1(level1_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT id FROM folder_level1 WHERE level1_id=%s"
        conncur.execute(connsql,level1_id)
        currlevel1idlist = conncur.fetchall()
        currlevel1id = currlevel1idlist[0]['id']
        conn.commit()
        conn.close()
        return currlevel1id
    except Exception as e:
        return False

#根据level1_name 查找*
def show_filder_level1_id(level1_name):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_level1 WHERE name=%s"
        conncur.execute(connsql,level1_name)
        currlevel1idlist = conncur.fetchall()
        conn.commit()
        conn.close()
        return currlevel1idlist
    except Exception as e:
        return False

#根据level1_path 查找*
def show_folder_level1(level1_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_level1 WHERE level1_path=%s"
        conncur.execute(connsql,level1_path)
        currlevel1idlist = conncur.fetchall()
        conn.commit()
        conn.close()
        return currlevel1idlist
    except Exception as e:
        return False

#根据level1_path 查找*
def show_folder_level1_from_id(level1_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_level1 WHERE level1_id=%s"
        conncur.execute(connsql,level1_id)
        currlevel1idlist = conncur.fetchone()
        conn.commit()
        conn.close()
        return currlevel1idlist
    except Exception as e:
        return False

#根据level2_path 查找*
def show_folder_level2(level2_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_level2 WHERE level2_path=%s"
        conncur.execute(connsql,level2_path)
        currlevel1idlist = conncur.fetchall()
        conn.commit()
        conn.close()
        return currlevel1idlist
    except Exception as e:
        return False

#根据level3_path 查找*
def show_folder_level3(level3_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_level3 WHERE level3_path=%s"
        conncur.execute(connsql,level3_path)
        currlevel1idlist = conncur.fetchall()
        conn.commit()
        conn.close()
        return currlevel1idlist
    except Exception as e:
        return False

#根据level3_id 查找*
def show_manager_dfs_group(level3_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM manager_dfs_group WHERE folder_level3_id=%s"
        conncur.execute(connsql,level3_id)
        currlevel1idlist = conncur.fetchall()
        conn.commit()
        conn.close()
        return currlevel1idlist
    except Exception as e:
        return False

# 查询当前的最大level1_id
def show_max_level1_id():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT max(level1_id) FROM folder_level1 "
        conncur.execute(connsql)
        currlevel2idlist = conncur.fetchall()
        currlevel2id = currlevel2idlist[0]['max(level1_id)']
        conn.commit()
        conn.close()
        return currlevel2id
    except Exception as e:
        return False

#查询当前的最大level2_id
def show_max_level2_id():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT max(level2_id) FROM folder_level2 "
        conncur.execute(connsql)
        currlevel2idlist = conncur.fetchall()
        currlevel2id = currlevel2idlist[0]['max(level2_id)']
        conn.commit()
        conn.close()
        return currlevel2id
    except Exception as e:
        return False

#查询当前的最大level3_id
def show_max_level3_id():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT max(level3_id) FROM folder_level3 "
        conncur.execute(connsql)
        currlevel3idlist = conncur.fetchall()
        currlevel3id = currlevel3idlist[0]['max(level3_id)']
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
    return currlevel3id

#查询当前的最大tree_id
def show_max_tree_id():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT max(tree_id) FROM folder_tree "
        conncur.execute(connsql)
        currtreeidlist = conncur.fetchall()
        currtreeid = currtreeidlist[0]['max(tree_id)']
        conn.commit()
        conn.close()
        return currtreeid
    except Exception as e:
        return False

# 新建一级文件夹插入fold_level1表
def insert_folder_level1(level1id, name,level1_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        level2_sql = "insert into folder_level1(level1_id,name,level1_path) value(%s,%s,%s)"
        level2value = (level1id, name,level1_path)
        conncur.execute(level2_sql, level2value)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#新建二级文件夹插入fold_level2表
def insert_folder_level2(level2id,name,level2_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        level2_sql = "insert into folder_level2(level2_id,name,level2_path) value(%s,%s,%s)"
        level2value = ( level2id, name,level2_path)
        conncur.execute(level2_sql, level2value)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#新建三级文件夹插入fold_level3表
def insert_folder_level3(level3id,name,level3_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        level3_sql = "insert into folder_level3(level3_id,name,level3_path) value(%s,%s,%s)"
        level3value = ( level3id, name,level3_path)
        conncur.execute(level3_sql, level3value)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#新建三级文件夹插入fold_tree表
def insert_folder_tree(level1id,level2id,level3id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        foldertreesql = "insert into folder_tree(tree_id,level1_id,level2_id,level3_id) value(%s,%s,%s,%s)"
        conncur.execute(foldertreesql,(level3id, level1id, level2id, level3id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#插入manage_dfs_group表
def insert_manager_dfs_group(level3id,perm_value,group_name,level3_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        managegroupsql =  "insert into manager_dfs_group(folder_level3_id,perm_value,group_name,level3_path) value(%s,%s,%s,%s)"
        managegroupvalue = ( level3id, perm_value, group_name,level3_path)
        conncur.execute(managegroupsql, managegroupvalue)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level3_id删除相应的tree表项
def deletelevel3treetable(level3_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        deletetreesql = "delete from folder_tree WHERE level3_id= %s"
        conncur.execute(deletetreesql,level3_id)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level3_id删除相应的folder_level3表项
def delete_folder_level3(level3_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        deletefoldersql = "delete from folder_level3 WHERE level3_id= %s"
        conncur.execute(deletefoldersql,level3_id)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level3_id删除相应的manage_dfs_group表项
def deletel_manager_dfs_group(level3_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        deletemanagesql = "delete from manager_dfs_group WHERE folder_level3_id= %s"
        conncur.execute(deletemanagesql,level3_id)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#通过level2_id查询下面的level3_id列表
def show_level3id(level2id):
    conn=dbinfo()
    level3idlist=[]
    try:
        conncur = conn.cursor()
        connsql="SELECT DISTINCT(folder_level3.LEVEL3_id) from folder_tree LEFT JOIN folder_level3 ON folder_level3.level3_id=folder_tree.level3_id where level2_id=%s"
        conncur.execute(connsql,(level2id))
        level3diclist = conncur.fetchall()
        conn.commit()
        conn.close()
        for level3dic in level3diclist:
            level3_id=level3dic['LEVEL3_id']
            level3idlist.append(level3_id)
        return level3idlist
    except Exception as e:
        return False

# 通过level1_id查询下面的level2_id列表
def show_level2id(level1id):
    conn = dbinfo()
    level2idlist = []
    try:
        conncur = conn.cursor()
        connsql = "SELECT DISTINCT(folder_level2.LEVEL2_id) from folder_tree LEFT JOIN folder_level2 ON folder_level2.level2_id=folder_tree.level2_id where level1_id=%s"
        conncur.execute(connsql, (level1id))
        level2diclist = conncur.fetchall()
        conn.commit()
        conn.close()
        for level2dic in level2diclist:
            level2_id = level2dic['LEVEL2_id']
            level2idlist.append(level2_id)
        return level2idlist
    except Exception as e:
        return False

#通过level3_id查询对应的文件夹名
def show_level3name(level3id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT * from folder_level3 WHERE level3_id=%s"
        conncur.execute(connsql,(level3id))
        level3dic = conncur.fetchone()
        conn.commit()
        conn.close()
        return level3dic
    except Exception as e:
        return False


#通过level3_id查询对应的文件夹名
def show_level2name(level2id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT * from folder_level2 WHERE level2_id=%s"
        conncur.execute(connsql,(level2id))
        level3dic = conncur.fetchone()
        conn.commit()
        conn.close()
        return level3dic
    except Exception as e:
        return False


#根据level2_id删除相应的folder_level2表项
def deletelevel2foldertable(level2_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        deletefoldersql = "delete from folder_level2 WHERE level2_id= %s"
        conncur.execute(deletefoldersql,level2_id)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level1_id删除相应的folder_level1表项
def deletelevel1foldertable(level1_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        deletefoldersql = "delete from folder_level1 WHERE level1_id= %s"
        conncur.execute(deletefoldersql,level1_id)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level3_id更新folder_level3的name表项
def updatenamelevel3foldertable(level3_id,newlevel3name,level3_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        renamefoldersql = "update folder_level3 set name=%s,level3_path=%s WHERE level3_id=%s"
        conncur.execute(renamefoldersql, (newlevel3name,level3_path,level3_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level3_id更新manager_dfs-group的groupname表项
def updatenamemanagergrouptable(level3_id,perm_value,newgroupname,level3_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        renamesql = "update manager_dfs_group set group_name=%s,level3_path=%s WHERE folder_level3_id=%s and perm_value=%s"
        conncur.execute(renamesql,(newgroupname,level3_path,level3_id,perm_value))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level2_id更新folder_level2的name表项
def updatenamelevel2foldertable(level2_id,newlevel2name,level2_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        renamefoldersql = "update folder_level2 set name=%s,level2_path=%s WHERE level2_id=%s"
        conncur.execute(renamefoldersql,(newlevel2name,level2_path,level2_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

#根据level1_id更新folder_level1的表项
def updatenamelevel1foldertable(level1_id,newlevel1name,level1_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        renamefoldersql = "update folder_level1 set name=%s,level1_path=%s WHERE level1_id=%s"
        conncur.execute(renamefoldersql,(newlevel1name,level1_path,level1_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


#通过level2_id和name查询是否存在level3
def showlevel3isexist(level3_name,level2_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        level3_sql = "SELECT level3_id from folder_level3 where name = %s and level3_id in (SELECT folder_tree.level3_id from folder_tree WHERE level2_id = %s) "
        conncur.execute(level3_sql,(level3_name,level2_id))
        level3 = conncur.fetchall()
        conn.commit()
        conn.close()
        return level3
    except Exception as e:
        return False

#通过level1_id和name查询是否存在level3
def showlevel2isexist(level2_name,level1_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        level2_sql = "SELECT level2_id from folder_level2 where name = %s and level2_id in (SELECT folder_tree.level2_id from folder_tree WHERE level1_id = %s) "
        conncur.execute(level2_sql,(level2_name,level1_id))
        level2 = conncur.fetchall()
        conn.commit()
        conn.close()
        return level2
    except Exception as e:
        return False

# 查询2层目录所在对应的Lever2ID
def showlevel2_name(level1_id,level2_name):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT folder_level2.level2_id FROM folder_tree,folder_level2 WHERE folder_tree.level2_id = folder_level2.level2_id AND folder_tree.level1_id =%s AND folder_level2.`name`=%s"
        conncur.execute(connsql,(level1_id,level2_name))
        serverlist = conncur.fetchall()
        level2_id = serverlist[0]['level2_id']
        conn.commit()
        conn.close()
        return level2_id
    except Exception as e:
        return False




