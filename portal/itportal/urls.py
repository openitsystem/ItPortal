"""itportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin\
from project import views as project_views
from admin_account import views as admin_account
from tools import views as tools_views
from mail import views as mail_views
from dfs import views as dfs_views
from internet import views as internet_views
from overall import views as overall_views
from jzaccount import views as jzaccount_views
from  api import approvalapi as api_approvalapi

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
]
urlpatterns += [
    url(r'^$|^portal/$', project_views.portal,name="portal"),
    url(r'^index/$', project_views.index,name='index'),
    url(r'^userlogin/$', project_views.userlogin,name='userlogin'),
    url(r'^logout/$', project_views.logout,name="logout"),
    url(r'^adminconfig/$', admin_account.adminconfig,name="adminconfig"),
    url(r'^basisite/$', admin_account.basisite,name="basisite"),
    url(r'^showcountman/$', project_views.showcountman, name="showcountman"),
    url(r'^changeadminpwd/$', admin_account.changeadminpwd,name="changeadminpwd"),
    # url(r'^addadips/$', admin_account.addadips,name="addadips"),
    # url(r'^deladdadips/$', admin_account.deladdadips,name="deladdadips"),
    url(r'^mysqllinktest/$', admin_account.mysqllinktest,name="mysqllinktest"),
    url(r'^delsqlconfig/$', admin_account.delsqlconfig,name="delsqlconfig"),
    url(r'^delmailsend/$', admin_account.delmailsend,name="delmailsend"),
    url(r'^delmysqllink/$', admin_account.delmysqllink,name="delmysqllink"),
    url(r'^deliislink/$', admin_account.deliislink,name="deliislink"),
    url(r'^deladlink/$', admin_account.deladlink,name="deladlink"),
    url(r'^delexlink/$', admin_account.delexlink,name="delexlink"),
    url(r'^iislinktest/$', admin_account.iislinktest,name="iislinktest"),
    url(r'^adlinktest/$', admin_account.adlinktest,name="adlinktest"),
    url(r'^exlinktest/$', admin_account.exlinktest,name="exlinktest"),
    url(r'^itgroupsearch/$', admin_account.itgroupsearch,name="itgroupsearch"),
    url(r'^showitgroupmembers/$', admin_account.showitgroupmembers,name="showitgroupmembers"),
    url(r'^delitgroup/$', admin_account.delitgroup,name="delitgroup"),
    url(r'^sendmailtest/$', admin_account.sendmailtest,name="sendmailtest"),
    url(r'^mangeronelyupdate/$', admin_account.mangeronelyupdate,name="mangeronelyupdate"),
    url(r'^updateconfigall/$', admin_account.updateconfigall,name="updateconfigall"),
    url(r'^mangeronelysave/$', admin_account.mangeronelysave,name="mangeronelysave"),
    url(r'^delmysqlmanger/$', admin_account.delmysqlmanger,name="delmysqlmanger"),
    url(r'^removeallgroupmemberfromadmin/$', admin_account.removeallgroupmemberfromadmin,name="removeallgroupmemberfromadmin"),
    url(r'^addgroupmembersfromadmin/$', admin_account.addgroupmembersfromadmin,name="addgroupmembersfromadmin"),
    url(r'^delmailmemberfromadmin/$', admin_account.delmailmemberfromadmin,name="delmailmemberfromadmin"),
    url(r'^delmysqlmanger/$', admin_account.delmysqlmanger,name="delmysqlmanger"),
    url(r'^apimanger/$', admin_account.apimanger,name="apimanger"),
    url(r'^saveapimanger/$', admin_account.saveapimanger,name="saveapimanger"),
    url(r'^delmysqlapi/$', admin_account.delmysqlapi,name="delmysqlapi"),
    url(r'^deluserphoneapi/$', admin_account.deluserphoneapi,name="deluserphoneapi"),
    url(r'^delsendmesspi/$', admin_account.delsendmesspi,name="delsendmesspi"),
    url(r'^getusermobile/$', admin_account.getusermobile,name="getusermobile"),
    url(r'^saveusertophone/$', admin_account.saveusertophone,name="saveusertophone"),
    url(r'^testmobilesend/$', admin_account.testmobilesend,name="testmobilesend"),
    url(r'^savephonesend/$', admin_account.savephonesend,name="savephonesend"),
    url(r'^pwdremindertips/$', admin_account.pwdremindertips,name="pwdremindertips"),
    url(r'^changepwdremindertips/$', admin_account.changepwdremindertips,name="changepwdremindertips"),
    url(r'^saveallmessage/$', admin_account.saveallmessage,name="saveallmessage"),
    url(r'^deltitlesql/$', admin_account.deltitlesql,name="deltitlesql"),
    url(r'^titlesaveqsl/$', admin_account.titlesaveqsl,name="titlesaveqsl"),
    url(r'^titleupdateqsl/$', admin_account.titleupdateqsl,name="titleupdateqsl"),
    url(r'^testapinprocess/$', admin_account.testapinprocess,name="testapinprocess"),
    url(r'^savemangeapiin/$', admin_account.savemangeapiin,name="savemangeapiin"),
    url(r'^deloutapi/$', admin_account.deloutapi,name="deloutapi"),

]
#tools
urlpatterns += [
    url(r'^changepwd/$', tools_views.changepwd,name="changepwd"),
    url(r'^resetpwd/$', tools_views.resetpwd, name="resetpwd"),
    url(r'^usersetchange/$', tools_views.usersetchange, name="usersetchange"),
    url(r'^userpwdchange/$', tools_views.userpwdchange, name="userpwdchange"),
    url(r'^mailgroupmanagement/$', tools_views.mailgroupmanagement, name="mailgroupmanagement"),
    url(r'^managershowmailgroup/$', tools_views.managershowmailgroup, name="managershowmailgroup"),
    url(r'^managershowsendtomailgroup/$', tools_views.managershowsendtomailgroup, name="managershowsendtomailgroup"),
    url(r'^showmailgroup/$', tools_views.showmailgroup, name="showmailgroup"),
    url(r'^showmailgroupmembers/$', tools_views.showmailgroupmembers, name="showmailgroupmembers"),
    url(r'^delmailmember/$', tools_views.delmailmember, name="delmailmember"),
    url(r'^delmailsendtomember/$', tools_views.delmailsendtomember, name="delmailsendtomember"),
    url(r'^getmailgroupvalue/$', tools_views.getmailgroupvalue, name="getmailgroupvalue"),
    url(r'^addgroupmembers/$', tools_views.addgroupmembers, name="addgroupmembers"),
    url(r'^addgroupsendtomembers/$', tools_views.addgroupsendtomembers, name="addgroupsendtomembers"),
    url(r'^removeallgroupmember/$', tools_views.removeallgroupmember, name="removeallgroupmember"),
    url(r'^removeallsnedtogroupmember/$', tools_views.removeallsnedtogroupmember, name="removeallsnedtogroupmember"),
    url(r'^changemailgroupdisplaynamevalue/$', tools_views.changemailgroupdisplaynamevalue, name="changemailgroupdisplaynamevalue"),
    url(r'^changemailgroupamanagerhangevalue/$', tools_views.changemailgroupamanagerhangevalue, name="changemailgroupamanagerhangevalue"),
    url(r'^changemailgrouphasoutvalue/$', tools_views.changemailgrouphasoutvalue, name="changemailgrouphasoutvalue"),
    url(r'^delmailgroup/$', tools_views.delmailgroup, name="delmailgroup"),
    url(r'^showmailsendtogroupmembers/$', tools_views.showmailsendtogroupmembers, name="showmailsendtogroupmembers"),
    url(r'^getmailgroupsendto/$', tools_views.getmailgroupsendto, name="getmailgroupsendto"),
    url(r'^userquery/$', tools_views.user_query, name="userquery"),
    url(r'^UserProfile/$', tools_views.user_profile, name="UserProfile"),
    url(r'^userunlock/$', tools_views.user_unlock, name="userunlock"),
    url(r'^unlock/$', tools_views.unlock, name="unlock"),
    url(r'^addPwdNoLock/$', tools_views.addPwdNoLock, name="addPwdNoLock"),
    url(r'^addPwdNoLockGroup/$', tools_views.addPwdNoLockGroup, name="addPwdNoLockGroup"),
    url(r'^adresetpwd/$', tools_views.ad_resetpwd, name="adresetpwd"),
    url(r'^userresetpwd/$', tools_views.user_resetpwd, name="userresetpwd"),



]
#mail
urlpatterns += [
    url(r'^applypublicmail/$', mail_views.applypublicmail,name="applypublicmail"),
    url(r'^applymailpermission/$', mail_views.applymailpermission,name="applymailpermission"),
    url(r'^applymailgroup/$', mail_views.applymailgroup,name="applymailgroup"),
    url(r'^findmail/$', mail_views.findmail,name="findmail"),
    url(r'^findmailgroup/$', mail_views.findmailgroup,name="findmailgroup"),
    url(r'^findmailgroupmanager/$', mail_views.findmailgroupmanager,name="findmailgroupmanager"),
    url(r'^tobemanager/$', mail_views.tobemanager,name="tobemanager"),
    url(r'^tobepublicmailmanager/$', mail_views.tobepublicmailmanager,name="tobepublicmailmanager"),
    url(r'^submitApplication/$', mail_views.submitApplication,name="submitApplication"),
    url(r'^unlockmail/$', mail_views.unlockmail, name="unlockmail"),
    url(r'^accountexist/$', mail_views.accountexist, name="accountexist"),
    url(r'^acountad/$', mail_views.acountad, name="acountad"),
    url(r'^lockactive/$', mail_views.lockactive, name="lockactive"),
    url(r'^pumailuserapply/$', mail_views.pumailuserapply, name="pumailuserapply"),
    url(r'^mailgroupapply/$', mail_views.mailgroupapply, name="mailgroupapply"),
]

#jzaccount
urlpatterns += [
    url(r'^jzaccountapp/$', jzaccount_views.jzaccountapp, name="jzaccountapp"),
    url(r'^Effectiveaccount/$', jzaccount_views.Effective_account, name="Effectiveaccount"),
    url(r'^AccountManagement/$', jzaccount_views.Account_Management, name="AccountManagement"),
    url(r'^AccountAddManagement/$', jzaccount_views.Account_AddManagement, name="AccountAddManagement"),
    url(r'^creatjzcount/$', jzaccount_views.creatjzcount, name="creatjzcount"),
    url(r'^searphonesq/$', jzaccount_views.searphonesq, name="searphonesq"),
    url(r'^fileupload/$', jzaccount_views.fileupload, name="fileupload"),
    url(r'^updatejzdate/$', jzaccount_views.updatejzdate, name="updatejzdate"),
    url(r'^jzresetpwd/$', jzaccount_views.jzresetpwd, name="jzresetpwd"),
    url(r'^showjzcountmanger/$', jzaccount_views.showjzcountmanger, name="showjzcountmanger"),
    url(r'^deljzcountmessage/$', jzaccount_views.deljzcountmessage, name="deljzcountmessage"),
    url(r'^upjzmanger/$', jzaccount_views.upjzmanger, name="upjzmanger"),
    url(r'^showjzcountmangerALL/$', jzaccount_views.showjzcountmangerALL, name="showjzcountmangerALL"),
    url(r'^IFadmin/$', jzaccount_views.IFadmin, name="IFadmin"),
    url(r'^jzhtml/$', jzaccount_views.jzhtml, name="jzhtml"),
    url(r'^getGetUserFromGroup/$',jzaccount_views.getGetUserFromGroup, name="getGetUserFromGroup"),
    url(r'^DeleteApplicationPermission/$',jzaccount_views.Delete_application_permission, name="DeleteApplicationPermission"),
    url(r'^addjzmanger/$',jzaccount_views.addjzmanger, name="addjzmanger"),

]

#DFS
urlpatterns += [
    #文件夹权限申请
    url(r'^dfsapply/$', dfs_views.dfsapply,name="dfsapply"),
    url(r'^level2info/$', dfs_views.level2info, name='level2info'),
    url(r'^level3info/$', dfs_views.level3info, name='level3info'),
    url(r'^showlevel2relation/$',dfs_views.showlevel2relation,name='showlevel2relation'),
    url(r'^showlevel1level2level3/$',dfs_views.showlevel1level2level3,name='showlevel1level2level3'),
    url(r'^addapplytoflow/$',dfs_views.addapplytoflow,name='addapplytoflow'),
    #多人文件夹权限申请
    url(r'^dfsapplys/$', dfs_views.dfsapplys,name="dfsapplys"),
    url(r'^groupmembers/$', dfs_views.groupmembers, name='groupmembers'),
    #申请进度查看
    url(r'^refer/$', dfs_views.refer, name='refer'),
    url(r'^getrefer/$', dfs_views.getrefer, name='getrefer'),
    #主管审批
    url(r'^approval/$',dfs_views.approval,name='approval'),
    url(r'^allsucapproval/$', dfs_views.allsucapproval, name='allsucapproval'),
    url(r'^unallapproval/$',dfs_views.unallapproval,name='unallapproval'),
    #文件夹管理员审批
    url(r'^relationapproval/$',dfs_views.relationapproval,name='relationapproval'),
    url(r'^allrelationsucapproval/$', dfs_views.allrelationsucapproval, name='allrelationsucapproval'),
    url(r'^unallrelationsucapproval/$', dfs_views.unallrelationsucapproval, name='unallrelationsucapproval'),
    #文件夹权限管理
    url(r'^relationmanager/$',dfs_views.relationmanager,name='relationmanager'),
    url(r'^searchgroupnamebyrelation/$',dfs_views.searchgroupnamebyrelation,name='searchgroupnamebyrelation'),
    url(r'^removegroupnamebyrelation/$',dfs_views.removegroupnamebyrelation,name='removegroupnamebyrelation'),
    url(r'^AllDelPermissions/$',dfs_views.AllDelPermissions,name='AllDelPermissions'),
    url(r'^AllAddPermissions/$',dfs_views.AllAddPermissions,name='AllAddPermissions'),
    url(r'^SetRelation/$',dfs_views.SetRelation,name='SetRelation'),
    #我的文件夹权限
    url(r'^mydfs/$', dfs_views.mydfs,name='mydfs'),
    #修改文件夹管理员
    url(r'^relationconfig/$', dfs_views.relationconfig,name='relationconfig'),
    url(r'^relationconfig_level2/$', dfs_views.relationconfig_level2,name='relationconfig_level2'),
    url(r'^SearchRelationFromL/$', dfs_views.SearchRelationFromL,name='SearchRelationFromL'),
    # 新建文件夹
    url(r'^addfolderpage/$', dfs_views.addfolderpage, name='addfolderpage'),
    url(r'^addfolderleve1/$', dfs_views.addfolderleve1, name='addfolderleve1'),
    url(r'^addfolderleve2/$', dfs_views.addfolderleve2, name='addfolderleve2'),
    url(r'^addfolderleve3/$', dfs_views.addfolderleve3, name='addfolderleve3'),
    # 删除文件夹
    url(r'^delfolderpage/$', dfs_views.delfolderpage, name='delfolderpage'),
    url(r'^delfolderlevel/$', dfs_views.delfolderlevel, name='delfolderlevel'),
    #重命名文件夹页面
    url(r'^renamefolderpage/$', dfs_views.renamefolderpage, name='renamefolderpage'),
    url(r'^renamefolderlevel/$', dfs_views.renamefolderlevel, name='renamefolderlevel'),
    #流程日志
    url(r'^flowlog/$', dfs_views.flowlog, name='flowlog'),
    url(r'^getflowlog/$', dfs_views.getflowlog, name='getflowlog'),
    #文件夹操作日志
    url(r'^folderapilog/$', dfs_views.folderapilog, name='folderapilog'),
    url(r'^getfolderapilog/$', dfs_views.getfolderapilog, name='getfolderapilog'),
    #DFS权限判断
    url(r'^dfs_permission/$', dfs_views.dfs_permission, name='dfs_permission'),
    #权限初始化
    url(r'^dfsconfigtion/$', dfs_views.dfsconfigtion, name='dfsconfigtion'),
    url(r'^show_folder_first_choice/$', dfs_views.show_folder_first_choice, name='show_folder_first_choice'),
    url(r'^DelFileConfig/$', dfs_views.DelFileConfig, name='DelFileConfig'),
    url(r'^AddFileConfig/$', dfs_views.AddFileConfig, name='AddFileConfig'),
    url(r'^dfs_api_test/$', dfs_views.dfs_api_test, name='dfs_api_test'),
    url(r'^FirstFolderAuthority/$', dfs_views.FirstFolderAuthority, name='FirstFolderAuthority'),
    url(r'^delDfsConfig/$', dfs_views.delDfsConfig, name='delDfsConfig'),
    url(r'^saveAllDfsConfig/$', dfs_views.saveAllDfsConfig, name='saveAllDfsConfig'),
    url(r'^DfsConfig/$', dfs_views.DfsConfig, name='DfsConfig'),
    url(r'^DfsApiConfigtion/$', dfs_views.DfsApiConfigtion, name='DfsApiConfigtion'),
]


#网络权限
urlpatterns += [
#网络权限申请页面
    url(r'^access/$', internet_views.access, name='access'),
    url(r'^saveInternet/$', internet_views.saveInternet, name='saveInternet'),

]

#信息页面
urlpatterns += [
    url(r'^referuser/$', overall_views.referuser,name="referuser"),
    url(r'^review/$', overall_views.review,name="review"),
    url(r'^systemlog/$', overall_views.systemlog,name="systemlog"),
    url(r'^showmailpubapp/$', overall_views.showmailpubapp, name="showmailpubapp"),
    url(r'^showmailpubreview/$', overall_views.showmailpubreview, name="showmailpubreview"),
    url(r'^showsystemlog/$', overall_views.showsystemlog, name="showsystemlog"),
    url(r'^pumailaccid/$', overall_views.pumailaccid, name="pumailaccid"),
    url(r'^refuspubmail/$', overall_views.refuspubmail, name="refuspubmail"),
    url(r'^usershowid/$', overall_views.usershowid, name="usershowid"),
    url(r'^userindexvalueshow/$', overall_views.userindexvalueshow, name="userindexvalueshow"),
    url(r'^showtitle/$', overall_views.showtitle, name="showtitle"),
    url(r'^publicmailmanagement/$', overall_views.publicmailmanagement, name="publicmailmanagement"),
    url(r'^mailcountdel/$', overall_views.mailcountdel, name="mailcountdel"),
    url(r'^updatepubmess/$', overall_views.updatepubmess, name="updatepubmess"),
    url(r'^showmailpumangaer/$', overall_views.showmailpumangaer, name="showmailpumangaer"),
    url(r'^psdpubmailset/$', overall_views.psdpubmailset, name="psdpubmailset"),
    url(r'^systemlog_permission/$', overall_views.systemlog_permission, name="systemlog_permission"),

]

#api接口
urlpatterns += [
    url(r'^api/approvalapi/$', api_approvalapi.approvalapi, name="approvalapi"),
]