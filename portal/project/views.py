import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.hashers import make_password, check_password

from adapi.dbinfo import searchflowdcount, shwotitle
from admin_account.dbinfo import dbinfo_select_global_configuration
from dfs.dbinfo import showmyapproval_count, showrelationapproval_count, showlevel2byusername
from itportal.settings import administratorpassword
from django.shortcuts import render, HttpResponseRedirect
from adapi.ad_api import adapi, sel_account_to_group


# Create your views here.
from jzaccount.jzscheduler import triggerjob


def index(request):
    try:
        username = request.session.get('username')
        displayname = request.session.get('displayname')
        if username:
            sel_account_to_groups =False
            app_director_count = showmyapproval_count(username)#显示主管需要的审批数量
            app_relation_count = showrelationapproval_count(username) #显示文件夹管理员需要的审批数量
            app_relation = showlevel2byusername(username) #是不是文件夹管理员
            global_configuration = dbinfo_select_global_configuration()# 查找数据
            if global_configuration:
                it_group = global_configuration[0].get("it_group",'')
                sel_account_to_groups = sel_account_to_group(username, it_group) #是不是DFS管理员 True
            return render_to_response('index.html', locals())
        else:
            return HttpResponseRedirect('/', request)
    except:
        return HttpResponseRedirect('/', request)



def portal(request):
    xx = triggerjob()
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    tltile = shwotitle()
    return render_to_response('portal.html', locals())

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/portal/', request)

def userlogin(request):
    post = request.POST
    username = post.get("Username")
    password = post.get("Password")
    returnbackurl = request.session.get("returnbackurl")
    try:
        if not returnbackurl:
            returnbackurl = r'/'
        if username:
            if password:
                if username.lower() == 'administrator':
                    # adminpassword = make_password('ITPortal...123')
                    if not dbinfo_select_global_configuration():
                        adminoldassword = administratorpassword
                    else:
                        adminsqlpassword = dbinfo_select_global_configuration()[0]['adminpwd']
                        if adminsqlpassword == '' or adminsqlpassword == None or adminsqlpassword == "None":
                            adminoldassword = administratorpassword
                        else:
                            adminoldassword = adminsqlpassword
                    if check_password(password,adminoldassword):
                        request.session['username'] = 'administrator'
                        request.session['displayname'] = '超级管理员'
                        request.session['titleshow'] = 'IT开放平台'
                        status = {'backurl': '/adminconfig/', 'status': 'success'}
                    else:
                        status = {'backurl': '', 'status': 'errorpasswd'}
                else:
                    loginvalue = adapi().Initialapi('VerifyUserLogin', username=username, password=password)
                    if loginvalue['isSuccess']:
                        request.session['username'] = username.lower()
                        request.session['displayname'] = loginvalue['message']['name']
                        # tltile = shwotitle()
                        # if tltile == None or tltile ==False :
                        #     request.session['titleshow']='IT开放平台'
                        # else:
                        #     request.session['titleshow'] = shwotitle()['title']
                        request.session['jobnumber'] = loginvalue['message']['jobnumber']
                        request.session['givenName'] = loginvalue['message']['givenName']
                        request.session['DN'] = loginvalue['message']['DN']
                        request.session['description'] = loginvalue['message']['description']
                        request.session['guid'] = loginvalue['message']['guid']
                        request.session['mail'] = loginvalue['message']['mail']
                        request.session['sn'] = loginvalue['message']['sn']
                        request.session['returnbackurl'] = ''
                        status = {'backurl': returnbackurl, 'status': 'success'}
                    else:
                        status = {'backurl':'','status':'errorpasswd'}
            else:
                status = {'backurl': '', 'status': 'nopassword'}
        else:
            status = {'backurl': '', 'status': 'nouser'}
    except Exception as e:
        status = {'backurl': '', 'status': 'error'}
    result =status
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#首页审批条数
def showcountman(request):
    username = request.session.get('username')
    try:
        directorcount = 0
        if username:
            directorcount=searchflowdcount(username)[0]['count(* )']
    except Exception as e:
        directorcount=0
    result = {'status':directorcount}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response