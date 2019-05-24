# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 10:52
# @Author  :
from datetime import datetime
from dbinfo_ad.newdbtest import dbinfo

#获取api 设置
def get_api(title):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from api where title=%s "
        conncur.execute(connsql, (title))
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

# 插入到表api
def insert_api(mess,title):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from api where title=%s "
        conncur.execute(connsql, (title))
        histroycounts = conncur.fetchone()
        if histroycounts:
            connsql = "update api SET mess=%s where title=%s"
            conncur.execute(connsql, (mess, title))
            conn.commit()
        else:
            connsql = "insert INTO api (mess, title) VALUE (%s,%s) "
            conncur.execute(connsql,(mess, title))
            conn.commit()
        conn.close()
        return True
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

#get
def getconfiguration():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from management_configuration limit1 "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

#get 获取dfs 设置limit1 get_management_configuration_copy
def get_management_configuration_copy():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from management_configuration_copy limit1 "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

def del_management_configuration_dfs():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "update management_configuration SET dfs_group=NULL,Basic_authority=NULL,dfs_manager=NULL,AD_time=0,dfs_relation_name=NULL,dfs_relation=NULL,dfs_relation_mail=NULL"
        conncur.execute(connsql, ())
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_management_configuration_dfs_switch(vaule):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "update management_configuration SET dfs_switch=%s"
        conncur.execute(connsql, (vaule))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_management_configuration_changepwdremindertips(vaule):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "update management_configuration SET pwdremindertips=%s"
        conncur.execute(connsql, (vaule))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def update_management_configuration_dfs(dfs_group,Basic_authority,dfs_manager,AD_time,dfs_relation_name,dfs_relation,dfs_relation_mail):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "update management_configuration SET dfs_group=%s,Basic_authority=%s,dfs_manager=%s,dfs_relation_name=%s,dfs_relation=%s,dfs_relation_mail=%s"
        conncur.execute(connsql, (dfs_group,Basic_authority,dfs_manager,dfs_relation_name,dfs_relation,dfs_relation_mail))
        connsql = "update management_configuration SET AD_time=%d" % AD_time
        conncur.execute(connsql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def insert_management_configuration_dfs(dfs_group,Basic_authority,dfs_manager,AD_time,dfs_relation_name,dfs_relation,dfs_relation_mail,domain):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "insert INTO management_configuration(dfs_group,Basic_authority,dfs_manager,dfs_relation_name,dfs_relation,dfs_relation_mail,domain) VALUE (%s,%s,%s,%s,%s,%s,%s)"
        conncur.execute(connsql, (dfs_group,Basic_authority,dfs_manager,dfs_relation_name,dfs_relation,dfs_relation_mail,domain))
        connsql = "update management_configuration SET AD_time=%d" % AD_time
        conncur.execute(connsql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_management_configuration_dfs_api(dfs_api):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "update management_configuration SET dfs_api=%s"
        conncur.execute(connsql,(dfs_api))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def insert_management_configuration_dfs_api(dfs_api,domain):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "insert INTO management_configuration(dfs_api,domain) VALUE (%s,%s)"
        conncur.execute(connsql, (dfs_api,domain))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_folder_first_choice():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from folder_first_choice "
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

def del_folder_first_choice_id(id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "delete from folder_first_choice WHERE id=%s"
        conncur.execute(connsql, (id))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False

# 插入到表folder_first_choice 并返回插入的数据
def add_folder_first_choice(folder_level, folder_path, server_manager):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "insert INTO folder_first_choice (folder_level, folder_path, server_manager) VALUE (%s,%s,%s) "
        conncur.execute(connsql,
                        (folder_level, folder_path, server_manager))
        conn.commit()
        connsql = "select * from folder_first_choice WHERE folder_path=%s"
        conncur.execute(connsql, (folder_path))
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#get 获取folder_level2
def getlevel2():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from folder_level2"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        return False



def showlevel1():
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT * from folder_level1 ORDER BY NAME "
        conncur.execute(connsql)
        level1 = conncur.fetchall()
        conn.commit()
        conn.close()
        return level1
    except Exception as e:
        print (e)
        return False

def show_folder_level1_to_id(level1_id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * from folder_level1 WHERE level1_id=%s"
        conncur.execute(connsql,(level1_id))
        level1 = conncur.fetchall()
        conn.commit()
        conn.close()
        return level1
    except Exception as e:
        print(e)
        return False

#通过level2_id查询对应的文件夹名
def show_level2name(level2_id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT * from folder_level2 WHERE level2_id=%s"
        conncur.execute(connsql,(level2_id))
        level3dic = conncur.fetchone()
        conn.commit()
        conn.close()
        return level3dic
    except Exception as e:
        return False

def showlevel2(level1id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT DISTINCT(folder_level2.LEVEL2_id),name from folder_tree LEFT JOIN folder_level2 ON folder_level2.level2_id=folder_tree.level2_id where level1_id=%s"
        conncur.execute(connsql,(level1id))
        level2 = conncur.fetchall()
        conn.commit()
        conn.close()
        return level2
    except Exception as e:
        print (e)
        return False


def showlevel3(level2id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT DISTINCT(folder_level3.LEVEL3_id),name,(folder_level3.level3_path) from folder_tree LEFT JOIN folder_level3 ON folder_level3.level3_id=folder_tree.level3_id where level2_id=%s"
        conncur.execute(connsql, (level2id))
        level3 = conncur.fetchall()
        conn.commit()
        conn.close()
        return level3
    except Exception as e:
        print (e)
        return False

def showlevel1level2level3id(level1_id,level2_id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT level3_id
                  FROM folder_tree
                  where level1_id=%s AND level2_id=%s"""
        conncur.execute(connsql,(level1_id,level2_id))
        level3_idlist= conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return level3_idlist


#通过level3_id查询对应的文件夹名
def showlevel3name(level3id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT name from folder_level3 WHERE level3_id=%s"
        conncur.execute(connsql,(level3id))
        level3dic = conncur.fetchone()
        conn.commit()
        conn.close()
        level3name=level3dic['name']
    except Exception as e:
        print (e)
    return level3name

def showlevel3names(level3_ids):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        # connsql=""SELECT name from folder_level3 where level3_id in (%s)"" % (level3_idlist)
        connsql ="SELECT name from folder_level3 where level3_id in %(ids)s"
        conncur.execute(connsql,{"ids":level3_ids})
        level3_namelist = conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return level3_namelist

def showtreeid(level1id,level2id,level3id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT tree_id from folder_tree where level1_id=%s and level2_id=%s and level3_id=%s"
        conncur.execute(connsql, (level1id,level2id,level3id))
        treeid = conncur.fetchone()
        conn.commit()
        conn.close()
        return treeid
    except Exception as e:
        print (e)
        return False

#查询组名
def showgroupname(level3id,pervalue):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT group_name from manager_dfs_group where folder_level3_id=%s and perm_value=%s "
        conncur.execute(connsql, (level3id,pervalue))
        groupname = conncur.fetchone()
        conn.commit()
        conn.close()
        return groupname
    except Exception as e:
        print (e)
        return False


#申请信息插入到表folder_dfs_flow(没有主管和文件夹的代理人)
def add_dfs_flow(username, displayName, treeids, group_name, now, director_name, director_account, level2_manager_name,level2_manager, flow_status,authority_applicant):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="insert INTO folder_dfs_flow (username, displayName, tree_id, group_name, submit_time, director_name, director_adaccount, relation_name,relation_adaccount, flow_status,authority_applicant) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        conncur.execute(connsql, (username, displayName, treeids, group_name, now, director_name, director_account, level2_manager_name,level2_manager, flow_status,authority_applicant))
        conn.commit()
        connsql = "SELECT * from folder_dfs_flow where username=%s and tree_id=%s and submit_time = %s"
        conncur.execute(connsql, (username, treeids,now))
        groupname = conncur.fetchone()
        conn.commit()
        conn.close()
        return groupname
    except Exception as e:
        print (e)
        return 0


#通过主管AD账户查找flow 用于邮件
def showmyemailflowdir(username):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT folder_dfs_flow.username,folder_dfs_flow.displayName,folder_dfs_flow.group_name,folder_dfs_flow.submit_time
                  FROM folder_dfs_flow
                  LEFT JOIN folder_tree ON folder_tree.tree_id=folder_dfs_flow.tree_id
                  LEFT JOIN folder_level1 ON folder_tree.level1_id=folder_level1.level1_id
                  LEFT JOIN folder_level2 on folder_tree.level2_id=folder_level2.level2_id
                 LEFT JOIN folder_level3 ON folder_tree.level3_id=folder_level3.level3_id  where director_adaccount=%s AND folder_dfs_flow.flow_status=0"""
        conncur.execute(connsql, (username))
        flowlists= conncur.fetchall()
        conn.commit()
        conn.close()
        return flowlists
    except Exception as e:
        print (e)
        return False


## 检查flow表是否有相同数据
def checkflow(username,groupname):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT count(folder_dfs_flow.id) as counts from folder_dfs_flow where username=%s and group_name=%s AND flow_status<'3'"
        conncur.execute(connsql, (username,groupname))
        flowidcounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return flowidcounts
    except Exception as e:
        print (e)
        return 0

#根据申请人分页显示申请过的记录
def showmyflowbypage(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = """SELECT *
                     FROM folder_dfs_flow
                     where (username=%s or authority_applicant=%s) ORDER by folder_dfs_flow.submit_time DESC"""
        conncur.execute(connsql,(username,username))
        flowlists = conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
    return flowlists


#显示主管需要的审批内容
def showmyapproval(username):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT * FROM folder_dfs_flow WHERE director_adaccount=%s AND flow_status=0"""
        conncur.execute(connsql, (username))
        approvelists= conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return approvelists

#显示主管需要的审批数量
def showmyapproval_count(username):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT count(*) FROM folder_dfs_flow WHERE director_adaccount=%s AND flow_status=0"""
        conncur.execute(connsql, (username))
        approvelists= conncur.fetchone()
        conn.commit()
        conn.close()
        return approvelists.get("count(*)",0)
    except Exception as e:
        print (e)
        return 0

#通过id来检查主管跟文件夹联系人是否是同一个人
def checkdiretorissamerelation(id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT * FROM folder_dfs_flow where id=%s"
        conncur.execute(connsql,(id))
        accounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return accounts
    except Exception as e:
        print (e)
        return False

#主管审批方法
def directorapproval(directorstatus,directortime,flowstatus,id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="update folder_dfs_flow SET director_status=%s,director_time=%s,flow_status=%s where id=%s"
        conncur.execute(connsql, (directorstatus,directortime,flowstatus,id))
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        print (e)
#文件管理员审批方法
def relationapprovaldb(relationstatus,relationtime,flowstatus,id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="update folder_dfs_flow SET relation_status=%s,relation_time=%s,flow_status=%s where id=%s"
        conncur.execute(connsql,(relationstatus,relationtime,flowstatus,id))
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        print (e)

#执行成功后，执行成功
def operate(endtime,flowstatus,id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="update folder_dfs_flow SET flow_status=%s,end_time=%s where id=%s"
        conncur.execute(connsql,(flowstatus,endtime,id))
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        print (e)

#显示文件夹关联人邮件审批 通过Ids
def showrelationemail(ids,flow_status):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT *
                  FROM folder_dfs_flow
                  where  id=%s and flow_status=%s"""
        conncur.execute(connsql, (ids,flow_status))
        approvelists= conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return approvelists


#通过id来检查申请人跟文件夹联系人是否是同一个人1
def checkusernameissamerelation(id,flow_status):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="SELECT * FROM folder_dfs_flow where id in %(id)s and flow_status = %(flow_status)s"
        conncur.execute(connsql,{"id":id,"flow_status":flow_status})
        username = conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return username


#通过文件夹关联人显示文件夹关联人邮件审批
def showrelationadaccountemail(relation_adaccount):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT * FROM folder_dfs_flow
                  where  relation_adaccount=%s and flow_status=1"""
        conncur.execute(connsql,(relation_adaccount))
        approvelists= conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return approvelists

#通过ID username 显示已开通
def showidemail(id,username):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT * FROM folder_dfs_flow
                  where  id  in %(id)s and flow_status=3 AND username = %(username)s """
        conncur.execute(connsql,{"id": id,"username": username})
        approvelists= conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return approvelists

#显示文件夹关联人审批单
def showrelationapproval(username):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT * FROM folder_dfs_flow
                  where relation_adaccount=%s AND flow_status=1 AND director_status=1"""
        conncur.execute(connsql, (username))
        relationapprovelists= conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return relationapprovelists

#显示文件夹关联人审批单
def showrelationapproval_count(username):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="""SELECT count(*) FROM folder_dfs_flow
                  where relation_adaccount=%s AND flow_status=1 AND director_status=1"""
        conncur.execute(connsql, (username))
        relationapprovelists= conncur.fetchone()
        conn.commit()
        conn.close()
        return relationapprovelists.get("count(*)",0)
    except Exception as e:
        print (e)
        return 0

#显示username下的文件夹有哪些二级目录 #文件夹管理
def showlevel2byusername(username):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_level2 WHERE level2_manager=%s"
        conncur.execute(connsql,(username))
        level2namelists = conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return level2namelists

#通过level3id查询组名
def showgroupnamebyrelation(folder_level3_id,perm_value):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM manager_dfs_group WHERE folder_level3_id=%s and perm_value=%s"
        conncur.execute(connsql,(folder_level3_id,perm_value))
        groupnames = conncur.fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print (e)
    return groupnames

#通过用户名跟组名以及flowstatus=3已成功开通的状态查询到flowid
def getflowbygroupandusername(username,groupname):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_dfs_flow WHERE username=%s and group_name=%s and flow_status=3"
        conncur.execute(connsql,(username,groupname))
        dictflowids = conncur.fetchall()
        conn.commit()
        conn.close()
        return dictflowids
    except Exception as e:
        print (e)
        return False

#修改文件夹管理员
def set_folder_level2_manage(level2_manager,level2_manager_name,level2_manager_mail,level2_id):
    conn=dbinfo()
    try:
        conncur = conn.cursor()
        connsql="update folder_level2 SET level2_manager=%s,level2_manager_name=%s,level2_manager_mail=%s where level2_id=%s"
        conncur.execute(connsql, (level2_manager,level2_manager_name,level2_manager_mail,level2_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print (e)
        return False

# 修改文件夹管理员
def set_folder_level2_manage_from_path(level2_manager, level2_manager_name, level2_manager_mail, level2_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "update folder_level2 SET level2_manager=%s,level2_manager_name=%s,level2_manager_mail=%s where level2_path=%s"
        conncur.execute(connsql, (level2_manager, level2_manager_name, level2_manager_mail, level2_path))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

# 通过level3_path 查找对应的权限组
def get_manager_dfs_group_from(level3_path):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM manager_dfs_group WHERE level3_path=%s"
        conncur.execute(connsql, (level3_path))
        dictflowids = conncur.fetchall()
        conn.commit()
        conn.close()
        return dictflowids
    except Exception as e:
        print(e)
        return False

# 查找 folder_dfs_flow
def sel_folder_dfs_flow():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_dfs_flow ORDER by folder_dfs_flow.submit_time DESC"
        conncur.execute(connsql, ())
        dictflowids = conncur.fetchall()
        conn.commit()
        conn.close()
        return dictflowids
    except Exception as e:
        print(e)
        return False

# 查找 folder_dfs_flow id
def sel_folder_dfs_flow_id(id):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_dfs_flow where id = %s"
        conncur.execute(connsql, (id))
        dictflowids = conncur.fetchone()
        conn.commit()
        conn.close()
        return dictflowids
    except Exception as e:
        print(e)
        return False

# 查找 folder_api_log
def sel_folder_api_log():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "SELECT * FROM folder_api_log ORDER by folder_api_log.times DESC"
        conncur.execute(connsql, ())
        dictflowids = conncur.fetchall()
        conn.commit()
        conn.close()
        return dictflowids
    except Exception as e:
        print(e)
        return False
