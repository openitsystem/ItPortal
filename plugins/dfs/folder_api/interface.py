# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 17:56
# @Author  : Santos
import os
import shutil
import time
import win32security
from folder_api.fileright import daclConstants, disable_inheritance, add_ace, rm_ace
from folder_api.dbinfo import *
from folder_api.open_adapi import *

#获取当前目录下的文件夹目录


def getdirlist(rootpath):
    try:
        filelist=os.listdir(rootpath)
        returndirslist=[]
        for num in range(len(filelist)):
            filename=filelist[num]
            if filename != 'DfsrPrivate':
                if os.path.isdir(rootpath+os.sep+filename):
                    returndirslist.append(filename)
                else:
                    pass
        return returndirslist
    except:
        pass

#删除文件报错权限(只有sid 的权限)
def delete_dir_dacl(path):
    try:
        dc = daclConstants()
        objectTypeBit = dc.getObjectTypeBit("DIRECTORY")
        sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()
        counter = 0
        while counter < dacl.GetAceCount():
            try:
                rev, access, usersid = dacl.GetAce(counter)
                user, group, type = win32security.LookupAccountSid('', usersid)
            except Exception as e:
                dacl.DeleteAce(counter)
                counter = counter - 1
            counter = counter + 1
        try:
            win32security.SetNamedSecurityInfo(
                path, objectTypeBit, win32security.DACL_SECURITY_INFORMATION,None, None, dacl, None)
            return True
        except Exception as e:
            return False
    except:
        return False


# 对一，二层文件夹权限进行设置
#1.禁用继承
#2.添加管理账号权限
#3.添加初始权限
#4.移除其他权限
def add_level1_authority(path,Basic_authority,manager):
    '''

    :param path: 文件路径
    :param Basic_authority: 初始权限；（建议 Authenticated Users）
    :param manager: 管理权限账号
    :return:
    '''
    try:
        disable_inheritances = disable_inheritance(path, "DIRECTORY")  # 禁用继承
        add_ace_man = add_ace(path, 'DIRECTORY', manager, 'FULLCONTROL', 'ALLOW', 'FOLDER&SUBFOLDERS&FILES')
        dc = daclConstants()
        objectTypeBit = dc.getObjectTypeBit("DIRECTORY")
        sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()
        counter = 0
        while counter < dacl.GetAceCount():
            try:
                rev, access, usersid = dacl.GetAce(counter)
                user, group, type = win32security.LookupAccountSid('', usersid)
                if not (('administrator' in user) or ("SYSTEM" in user) or (manager in user) or ('Administrator' in user)):
                    dacl.DeleteAce(counter)
                    counter = counter - 1
            except Exception as e:
                dacl.DeleteAce(counter)
                counter = counter - 1
            counter = counter + 1
        try:
            win32security.SetNamedSecurityInfo(
                path, objectTypeBit, win32security.DACL_SECURITY_INFORMATION, None, None, dacl, None)
        except Exception as e:
            print(e)
        add_ace_user = add_ace(path, 'DIRECTORY', Basic_authority, 'READ', 'ALLOW', 'THIS FOLDER ONLY')
        print(add_ace_user)
        return add_ace_user['result']
    except Exception as e:
        print(e)
        return False

# add_level1_authority(r'F:\folders', "Authenticated Users", "file")
#设置3层文件夹权限
#1.禁用继承
#2.添加管理账号权限
#3.移除其他权限（如果是域权限则添加到对应权限组）
#4.添加对应权限组权限
def set_level3_authority(path,manager,authority_read,authority_modify,domain):
    '''

    :param path: 文件路径
    :param manager: 管理账号
    :param authority_read: 此路径 读取和执行 组（账号）
    :param authority_modify:
    :param domain:
    :return:
    '''
    try:
        disable_inheritances = disable_inheritance(path, "DIRECTORY")  # 禁用继承
        add_ace_man = add_ace(path, 'DIRECTORY', manager, 'FULLCONTROL', 'ALLOW', 'FOLDER&SUBFOLDERS&FILES')
        dc = daclConstants()
        objectTypeBit = dc.getObjectTypeBit("DIRECTORY")
        sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()
        counter = 0
        while counter < dacl.GetAceCount():
            try:
                rev, access, usersid = dacl.GetAce(counter)
                user, group, type = win32security.LookupAccountSid('', usersid)
                if not (('administrator' in user) or ("SYSTEM" in user) or (manager in user) or ('Administrator' in user) or (authority_read in user) or (authority_modify in user)):
                    if ObjectExist(user,'user',domain,tokenid=None,ip=None):#这个用户是域user 用户，则，添加修改权限
                        AddUserToGroup(user, authority_modify,domain)
                    elif "Users" in user:
                        pass
                    elif access != 1179785:  # permits=[('查看','1179785','READ&EXECUTE'),('修改','1245631','MODIFY')]
                        GetUserFromGroupss = GetUserFromGroup(user, domain,tokenid=None,ip=None)
                        if GetUserFromGroupss['isSuccess']:
                            for i in GetUserFromGroupss['message']['message']:
                                GetPropertyFordistinguishedNames = GetPropertyFordistinguishedName(i['member'], domain)
                                if GetPropertyFordistinguishedNames['isSuccess']:
                                    sAMAccountName = GetPropertyFordistinguishedNames['message'][0]['sAMAccountName']
                                    AddUserToGroup(sAMAccountName, authority_modify,domain)
                    else:
                        GetUserFromGroupss = GetUserFromGroup(user, domain, tokenid=None, ip=None)
                        if GetUserFromGroupss['isSuccess']:
                            for i in GetUserFromGroupss['message']['message']:
                                GetPropertyFordistinguishedNames = GetPropertyFordistinguishedName(i['member'], domain)
                                if GetPropertyFordistinguishedNames['isSuccess']:
                                    sAMAccountName = GetPropertyFordistinguishedNames['message'][0]['sAMAccountName']
                                    AddUserToGroup(sAMAccountName, authority_read,domain)
                    dacl.DeleteAce(counter)
                    counter = counter - 1
            except Exception as e:
                dacl.DeleteAce(counter)
                counter = counter - 1
            counter = counter + 1
        try:
            win32security.SetNamedSecurityInfo(
                path, objectTypeBit, win32security.DACL_SECURITY_INFORMATION, None, None, dacl, None)
        except Exception as e:
            print(e)
        add_ace_authority_read = add_ace(path, 'DIRECTORY', authority_read, 'READ&EXECUTE', 'ALLOW', 'FOLDER&SUBFOLDERS&FILES')#读取和执行
        add_ace_authority_modify = add_ace(path, 'DIRECTORY', authority_modify, 'MODIFY', 'ALLOW', 'FOLDER&SUBFOLDERS&FILES')#修改
        print(add_ace_authority_modify)
        return add_ace_authority_modify['result']
    except Exception as e:
        print(e)
        return False


#文件权限操作和加数据库类
class dfs_folder:
    def __init__(self):
        get_management_configurations = get_management_configuration()
        self.Basic_authority = get_management_configurations.get('Basic_authority','') # 默认文件夹权限
        self.DFS_distinguishedName = get_management_configurations.get('dfs_group','')  # AD 文件权限组的位置
        self.dfs_manager = get_management_configurations.get('dfs_manager','')  # AD 文件权限组的位置
        self.AD_time = get_management_configurations.get('AD_time', '')  # AD组新建完成后的缓冲时间，（文件夹无法实时获取到新建组）
        # self.get_folder_first_chiices = get_folder_first_chiice() #获取数据库
        # for get_folder_first in get_folder_first_chiices:
        #     folder_path = get_folder_first['folder_path']  # 文件夹路径
        #     folder_level = get_folder_first['folder_level']  # 文件夹层数
    def level1_folder(self,path):
        try:
            show_max_level1_ids_folder0 = show_max_level1_id()
            if show_max_level1_ids_folder0:
                show_max_level1_ids_folder0 = show_max_level1_ids_folder0 + 1
            else:
                show_max_level1_ids_folder0 = 1
            level1_name = path.split('\\')[-1]
            if not show_folder_level1(path):
                insert_folder_level1(show_max_level1_ids_folder0, level1_name,path)
            add_level1_authoritys = add_level1_authority(path,self.Basic_authority, self.dfs_manager)
            return add_level1_authoritys
        except Exception as e:
            print(e)
            return False

    def level2_folder(self,path):
        try:
            show_max_level2_ids = show_max_level2_id()
            if show_max_level2_ids:
                show_max_level2_ids = show_max_level2_ids + 1
            else:
                show_max_level2_ids = 1
            level1_path = ("\\").join(path.split('\\')[:-1])
            level1_name = path.split('\\')[-2]
            level2_name = path.split('\\')[-1]
            show_folder_level1s = show_folder_level1(level1_path)
            if show_folder_level1s:
                level1_id = show_folder_level1s[0].get('level1_id','')
                show_folder_level2s = show_folder_level2(path)
                if not show_folder_level2s:
                    insert_folder_level2(show_max_level2_ids, level2_name,path)
            else:
                show_max_level1_ids_folder0 = show_max_level1_id()
                if show_max_level1_ids_folder0:
                    show_max_level1_ids_folder0 = show_max_level1_ids_folder0 + 1
                else:
                    show_max_level1_ids_folder0 = 1
                insert_folder_level1(show_max_level1_ids_folder0, level1_name,level1_path)
                insert_folder_level2(show_max_level2_ids, level2_name,path)
            add_level2_authoritys = add_level1_authority(path,self.Basic_authority, self.dfs_manager)
            return add_level2_authoritys
        except Exception as e:
            print(e)
            return False
    # 第3层目录创建组和插入数据库
    def creat_level3_group(self,path,level1_id,showlevel2_id,show_max_level3_ids,level1_name,level2_name,level3_name,domain,tokenid):
        try:
            insert_folder_level3(show_max_level3_ids, level3_name,path)
            insert_folder_tree(level1_id, showlevel2_id,show_max_level3_ids)
            for perm_value in ["查看", "修改"]:
                if ObjectExistsOU(level1_name, 'organizationalUnit', self.DFS_distinguishedName, domain,
                                  tokenid):
                    userou_folder0 = "OU=" + level1_name + "," + self.DFS_distinguishedName
                else:
                    CreateOus = Createobject(level1_name, self.DFS_distinguishedName, 'organizationalUnit',
                                             domain,
                                             sn=None, displayName=None, wWWHomePage=None,
                                             password=None, guid=None, tokenid=tokenid)
                    if CreateOus['isSuccess']:
                        userou_folder0 = "OU=" + level1_name + "," + self.DFS_distinguishedName
                    else:
                        userou_folder0 = self.DFS_distinguishedName
                level3_group = level1_name + "-" + level2_name + "-" + level3_name + "-" + perm_value
                Createobject_group = Createobject(level3_group, userou_folder0, 'group', domain,
                                                  sn=None, displayName=None, wWWHomePage=None,
                                                  password=None, guid=None, tokenid=tokenid, ip=None)
                insert_manager_dfs_group(show_max_level3_ids, perm_value, level3_group, path)
                print(Createobject_group)
            if Createobject_group['isSuccess']:
                time.sleep(self.AD_time)
            return True
        except Exception as e:
            print(e)
            return False

    def level3_folder(self, path,domain,tokenid):
        try:
            show_max_level1_ids = show_max_level1_id()
            if show_max_level1_ids:
                show_max_level1_ids = show_max_level1_ids + 1
            else:
                show_max_level1_ids = 1
            show_max_level2_ids = show_max_level2_id()
            if show_max_level2_ids:
                show_max_level2_ids = show_max_level2_ids + 1
            else:
                show_max_level2_ids = 1
            show_max_level3_ids = show_max_level3_id()
            if not show_max_level3_ids:
                show_max_level3_ids = 1
            else:
                show_max_level3_ids = show_max_level3_ids + 1
            level1_name = path.split('\\')[-3]
            level2_name = path.split('\\')[-2]
            level3_name = path.split('\\')[-1]
            level1_path = ("\\").join(path.split('\\')[:-2])
            level2_path = ("\\").join(path.split('\\')[:-1])
            authority_read = level1_name + "-" + level2_name + "-" + level3_name + "-查看"
            authority_modify = level1_name + "-" + level2_name + "-" + level3_name + "-修改"
            show_folder_level1s = show_folder_level1(level1_path)#level1name 获取 level1 id
            if show_folder_level1s:
                level1_id = show_folder_level1s[0].get('level1_id', '')#1层目录所在对应的Lever1ID
                show_folder_level2s = show_folder_level2(level2_path) #查询2层目录所在对应的Lever2ID
                if show_folder_level2s:
                    level2_id = show_folder_level2s[0].get('level2_id', '')  # 2层目录所在对应的Lever1ID
                    show_folder_level3s = show_folder_level3(path) #查询3层目录所在对应的Lever3ID
                    if not show_folder_level3s:
                        self.creat_level3_group(path, level1_id, level2_id, show_max_level3_ids, level1_name,
                                                level2_name, level3_name, domain, tokenid)
                else:
                    insert_folder_level2(show_max_level2_ids, level2_name,level2_path)
                    self.creat_level3_group(path, level1_id, show_max_level2_ids, show_max_level3_ids, level1_name,
                                            level2_name, level3_name, domain, tokenid)
            else:
                insert_folder_level1(show_max_level1_ids, level1_name,level1_path)
                insert_folder_level2(show_max_level2_ids, level2_name,level2_path)
                self.creat_level3_group(path,show_max_level1_ids, show_max_level2_ids, show_max_level3_ids, level1_name,
                                        level2_name, level3_name, domain, tokenid)
            set_level3_authoritys = set_level3_authority(path, self.dfs_manager, authority_read, authority_modify,
                                                         domain)  # 添加3目录权限
            return set_level3_authoritys
        except Exception as e:
            print(e)
            return False

    def delete_level3(self,level3_id,domain,tokenid):
        try:
            show_manager_dfs_groups = show_manager_dfs_group(level3_id)
            if show_manager_dfs_groups:
                for groups in show_manager_dfs_groups:
                    group_name = groups['group_name']
                    DeleteAdgroupByOUs = DeleteAdgroupByOU(group_name, self.DFS_distinguishedName, domain, tokenid, ip=None)
                deletetree_result = deletelevel3treetable(level3_id)
                deletefolderlevel3_result = delete_folder_level3(level3_id)
                deletemanagegroup_result = deletel_manager_dfs_group(level3_id)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_level2(self,level2_id,domain,tokenid):
        try:
            level3idlist = show_level3id(level2_id)
            if level3idlist:
                for level3_id in level3idlist:
                    self.delete_level3(level3_id,domain,tokenid)
            deletelevel2folder_result = deletelevel2foldertable(level2_id)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_level1(self,level1_id,domain,tokenid):
        try:
            level2idlist = show_level2id(level1_id)
            if level2idlist:
                for level2_id in level2idlist:
                    self.delete_level2(level2_id,domain,tokenid)
            deletelevel1folder_result = deletelevel1foldertable(level1_id)
            return True
        except Exception as e:
            print(e)
            return False

    def rename_level3(self,level3_id,new_level3_path,domain,tokenid):
        try:
            level1_name = new_level3_path.split('\\')[-3]
            level2_name = new_level3_path.split('\\')[-2]
            level3_name = new_level3_path.split('\\')[-1]
            authority_read = level1_name + "-" + level2_name + "-" + level3_name + "-查看"
            authority_modify = level1_name + "-" + level2_name + "-" + level3_name + "-修改"
            show_manager_dfs_groups = show_manager_dfs_group(level3_id)
            if show_manager_dfs_groups:
                #更新AD组和 manager_dfs_group数据库
                for groups in show_manager_dfs_groups:
                    group_name = groups['group_name']
                    if groups['perm_value'] == "查看":
                        Renameobject(group_name, authority_read, 'group', domain, tokenid, ip=None)
                        managegroup_result_read = updatenamemanagergrouptable(level3_id, "查看", authority_read,
                                                                         new_level3_path)  # 更新manager_dfs_group
                    else:
                        Renameobject(group_name, authority_modify, 'group', domain, tokenid, ip=None)
                        managegroup_result_modify = updatenamemanagergrouptable(level3_id,"修改",authority_modify,new_level3_path) # 更新manager_dfs_group
                updatelevel3_result = updatenamelevel3foldertable(level3_id,level3_name,new_level3_path)  # 更新folder_level3
                print(updatelevel3_result)
            return True
        except Exception as e:
            print(e)
            return False

    def rename_level2(self,level2_id,new_level2_path,domain,tokenid):
        try:
            level2_name = new_level2_path.split('\\')[-1]
            update_level2 = updatenamelevel2foldertable(level2_id,level2_name,new_level2_path)
            level3idlist = show_level3id(level2_id)
            for level3_id in level3idlist:
                show_level3names = show_level3name(level3_id)
                if show_level3names:
                    new_level3_path = new_level2_path+"\\"+show_level3names['name']
                    self.rename_level3(level3_id,new_level3_path,domain,tokenid)
            return True
        except Exception as e:
            print(e)
            return False

    def rename_level1(self,level1_id,new_level1_path,domain,tokenid):
        try:
            level1_name = new_level1_path.split('\\')[-1]
            show_folder_level1_from_ids = show_folder_level1_from_id(level1_id)#获取修改前的文件名称
            old_name = show_folder_level1_from_ids.get("name",'')
            if old_name:
                old_OUdistinguishedName = "OU="+old_name+","+self.DFS_distinguishedName
                Renameobjects =Renameobject(old_OUdistinguishedName, level1_name, 'organizationalUnit', domain, tokenid, ip=None)#AD重命名第1层文件目录
            update_level1 = updatenamelevel1foldertable(level1_id,level1_name,new_level1_path)
            level2idlist = show_level2id(level1_id)
            for level2_id in level2idlist:
                show_level2names = show_level2name(level2_id)
                if show_level2names:
                    new_level2_path = new_level1_path + "\\" + show_level2names['name']
                    self.rename_level2(level2_id, new_level2_path, domain, tokenid)
            return True
        except Exception as e:
            print(e)
            return False


def first_folder_authority(domain,tokenid):
    try:
        get_folder_first_chiices = get_folder_first_chiice()
        if get_folder_first_chiices :
            for get_folder_first in get_folder_first_chiices:
                folder_path = get_folder_first['folder_path']  # 文件夹路径
                folder_level = get_folder_first['folder_level']  # 文件夹层数

                if folder_level == 0:
                    getdirlists = getdirlist(folder_path)
                    for i in getdirlists:
                        level1_path = folder_path + os.sep + i
                        getdirlist_2 = getdirlist(level1_path)
                        for level2_name in getdirlist_2:
                            level2_path = folder_path + os.sep + i + os.sep + level2_name
                            getdirlist_3 = getdirlist(level2_path)
                            for level3_name in getdirlist_3:
                                level3_path = folder_path + os.sep + i + os.sep + level2_name+ os.sep + level3_name
                                dfs_folder().level3_folder(level3_path, domain, tokenid)
                            dfs_folder().level2_folder(level2_path)  # 添加二层目录文件夹权限
                        dfs_folder().level1_folder(level1_path)  # 添加一层目录文件夹权限
                elif folder_level == 1:
                    level1_name_f1 = folder_path.split('\\')[-1]
                    level1_path_f1 = folder_path
                    getdirlist_2_f1 = getdirlist(level1_path_f1)
                    for level2_name_f1 in getdirlist_2_f1:
                        level2_path_f1 = level1_path_f1 + os.sep + level2_name_f1
                        getdirlist_3_f1 = getdirlist(level2_path_f1)
                        for level3_name_f1 in getdirlist_3_f1:
                            level3_path_f1 = level2_path_f1+ os.sep + level3_name_f1
                            dfs_folder().level3_folder(level3_path_f1, domain, tokenid)
                        dfs_folder().level2_folder(level2_path_f1)  # 添加二层目录文件夹权限
                    dfs_folder().level1_folder(level1_path_f1)  # 添加一层目录文件夹权限
        return True
    except Exception as e:
        print(e)
        return False



# 新建文件夹
def creat_folder(src_path):
    try:
        os.mkdir(src_path)
        result =  {'isSuccess':True,"message":str(src_path)+";文件夹新建成功"}
    except Exception as e:
        e = str(repr(e))
        if '当文件已存在时，无法创建该文件。' in e:
            result = {'isSuccess': True, "message": str(src_path) + ";文件夹已存在"}
        else:
            result = {'isSuccess': False, "message": str(src_path) + ";文件夹新建出现错误："+e}
    return result

#删除文件夹
def delete_folder(src_path):
    try:
        shutil.rmtree(src_path)  # 删除名文件夹
        result =  {'isSuccess':True,"message":str(src_path)+";文件夹删除成功"}
    except Exception as e:
        e = str(repr(e))
        if "FileNotFoundError(2, '系统找不到指定的路径。')" in e:
            result = {'isSuccess': True, "message": str(src_path) + ";文件夹不存在"}
        else:
            result = {'isSuccess': False, "message": str(src_path) + ";文件夹删除错误："+e}
    return result
#重命名文件夹

def rename_folder(src_path,dest_path):
    try:
        os.rename(src_path, dest_path)  # 重命名文件夹
        result =  {'isSuccess':True,"message":str(src_path)+";重命名为;"+str(dest_path)}
    except Exception as e:
        e = str(repr(e))
        if "系统找不到指定的文件" in e:
            result = {'isSuccess': True, "message": str(src_path) + ";重命名找不到文件更新数据库"}
        else:
            result = {'isSuccess': False, "message": str(src_path) + ";文件夹重命名错误："+e}
    return result


#获取当前文件夹权限，附加到另外的文件夹
