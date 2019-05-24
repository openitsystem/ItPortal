# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 15:00
# @Author  :
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
# Create your views here.
from adapi.ad_api import *
from admin_account.Profile import readprofile
from dfs.dbinfo import *
from dfs.folder import dfs_api
from dfs.thr_apply import thr_apply_update
from dfs.thr_folder import thr_creat_folder_level3, set_file_FirstFolderAuthority
from dfs.thr_re_sucapproval import thr_all_re_sucapproval
from dfs.thr_sucapproval import thr_allsucapproval
from sendmail.sendmail import send_html_email
from tools.views import MyThread
from logmanager.views import logmanager
import ast
from django.utils.html import escape

def dfsapply(request):
    try:
        username = request.session.get('username')
        displayname = request.session.get('displayname')
        if username:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            level1list = showlevel1()
            return render_to_response('dfsweb/dfsapply.html', locals())
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        logmanager().log(returnid=0, username=username, ip=ip, message="dfsapply,文件夹权限申请页面无法打开："+str(e), issuccess=0, methodname="dfsapply",returnparameters = str(request.POST), types="dfs")
        return HttpResponseRedirect('/', request)


#通过第一级目录的id显示第二级目录的信息
def level2info(request):
    level1idinfo=escape(request.POST.get('level1idinfo'))
    username=request.session.get('username')
    if username:
        try:
            level2lists=showlevel2(level1idinfo)
            dict_level2=[]
            for level2list in level2lists:
                temp=[]
                temp.append(level2list['LEVEL2_id'])
                temp.append(level2list['name'])
                dict_level2.append(temp)
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps({"dict_level2":dict_level2}))
    else:
        return HttpResponseRedirect('/', request)

#通过第二级目录的id显示第三级目录的信息
def level3info(request):
    level2idinfo=escape(request.POST.get('level2idinfo'))
    username=request.session.get('username')
    if username:
        try:
            level3lists=showlevel3(level2idinfo)
            dict_level3=[]
            for level3list in level3lists:
                temp=[]
                temp.append(level3list['LEVEL3_id'])
                temp.append(level3list['name'])
                temp.append(level3list['level3_path'])
                dict_level3.append(temp)
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps({"dict_level3":dict_level3}))
    else:
        return HttpResponseRedirect('/', request)

#显示文件夹关联人信息
def showlevel2relation(request):
    level2_id=escape(request.POST.get('level2_id'))
    username=request.session.get('username')
    if username:
        try:
            relations=show_level2name(level2_id)
            dict_relation=[]
            temp=[]
            level2_manager_name = relations.get('level2_manager_name','')
            if not level2_manager_name:
                level2_manager_name = get_management_configuration().get('dfs_relation_name','')
            temp.append(level2_manager_name)
            dict_relation.append(temp)
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps({"dict_relation":dict_relation}))
    else:
        return HttpResponseRedirect('/', request)


#根据level1level2level3 ID 生成 level3ID list 和 level3text list
def showlevel1level2level3(request):
    username = request.session.get('username')
    level1_id = escape(request.POST.get('level1_id'))
    level2_id = escape(request.POST.get('level2_id'))
    level3_id = escape(request.POST.get('level3_id')).split(',')
    try:
        if username:
            if '-1' in level3_id: #全选
                level3_idlist = showlevel1level2level3id(level1_id,level2_id)
                level3_idlists = list()
                level3_namelist = list()

                for i in range(len(level3_idlist)):
                    level3_idlists.append(str(level3_idlist[i]['level3_id']))
                if len(level3_idlists)==1:
                    level3_namelist.append(showlevel3name(level3_idlists[0]))
                else:
                    level3_namelists = showlevel3names(tuple(level3_idlists))
                    for i in range(len(level3_namelists)):
                        level3_namelist.append(level3_namelists[i]['name'])
            elif len(level3_id)==1:#单选
                level3_idlists = level3_id
                level3_namelist = list()
                level3_namelist.append(showlevel3name(level3_idlists[0]))
            else:
                # 或选择几个
                level3_idlists = level3_id
                level3_namelists = showlevel3names(tuple(level3_idlists))
                level3_namelist = list()
                for i in range(len(level3_namelists)):
                    level3_namelist.append(level3_namelists[i]['name'])
            result = {'level3_idlists': level3_idlists,'level3_namelist':level3_namelist}
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        print(e)


#把申请插入到flow表并发邮件告知主管
def addapplytoflow(request):
    adusername = request.session.get('username')
    post = request.POST
    level_id_lists = escape(post.get("level_id_lists")) # 目录ID#
    level_id_list = level_id_lists.split(';')
    read_m_lists = escape(post.get("read_m_lists"))
    read_m_list = read_m_lists.split(';')  # 查看和修改
    account_lists = escape(post.get("account_lists"))
    account_list = account_lists.split(';')  # 申请人AD
    if adusername:
        addapplysuccess = 1
        thr_apply_update(adusername,level_id_list,read_m_list,account_list)#异步申请权限防止申请权限人数多
        result = {'status': addapplysuccess}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

def dfsapplys(request):
    try:
        username = request.session.get('username')
        displayname = request.session.get('displayname')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        level1list = showlevel1()
        return render_to_response('dfsweb/dfsapplys.html', locals())
    except Exception as e:
        logmanager().log(returnid=0, username=username, ip=ip, message="dfsapplys,多人文件夹权限申请页面无法打开：" + str(e), issuccess=0, methodname="dfsapplys", returnparameters=str(request.POST),
                         types="dfs")
        return HttpResponseRedirect('/', request)


#一键添加多人权限（确认输入是否是AD账户）
def groupmembers(request):
    username = request.session.get('username')
    groupmembers=escape(request.POST.get('groupmembers'))
    try:
        mysqlallvalue = dbinfo_select_global_configuration()
        if mysqlallvalue:
            domain = str(mysqlallvalue[0]['ad_domain'])
        else:
            domain = "test"
        if username:
            if groupmembers:
                newgroupmembers = groupmembers.strip().split('\n')
                newgroupmembers = list(set(newgroupmembers))
                adaccount_lists = list()
                elists = list()
                for newgroupmember in newgroupmembers:
                    if '@' in newgroupmember:
                        GetobjectPropertybysmtps = adapi().Initialapi("GetobjectPropertybysmtp", objects=newgroupmember)
                        if GetobjectPropertybysmtps['isSuccess']:
                            adaccount_lists.append(GetobjectPropertybysmtps['message'][0].get('sAMAccountName',''))#添加AD账号
                        else:
                            elists.append(newgroupmember)
                    else:
                        if ObjectExist(newgroupmember, 'user', domain):
                            adaccount_lists.append(newgroupmember)
                        else:
                            elists.append(newgroupmember)
                if len(elists)==0:
                    status = 1
                else:
                    status =2
            else:
               status=3
        else:
            return HttpResponseRedirect('/', request)
    except Exception as e:
        status = 3
    result = {'status': status, 'adaccount_lists': adaccount_lists, 'error': elists}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#显示我的申请进度
def refer(request):
    username=request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        except Exception as e:
            flowlists=[]
            logmanager().log(returnid=0, username=username, ip=ip, message="refer,我的申请进度页面无法打开：" + str(e), issuccess=0, methodname="refer", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/refer.html', locals())
    else:
        return HttpResponseRedirect('/', request)

# get getrefer
def getrefer(request):
    username = request.session.get('username')
    if username:
        try:
            row = showmyflowbypage(username)
            total = len(row)
            result = {'row': row, "total": total}
        except Exception as e:
            result = {'row': [], "total": 0}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result, indent=4, sort_keys=True, default=str))
        return response
    else:
        return HttpResponseRedirect('/', request)

#显示主管审批单详情
def approval(request):
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            approvelists = showmyapproval(username)
        except Exception as e:
            approvelists = []
            logmanager().log(returnid=0, username=username, ip=ip, message="approval,显示主管审批单详情：" + str(e), issuccess=0, methodname="approval", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/approval.html', locals())
    else:
        return HttpResponseRedirect('/', request)

#主管和代理人一键审批同意方法
def allsucapproval(request):
    username=request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            firstcelllists=escape(request.POST.get('firstcelllists'))
            firstcelllist = firstcelllists.split(';')
            thr_allsucapproval(username,firstcelllist)
            result = 1
        except Exception as e:
            result = 2
            logmanager().log(returnid=0, username=username, ip=ip, message="allsucapproval,主管一键审批同意方法：" + str(e), issuccess=0, methodname="allsucapproval", returnparameters=str(request.POST),
                             types="dfs")
        result = {'status': result}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#主管和代理人一键审批不同意的方法
def unallapproval(request):
    username=request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            firstcelllists=escape(request.POST.get('firstcelllists'))
            firstcelllist = firstcelllists.split(';')
            for i in range(len(firstcelllist)):
                approvalresult=directorapproval('0',now,'4',firstcelllist[i])
            if approvalresult==1:
                result=1
            else:
                result=2
        except Exception as e:
            result = 2
            logmanager().log(returnid=0, username=username, ip=ip, message="unallapproval,主管一键审批不同意方法：" + str(e), issuccess=0, methodname="unallapproval", returnparameters=str(request.POST),
                             types="dfs")
        result = {'status': result}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#显示文件夹关联人的所有审批单
def relationapproval(request):
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            approvelists = showrelationapproval(username)
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="relationapproval,显示文件夹管理员的所有审批单：" + str(e), issuccess=0, methodname="relationapproval", returnparameters=str(request.POST),
                             types="dfs")
            pprovelists = []
        return render_to_response('dfsweb/relationapproval.html', locals())
    else:
        return HttpResponseRedirect('/', request)


#文件夹关联人和代理人一键审批同意
def allrelationsucapproval(request):
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            firstcelllists=escape(request.POST.get('firstcelllists'))
            firstcelllist = firstcelllists.split(';')
            thr_all_re_sucapproval(username,firstcelllist)
            result = 1
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            if not app_relation:
                logmanager().log(returnid=2, username=username, ip=ip, message="allrelationsucapproval,非文件夹管理员一键审批同意", issuccess=0, methodname="allrelationsucapproval", returnparameters=str(request.POST),types="dfs")
        except Exception as e:
            result = 2
            logmanager().log(returnid=0, username=username, ip=ip, message="allrelationsucapproval,文件夹管理员一键审批同意：" + str(e), issuccess=0, methodname="allrelationsucapproval", returnparameters=str(request.POST),
                             types="dfs")
        result = {'status': result}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#文件夹关联人和代理人一键审批不同意
def unallrelationsucapproval(request):
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            firstcelllists=escape(request.POST.get('firstcelllists'))
            firstcelllist = firstcelllists.split(';')
            for i in range(len(firstcelllist)):
                relationapprovalresult=relationapprovaldb('0',now,'5',firstcelllist[i])
            if relationapprovalresult==1:
                result=1
            else:
                result=2
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            if not app_relation:
                logmanager().log(returnid=2, username=username, ip=ip, message="allrelationsucapproval,非文件夹管理员一键审批不同意", issuccess=0, methodname="allrelationsucapproval", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = 2
            logmanager().log(returnid=0, username=username, ip=ip, message="allrelationsucapproval,文件夹管理员一键审批不同意：" + str(e), issuccess=0, methodname="allrelationsucapproval", returnparameters=str(request.POST),
                             types="dfs")
        result = {'status': result}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)


#显示文件夹权限管理
def relationmanager(request):
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            level2namelists = []
            sel_account_to_groups = False
            app_director_count = showmyapproval_count(username)  # 显示主管需要的审批数量
            app_relation_count = showrelationapproval_count(username)  # 显示文件夹管理员需要的审批数量
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            if app_relation:
                level2namelists = app_relation
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
                if sel_account_to_groups:
                    level2namelists = getlevel2()
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="relationmanager,显示文件夹权限管理：" + str(e), issuccess=0, methodname="relationmanager", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/relationmanager.html', locals())
    else:
        return HttpResponseRedirect('/', request)
#查找文件夹权限组里面的成员
def searchgroupnamebyrelation(request):
    folder_level3_id=escape(request.POST.get('folder_level3_id'))
    perm_value=escape(request.POST.get('perm_value'))
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            if folder_level3_id and perm_value:
                showgroupnamebyrelations = showgroupnamebyrelation(folder_level3_id, perm_value) #通过数据库查找组
                if showgroupnamebyrelations:
                    group_name = showgroupnamebyrelations[0].get("group_name",'')
                    dict_group = adapi().Initialapi("GetUserFromGroup", groupname=group_name)#在AD里查找组的用户
                    if dict_group['isSuccess']:
                        rows = list()
                        li = []
                        for i in dict_group['message']['message']:
                            t = MyThread(i['member'])
                            li.append(t)
                            t.start()
                        for t in li:
                            t.join()
                            rows.append(t.get_result())
                        temptable_date=[]
                        for row in rows:
                            temptable_date.append({"group_name":group_name,"sAMAccountName":row['sAMAccountName'],"displayName":row['displayName'],"description":row['description']})
                        data = {"message":{"temptable_date": temptable_date,"group_name":group_name,"folder_level3_id":folder_level3_id},"isSuccess":True}
                    else:
                        data = {"isSuccess":False,"message":dict_group['message']['message']}
                else:
                    data = {"isSuccess": False, "message": "没有查询到组"}
            else:
                data = {"isSuccess": False, "message": "传入值有空"}
        except Exception as e:
            data = {"isSuccess": False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="searchgroupnamebyrelation,查找文件夹权限组里面的成员：" + str(e), issuccess=0, methodname="searchgroupnamebyrelation", returnparameters=str(request.POST),
                             types="dfs")
        result = {"data":data,}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)


#移除并发送邮件
def removegroupnamebyrelation(request):
    username = request.session.get('username')
    groupnamebyrelation=escape(request.POST.get('groupnamebyrelation'))
    usernamebyrelation=escape(request.POST.get('usernamebyrelation'))
    if username:
        try:
            if groupnamebyrelation and usernamebyrelation:
                RemoveUserFromGroups=adapi().Initialapi("RemoveUserFromGroup",sAMAccountName=usernamebyrelation,groupname=groupnamebyrelation)
                if RemoveUserFromGroups['isSuccess']:
                    dictflowids = getflowbygroupandusername(usernamebyrelation, groupnamebyrelation)
                    if dictflowids:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        opresult=operate(now,'7',dictflowids[0]['flowid'])
                    result=1
                    subject = u'文件夹权限被移除'
                    GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=usernamebyrelation, objectClass='user')
                    if GetobjectPropertys['isSuccess']:
                        mail = GetobjectPropertys['message'][0].get("mail", "")
                        if mail:
                            to_list = [mail]
                            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            html_content = "账户：" + GetobjectPropertys['message'][0]['sAMAccountName'] + ",的文件夹权限：" + groupnamebyrelation + ",被管理员:" + username + "移除"+now
                            send_html_email(subject, html_content, to_list)
                else:
                    result=2
            else:
                result=3
        except Exception as e:
            result = 3
        result = {'status': result}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#一键移除权限并发送邮件
def AllDelPermissions(request):
    username = request.session.get('username')
    getSelections=escape(request.POST.get('getSelections'))
    SuccessList = []
    ErrosList = []
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if app_relation or sel_account_to_groups:
                if getSelections:
                    getSelectionsLists=ast.literal_eval(getSelections.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    for getSelection in getSelectionsLists:
                        RemoveUserFromGroups=adapi().Initialapi("RemoveUserFromGroup",sAMAccountName=getSelection['sAMAccountName'],groupname=getSelection['group_name'])
                        if RemoveUserFromGroups['isSuccess']:
                            SuccessList.append(getSelection['sAMAccountName'])
                            dictflowids = getflowbygroupandusername(getSelection['sAMAccountName'], getSelection['group_name'])
                            if dictflowids:
                                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                opresult=operate(now,'7',dictflowids[0]['flowid'])
                            subject = u'文件夹权限被移除'
                            GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=getSelection['sAMAccountName'], objectClass='user')
                            if GetobjectPropertys['isSuccess']:
                                mail = GetobjectPropertys['message'][0].get("mail","")
                                if mail:
                                    to_list = [mail]
                                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    html_content = "账户：" + GetobjectPropertys['message'][0]['sAMAccountName'] + ",的文件夹权限：" + getSelection['group_name'] + ",被管理员:" + username + "移除"+now
                                    send_html_email(subject, html_content, to_list)
                        else:
                            ErrosList.append(getSelection['sAMAccountName'])
                    if SuccessList:
                        status=1
                    else:
                        status=2
                else:
                    status=3
            else:
                status = 3
                logmanager().log(returnid=2, username=username, ip=ip, message="AllDelPermissions,用户不是文件夹管理员,一键移除权限并发送邮件：" , issuccess=0, methodname="AllDelPermissions", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="AllDelPermissions,一键移除权限并发送邮件：" + str(e), issuccess=0, methodname="AllDelPermissions", returnparameters=str(request.POST),
                             types="dfs")
            status = 3
        result = {'status': status,"SuccessList":SuccessList,"ErrosList":ErrosList}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#一键添加权限
def AllAddPermissions(request):
    username = request.session.get('username')
    folder_level3_id=escape(request.POST.get('folder_level3_id'))
    perm_value=escape(request.POST.get('perm_value'))
    groupmembers = escape(request.POST.get('groupmembers'))
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if app_relation or sel_account_to_groups:
                mysqlallvalue = dbinfo_select_global_configuration()
                if mysqlallvalue:
                    domain = str(mysqlallvalue[0]['ad_domain'])
                else:
                    domain = "test"
                if groupmembers and perm_value and folder_level3_id:
                    showgroupnamebyrelations = showgroupnamebyrelation(folder_level3_id, perm_value)  # 通过数据库查找组
                    if showgroupnamebyrelations:
                        group_name = showgroupnamebyrelations[0].get("group_name", '')
                        newgroupmembers = groupmembers.strip().split('\n')
                        newgroupmembers = list(set(newgroupmembers))
                        adaccount_lists = list()
                        temptable_date= list()
                        elists = list()
                        for newgroupmember in newgroupmembers:
                            if '@' in newgroupmember:
                                GetobjectPropertybysmtps = adapi().Initialapi("GetobjectPropertybysmtp", objects=newgroupmember)
                                if GetobjectPropertybysmtps['isSuccess']:
                                    sAMAccountName = GetobjectPropertybysmtps['message'][0].get('sAMAccountName', '')
                                    adaccount_lists.append(GetobjectPropertybysmtps['message'][0].get('sAMAccountName', ''))  # 添加AD账号
                                else:
                                    elists.append(newgroupmember)
                            else:
                                if ObjectExist(newgroupmember, 'user', domain):
                                    adaccount_lists.append(newgroupmember)
                                else:
                                    elists.append(newgroupmember)
                        if adaccount_lists:
                            for adaccount in adaccount_lists:
                                AddUserToGroups = adapi().Initialapi("AddUserToGroup", sAMAccountName=adaccount, groupname=group_name)
                                if AddUserToGroups['isSuccess'] or "对象已存在" in AddUserToGroups['message']:
                                    temptable_date.append({"group_name":group_name,"sAMAccountName":adaccount,"displayName":"新加入对象","description":""})
                                else:
                                    elists.append(adaccount)
                        if temptable_date:
                            status = 1
                        else:
                            status = 2
                    else:
                        status = 3
                else:
                    status = 3
            else:
                status = 3
                logmanager().log(returnid=2, username=username, ip=ip, message="AllAddPermissions,用户不是文件夹管理员,一键添加权限：", issuccess=0, methodname="AllAddPermissions", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="AllAddPermissions,一键添加权限：" + str(e), issuccess=0, methodname="AllAddPermissions", returnparameters=str(request.POST),
                             types="dfs")
            status = 3
        result = {'status': status,"temptable_date":temptable_date,"elists":elists}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

# 修改文件夹管理员
def SetRelation(request):
    username = request.session.get('username')
    level2id_modal = escape(request.POST.get('level2id_modal'))
    adaccount_modal = escape(request.POST.get('adaccount_modal'))
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if app_relation or sel_account_to_groups:
                if level2id_modal and adaccount_modal:
                    GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=adaccount_modal, objectClass='user')
                    if GetobjectPropertys['isSuccess']:
                        mail = GetobjectPropertys['message'][0].get('mail','')
                        displayName = GetobjectPropertys['message'][0].get('displayName', '')
                        set_folder_level2_manages = set_folder_level2_manage(adaccount_modal, displayName, mail, level2id_modal)
                        if set_folder_level2_manages:
                            result = {'isSuccess': True, "message": {"level2_manager":adaccount_modal,"level2_manager_name":displayName,"level2_manager_mail":mail,}}
                        else:
                            result = {'isSuccess': False, "message": "插入数据库失败"}
                    else:
                        result = {'isSuccess': False, "message": "AD账户填写错误"}
                else:
                    result = {'isSuccess': False, "message": "传入空值"}
            else:
                result = {'isSuccess': False, "message": "用户不是文件夹管理员"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="SetRelation,修改文件夹管理员：", issuccess=0, methodname="SetRelation", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="SetRelation,修改文件夹管理员：" + str(e), issuccess=0, methodname="SetRelation", returnparameters=str(request.POST),
                             types="dfs")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#显示我的文件夹权限页面
def mydfs(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            get_management_configurations = get_management_configuration()
            DFS_distinguishedName = get_management_configurations.get('dfs_group', '')
            DfsGroupLists=[]
            GetAdGroups = adapi().Initialapi("GetAdGroup", username=username)
            if GetAdGroups and DFS_distinguishedName:
                for groups in GetAdGroups['message']['groups']:
                    if DFS_distinguishedName in groups:
                        groups_cn = (groups.split(',')[0]).replace("CN=","")
                        DfsGroupLists.append(groups_cn)
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="mydfs,我的文件夹权限页面：" + str(e), issuccess=0, methodname="mydfs", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/mydfs.html', locals())
    else:
        return HttpResponseRedirect('/', request)

#修改文件夹管理员 页面
def relationconfig(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
                if sel_account_to_groups:
                    level1list = showlevel1()
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="relationconfig,修改文件夹管理员页面：" + str(e), issuccess=0, methodname="relationconfig", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/relationconfig.html', locals())
    else:
        return HttpResponseRedirect('/', request)

# get 2层目录数据
def relationconfig_level2(request):
    username = request.session.get('username')
    if username:
        try:
            result = {'row': [], "total": 0}
            sel_account_to_groups = False
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
                if sel_account_to_groups:
                    row = getlevel2()
                    total = len(row)
                    result = {'row': row, "total": total}
        except Exception as e:
            result = {'row': [], "total": 0}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#根据一层目录ID 获取folder_level2 相关数据
def SearchRelationFromL(request):
    level1id=escape(request.POST.get('level1id'))
    username = request.session.get('username')
    if username:
        try:
            if level1id:
                show_folder_level1_to_ids = show_folder_level1_to_id(level1id)
                if show_folder_level1_to_ids:
                    level1_path=show_folder_level1_to_ids[0]['level1_path']+'\\'
                    row=[]
                    getlevel2Lists = getlevel2()
                    if getlevel2Lists:
                        for getlevel2s in getlevel2Lists:
                            if level1_path in getlevel2s['level2_path']:
                                row.append(getlevel2s)
                        result = {"isSuccess": True, "message": row}
                    else:
                        result = {"isSuccess": False, "message":'没有数据'}
                else:
                    result = {"isSuccess": False, "message": '没有一层目录'}
            else:
                result = {"isSuccess": False, "message": "传入值有空"}
        except Exception as e:
            result = {"isSuccess": False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#新建文件夹页面
def addfolderpage(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups:
                level1list = showlevel1()  #是DFS管理员显示全部
            elif app_relation: # 只是2层文件夹管理员
                level2namelists = app_relation#查找folder_level2 中的文件夹管理员
            else:
                level1list=[]
                level2namelists=[]
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="addfolderpage,新建文件夹页面：" + str(e), issuccess=0, methodname="addfolderpage", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/addfolderpage.html', locals())
    else:
        return HttpResponseRedirect('/', request)

#新建一层文件夹，并写数据库
def addfolderleve1(request):
    app_level1_path_list=(request.POST.get('app_level1_path_list')).replace(" ",'').replace("<",'').replace(">",'')
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups:
                SuccessList= []
                if app_level1_path_list:
                    app_level1_path_list = ast.literal_eval(app_level1_path_list.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    for level1_path in app_level1_path_list:
                        if ":\\" in level1_path:
                            CreateFolders = dfs_api().postapi("CreateFolder", src_path=level1_path)
                            if CreateFolders['isSuccess']:
                                Level1Folders = dfs_api().postapi("Level1Folder", path=level1_path)
                                if Level1Folders['isSuccess']:
                                    SuccessList.append(level1_path)
                    if SuccessList:
                        result = {"isSuccess": True, "message": SuccessList}
                    else:
                        result = {"isSuccess": False, "message": "都没有新建成功"}
                else:
                    result = {"isSuccess": False, "message": "传入值为空"}
            else:
                result = {"isSuccess": False, "message": "您不是IT管理员"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="addfolderleve1,新建一层文件夹，并写数据库：", issuccess=0, methodname="addfolderleve1", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = {"isSuccess": False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="addfolderleve1,新建一层文件夹，并写数据库：" + str(e), issuccess=0, methodname="addfolderleve1", returnparameters=str(request.POST),
                             types="dfs")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#新建二层文件夹，并写数据库
def addfolderleve2(request):
    app_level2_path_list=(request.POST.get('app_level2_path_list')).replace(" ",'').replace("<",'').replace(">",'')
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups or app_relation:
                SuccessList= []
                if app_level2_path_list:
                    app_level2_path_list = ast.literal_eval(app_level2_path_list.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    GetobjectPropertys = adapi().Initialapi("GetobjectProperty", objects=username, objectClass='user')
                    if GetobjectPropertys['isSuccess']:
                        mail = GetobjectPropertys['message'][0].get('mail', '')
                        displayName = GetobjectPropertys['message'][0].get('displayName', '')
                    for level2_path in app_level2_path_list:
                        if ":\\" in level2_path:
                            CreateFolders = dfs_api().postapi("CreateFolder", src_path=level2_path)
                            if CreateFolders['isSuccess']:
                                Level2Folders = dfs_api().postapi("Level2Folder", path=level2_path)
                                if Level2Folders['isSuccess']:
                                    SuccessList.append(level2_path)
                                    set_folder_level2_manage_from_paths = set_folder_level2_manage_from_path(username, displayName, mail, level2_path)
                    if SuccessList:
                        result = {"isSuccess": True, "message": SuccessList}
                    else:
                        result = {"isSuccess": False, "message": "都没有新建成功"}
                else:
                    result = {"isSuccess": False, "message": "传入值为空"}
            else:
                result = {"isSuccess": False, "message": "您不是文件夹管理员"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="addfolderleve2,新建二层文件夹，并写数据库", issuccess=0, methodname="addfolderleve2", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = {"isSuccess": False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="addfolderleve2,新建二层文件夹，并写数据库" + str(e), issuccess=0, methodname="addfolderleve2", returnparameters=str(request.POST),
                             types="dfs")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#新建三层文件夹，并写数据库
def addfolderleve3(request):
    app_level3_path_list=(request.POST.get('app_level3_path_list')).replace(" ",'').replace("<",'').replace(">",'')
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups or app_relation:
                SuccessList= []
                if app_level3_path_list:
                    app_level3_path_list = ast.literal_eval(app_level3_path_list.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    for level3_path in app_level3_path_list:
                        if ":\\" in level3_path:
                            CreateFolders = dfs_api().postapi("CreateFolder", src_path=level3_path)
                            if CreateFolders['isSuccess']:
                                SuccessList.append(level3_path)
                                thr_creat_folder_level3(username, level3_path)
                    if SuccessList:
                        result = {"isSuccess": True, "message": SuccessList}
                    else:
                        result = {"isSuccess": False, "message": "都没有新建成功"}
                else:
                    result = {"isSuccess": False, "message": "传入值为空"}
            else:
                result = {"isSuccess": False, "message": "您不是文件夹管理员"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="addfolderleve3,新建三层文件夹，并写数据库", issuccess=0, methodname="addfolderleve3", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = {"isSuccess": False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="addfolderleve3,新建三层文件夹，并写数据库：" + str(e), issuccess=0, methodname="addfolderleve3", returnparameters=str(request.POST),
                             types="dfs")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#删除文件夹页面
def delfolderpage(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups:
                level1list = showlevel1()
            elif app_relation:
                level2namelists = app_relation#查找folder_level2 中的文件夹管理员
            else:
                level1list=[]
                level2namelists=[]
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="delfolderpage,删除文件夹页面：" + str(e), issuccess=0, methodname="delfolderpage", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/delfolderpage.html', locals())
    else:
        return HttpResponseRedirect('/', request)

#删除文件夹，并写数据库
def delfolderlevel(request):
    app_level_path_list=(request.POST.get('app_level_path_list')).replace(" ",'').replace("<",'').replace(">",'')
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups or app_relation:
                SuccessList= []
                if app_level_path_list:
                    app_level_path_list = ast.literal_eval(app_level_path_list.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    for level_path in app_level_path_list:
                        if ":\\" in level_path:
                            DeleteFolder = dfs_api().postapi("DeleteFolder", src_path=level_path)
                            if DeleteFolder['isSuccess']:
                                SuccessList.append(level_path)
                    if SuccessList:
                        result = {"isSuccess": True, "message": SuccessList}
                    else:
                        result = {"isSuccess": False, "message": "都没有新建成功"}
                else:
                    result = {"isSuccess": False, "message": "传入值为空"}
            else:
                result = {"isSuccess": False, "message": "您不是文件夹管理员"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="delfolderlevel,删除文件夹，并写数据库", issuccess=0, methodname="delfolderlevel", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = {"isSuccess": False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="delfolderlevel,删除文件夹，并写数据库" + str(e), issuccess=0, methodname="delfolderlevel", returnparameters=str(request.POST),
                             types="dfs")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#重命名文件夹页面
def renamefolderpage(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups:
                level1list = showlevel1()
            elif app_relation:
                level2namelists = app_relation  # 查找folder_level2 中的文件夹管理员
            else:
                level1list = []
                level2namelists = []
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="renamefolderpage,重命名文件夹页面：" + str(e), issuccess=0, methodname="renamefolderpage", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/renamefolderpage.html', locals())
    else:
        return HttpResponseRedirect('/', request)

#重命名文件夹页面，并写数据库
def renamefolderlevel(request):
    app_level=(request.POST.get('app_level')).replace(" ",'').replace("<",'').replace(">",'')
    username = request.session.get('username')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups or app_relation:
                SuccessList= []
                if app_level:
                    app_level = ast.literal_eval(app_level.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    for app_level_dict in app_level:
                        old_path = app_level_dict.get('path','')
                        new_name = app_level_dict.get('newname', '')
                        if ":\\" in old_path:
                            new_path = old_path.split("\\")
                            del (new_path[-1])
                            new_path = '\\'.join(new_path) + '\\' + new_name
                            DeleteFolder = dfs_api().postapi("RenameFolder", src_path=old_path,dest_path=new_path)
                            if DeleteFolder['isSuccess']:
                                SuccessList.append(new_path)
                    if SuccessList:
                        result = {"isSuccess": True, "message": SuccessList}
                    else:
                        result = {"isSuccess": False, "message": "都没有重命名成功"}
                else:
                    result = {"isSuccess": False, "message": "传入值为空"}
            else:
                result = {"isSuccess": False, "message": "您不是文件夹管理员"}
            if not result['isSuccess']:
                logmanager().log(returnid=2, username=username, ip=ip, message="renamefolderlevel,重命名文件夹页面，并写数据库", issuccess=0, methodname="renamefolderlevel", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            result = {"isSuccess": False, "message": str(e)}
            logmanager().log(returnid=0, username=username, ip=ip, message="renamefolderlevel,重命名文件夹页面，并写数据库" + str(e), issuccess=0, methodname="renamefolderlevel", returnparameters=str(request.POST),
                             types="dfs")
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)


#流程日志页面
def flowlog(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="flowlog,流程日志页面：" + str(e), issuccess=0, methodname="flowlog", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/flowlog.html', locals())
    else:
        return HttpResponseRedirect('/', request)

# get getflowlog
def getflowlog(request):
    username = request.session.get('username')
    if username:
        try:
            row = sel_folder_dfs_flow()
            total = len(row)
            result = {'row': row, "total": total}
        except Exception as e:
            result = {'row': [], "total": 0}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result,indent=4, sort_keys=True, default=str))
        return response
    else:
        return HttpResponseRedirect('/', request)

#文件夹操作日志
def folderapilog(request):
    username = request.session.get('username')
    displayname= request.session.get('displayname')
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="folderapilog,文件夹操作日志：" + str(e), issuccess=0, methodname="folderapilog", returnparameters=str(request.POST),
                             types="dfs")
        return render_to_response('dfsweb/folderapilog.html', locals())
    else:
        return HttpResponseRedirect('/', request)

# get getfolderapilog
def getfolderapilog(request):
    username = request.session.get('username')
    if username:
        try:
            sel_account_to_groups = False
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            if sel_account_to_groups or app_relation:
                row = sel_folder_api_log()
                total = len(row)
                result = {'row': row, "total": total}
            else:
                result = {'row': [], "total": 0}
        except Exception as e:
            result = {'row': [], "total": 0}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result,indent=4, sort_keys=True, default=str))
        return response
    else:
        return HttpResponseRedirect('/', request)


##前置权限判断
def dfs_permission(request):
    username = request.session.get('username')
    result = {'dfs_manager': False, "file_manager": False, "app_director_count": 0, "app_relation_count": 0,"dfs_switch":''}
    if username:
        try:
            sel_account_to_groups = False
            dfs_switch = ""
            app_director_count = showmyapproval_count(username)  # 显示主管需要的审批数量
            app_relation_count = showrelationapproval_count(username)  # 显示文件夹管理员需要的审批数量
            app_relation = showlevel2byusername(username)  # 是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()  # 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group", '')
                sel_account_to_groups = sel_account_to_group(username, it_group)  # 是不是DFS管理员 True
            management_configuration = get_management_configuration()
            if management_configuration:
                dfs_switch = management_configuration.get("dfs_switch","")
            result = {'dfs_manager': sel_account_to_groups, "file_manager": app_relation,"app_director_count":app_director_count,"app_relation_count":app_relation_count,"dfs_switch":dfs_switch}
        except Exception as e:
            result = {'dfs_manager': False, "file_manager": False, "app_director_count": 0, "app_relation_count": 0,"dfs_switch":''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,indent=4, sort_keys=True, default=str))
    return response



# get 权限初始化
def show_folder_first_choice(request):
    username = request.session.get('username')
    if username:
        try:
            result = {'row': [], "total": 0}
            if username.lower() =='administrator':
                row = get_folder_first_choice()
                total = len(row)
                result = {'row': row, "total": total}
        except Exception as e:
            result = {'row': [], "total": 0}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#一键移除DFS 目录 权限初始化
def DelFileConfig(request):
    username = request.session.get('username')
    getSelections=(request.POST.get('getSelections')).replace(" ",'').replace("<",'').replace(">",'')
    SuccessList=[]
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            if username.lower() == 'administrator':
                if getSelections:
                    getSelectionsLists=ast.literal_eval(getSelections.replace("true","'true'").replace("false","'false'").replace("null","'null'"))
                    for getSelection in getSelectionsLists:
                        del_folder_first_choice_id(getSelection['id'])
                        SuccessList.append(getSelection['id'])
                    status = 1
                else:
                    status=3
            else:
                status = 3
                logmanager().log(returnid=2, username=username, ip=ip, message="DelFileConfig,用户不是administrator：" , issuccess=0, methodname="DelFileConfig", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="DelFileConfig,一键移除DFS 权限初始化：" + str(e), issuccess=0, methodname="DelFileConfig", returnparameters=str(request.POST),
                             types="dfs")
            status = 3
        result = {'status': status,'SuccessList':SuccessList}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#添加DFS目录 权限初始化
def AddFileConfig(request):
    username = request.session.get('username')
    folder_level=escape(request.POST.get('folder_level'))
    folder_path = escape(request.POST.get('folder_path'))
    server_manager = escape(request.POST.get('server_manager'))
    SuccessList=[]
    if username:
        try:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            if username.lower() == 'administrator':
                if folder_level and folder_path and server_manager:
                    add_folder_first_choices = add_folder_first_choice(folder_level, folder_path, server_manager)
                    if add_folder_first_choices:
                        SuccessList.append(add_folder_first_choices)
                    status = 1
                else:
                    status=3
            else:
                status = 3
                logmanager().log(returnid=2, username=username, ip=ip, message="AddFileConfig,用户不是administrator：" , issuccess=0, methodname="AddFileConfig", returnparameters=str(request.POST),
                                 types="dfs")
        except Exception as e:
            logmanager().log(returnid=0, username=username, ip=ip, message="AddFileConfig,添加DFS目录 权限初始化：" + str(e), issuccess=0, methodname="AddFileConfig", returnparameters=str(request.POST),
                             types="dfs")
            status = 3
        result = {'status': status,'SuccessList':SuccessList}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#添加DFS目录 测试api 连接
def dfs_api_test(request):
    username = request.session.get('username')
    if username:
        try:
            result = dfs_api().postapi("dfs_api_test")
        except Exception as e:
            result = {'isSuccess': False, 'message':str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#文件夹权限权限初始化
def FirstFolderAuthority(request):
    username = request.session.get('username')
    if username:
        try:
            mysqlallvalue = dbinfo_select_global_configuration()
            if mysqlallvalue:
                domain = str(mysqlallvalue[0]['ad_domain'])
            else:
                domain = "test"
            set_file_FirstFolderAuthority(domain)
            result = {'isSuccess': True, 'message':'成功'}
        except Exception as e:
            result = {'isSuccess': False, 'message':str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

#文件夹配置管理页面
def dfsconfigtion(request):
    try:
        username = request.session.get('username','')
        displayname = request.session.get('displayname','')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        management_configuration = get_management_configuration()
        return render_to_response('admin/dfsconfigtion.html', locals())
    except Exception as e:
        print(e)
        logmanager().log(returnid=0, username=username, ip=ip, message="dfsconfigtion,文件夹配置管理页面：" + str(e), issuccess=0, methodname="dfsconfigtion", returnparameters=str(request.POST),
                         types="dfs")
        return HttpResponseRedirect('/', request)


# 删除文件夹配置
def delDfsConfig(request):
    username = request.session.get('username')
    if username.lower() =='administrator':
        try:
            management_configuration = get_management_configuration()
            if management_configuration:
                del_dfs_config = del_management_configuration_dfs()
                if del_dfs_config:
                    result = {'isSuccess': True, 'message': '数据更新成功'}
                else:
                    result = {'isSuccess': False, 'message': '数据更新失败'}
            else:
                result = {'isSuccess': False, 'message': '没有找到这列数据'}
        except Exception as e:
            result = {'isSuccess': False, 'message':str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

# 更新文件夹服务器接口地址
def DfsApiConfigtion(request):
    username = request.session.get('username')
    if username.lower() == 'administrator':
        try:
            inputdfs_api = escape(request.POST.get('inputdfs_api', ''))
            mysqlallvalue = dbinfo_select_global_configuration()
            if mysqlallvalue:
                domain = str(mysqlallvalue[0]['ad_domain'])
            else:
                domain = ''
            if inputdfs_api and domain:
                management_configuration = get_management_configuration()
                if management_configuration:
                    dfs_api_config =update_management_configuration_dfs_api(inputdfs_api)
                else:
                    dfs_api_config =insert_management_configuration_dfs_api(inputdfs_api,domain)
                if dfs_api_config:
                    mysql_host = readprofile('mysql', 'ip')
                    mysql_user = readprofile('mysql', 'username')
                    mysql_port = readprofile('mysql', 'Port')
                    mysql_password = (readprofile('mysql', 'Password'))
                    mysql_database = 'itdev-portal'
                    dfs_api_mysqlconfig = dfs_api().postapi("dfs_api_mysqlconfig", mysql_host=mysql_host, mysql_user=mysql_user, mysql_port=mysql_port, mysql_password=mysql_password,
                                                            mysql_database=mysql_database)
                    if dfs_api_mysqlconfig['isSuccess']:
                        result = {'isSuccess': True, 'message': '数据更新成功'}
                    else:
                        result = {'isSuccess': False, 'message': '数据库连接失败'}
                else:
                    result = {'isSuccess': False, 'message': '数据更新失败'}

            else:
                result = {"isSuccess": False, "message": "数据不完整"}
        except Exception as e:
            result = {'isSuccess': False, 'message': str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

# 更新文件夹配置
def saveAllDfsConfig(request):
    username = request.session.get('username')
    if username.lower() =='administrator':
        try:
            dfs_group = escape(request.POST.get('dfs_group',''))
            Basic_authority = escape(request.POST.get('Basic_authority',''))
            dfs_manager = escape(request.POST.get('dfs_manager',''))
            AD_time = int(escape(request.POST.get('AD_time','')))
            dfs_relation_name = escape(request.POST.get('dfs_relation_name',''))
            dfs_relation = escape(request.POST.get('dfs_relation', ''))
            dfs_relation_mail = escape(request.POST.get('dfs_relation_mail', ''))
            if dfs_group and Basic_authority and dfs_manager and dfs_relation and dfs_relation_mail and dfs_relation_name and AD_time:
                mysqlallvalue = dbinfo_select_global_configuration()
                if mysqlallvalue:
                    domain = str(mysqlallvalue[0]['ad_domain'])
                    if domain:
                        if ObjectExist(dfs_manager, 'user', domain) and ObjectExist(dfs_relation, 'user', domain):
                            management_configuration = get_management_configuration()
                            if management_configuration:
                                del_dfs_config = update_management_configuration_dfs(dfs_group,Basic_authority,dfs_manager,AD_time,dfs_relation_name,dfs_relation,dfs_relation_mail)
                            else:
                                del_dfs_config = insert_management_configuration_dfs(dfs_group, Basic_authority, dfs_manager, AD_time, dfs_relation_name, dfs_relation, dfs_relation_mail,domain)
                            if del_dfs_config:
                                result = {'isSuccess': True, 'message': '数据更新成功'}
                            else:
                                result = {'isSuccess': False, 'message': '数据更新失败'}
                    else:
                        result = {'isSuccess': False, 'message': '数据不完整'}
                else:
                    result = {'isSuccess': False, 'message': '管理员账户必须是AD账户'}
            else:
                result = {"isSuccess":False,"message":"数据不完整"}
        except Exception as e:
            result = {'isSuccess': False, 'message':str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)

# 打开或者关闭文件夹权限相关
def DfsConfig(request):
    username = request.session.get('username')
    if username.lower() =='administrator':
        try:
            dfs_switch = escape(request.POST.get('dfs_switch', ''))
            management_configuration = get_management_configuration()
            if management_configuration:
                if dfs_switch =="0" or dfs_switch =="1":
                    update_management_configuration = update_management_configuration_dfs_switch(dfs_switch)
                    if update_management_configuration:
                        result = {'isSuccess': True, 'message': '数据更新成功'}
                    else:
                        result = {'isSuccess': False, 'message': '数据更新失败'}
                else:
                    result = {'isSuccess': False, 'message': '传入数据不对'}
            else:
                result = {'isSuccess': False, 'message': '没有找到这列数据'}
        except Exception as e:
            result = {'isSuccess': False, 'message':str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    else:
        return HttpResponseRedirect('/', request)