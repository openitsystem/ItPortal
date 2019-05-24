from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from folder_api.Profile import writeprofile
from folder_api.decrypt_api import api_auth_post
from folder_api.encrypt_decode import encrypt_and_decode
from folder_api.interface import *
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,HttpResponse
from watchdog.observers import Observer
from monitor_file.th_watchdog import thr_watchdog_folder
from monitor_file.views import thr_watchdog_start

class dfs_api_test(APIView):
    @api_auth_post
    def post(self, request):
        try:
            respjson = {'isSuccess': True, "message": "接口测试通过"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "接口测试不通过：" + str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response

class dfs_api_mysqlconfig(APIView):
    @api_auth_post
    def post(self, request):
        try:
            mysql_host = request.POST.get('mysql_host', '')
            mysql_port = request.POST.get('mysql_port', '')
            mysql_user = request.POST.get('mysql_user', '')
            mysql_password = request.POST.get('mysql_password', '')
            mysql_database = request.POST.get('mysql_database', '')
            mysql_password_jie = encrypt_and_decode().decrypted_text(mysql_password)
            if dbinfotest(mysql_host,mysql_port,mysql_user,mysql_password_jie,mysql_database):
                writeprofile("mysql", "mysql_host", mysql_host)
                writeprofile("mysql", "mysql_port", mysql_port)
                writeprofile("mysql", "mysql_user", mysql_user)
                writeprofile("mysql", "mysql_password", mysql_password)
                writeprofile("mysql", "mysql_database", mysql_database)
                if dbinfo():
                    respjson = {'isSuccess': True, "message": '修改成功'}
                else:
                    respjson = {'isSuccess': False, "message": "初始化数据库失败，修改后数据有问题"}
            else:
                respjson = {'isSuccess': False, "message": "初始化数据库失败，保留原有数据"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "接口测试不通过：" + str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response




class CreateFolder(APIView):
    @api_auth_post
    def post(self, request):
        try:
            src_path = request.POST.get('src_path', '')  # clientid
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            respjson = creat_folder(src_path)
            if respjson['isSuccess']:
                thr_watchdog_folder('created', src_path, '1')  # 异步调用处理数据库还有权限
        except Exception as e:
            respjson = {'isSuccess': False, "message": str(src_path) + ";文件夹新建出现错误：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'CreateFolder', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response

class DeleteFolder(APIView):
    @api_auth_post
    def post(self, request):
        try:
            src_path = request.POST.get('src_path', '')  # 路径
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            respjson = delete_folder(src_path)
            if respjson['isSuccess']:
                thr_watchdog_folder('deleted', src_path, '1')  # 异步调用处理数据库还有权限
        except Exception as e:
            respjson = {'isSuccess': False, "message": str(src_path) + ";文件夹删除错误：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'DeleteFolder', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response
    
class RenameFolder(APIView):
    @api_auth_post
    def post(self, request):
        try:
            src_path = request.POST.get('src_path', '')  # 路径
            dest_path = request.POST.get('dest_path', '') #新文件路径
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            respjson = rename_folder(src_path, dest_path)
            if respjson['isSuccess']:
                thr_watchdog_folder('moved', src_path, dest_path)  # 异步调用处理数据库还有权限
        except Exception as e:
            respjson = {'isSuccess': False, "message": str(src_path) + ";文件夹重命名错误：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'RenameFolder', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response
#根据folder_first_choice数据库对文件夹初始化，也可以重复调用（更新数据）
class FirstFolderAuthority(APIView):
    @api_auth_post
    def post(self, request):
        '''
        根据folder_first_choice数据库对文件夹初始化，也可以重复调用（更新数据）
        :param request:
        :return:
        '''
        try:
            domain = request.POST.get('domain', '')  #
            tokenid = request.POST.get('tokenid', '')  #
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            isSuccess = first_folder_authority(domain, tokenid)
            respjson = {'isSuccess': isSuccess, "message": "根据folder_first_choice数据库对文件夹初始化,也可以重复调用（更新数据）"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "根据folder_first_choice数据库对文件夹初始化错误：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'FirstFolderAuthority', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response
# 添加一层目录文件夹权限和写数据库
class Level1Folder(APIView):
    @api_auth_post
    def post(self, request):
        try:
            path = request.POST.get('path', '')  #
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            isSuccess = dfs_folder().level1_folder(path)  # 添加一层目录文件夹权限
            respjson = {'isSuccess': isSuccess, "message": "根据management_configuration数据库,添加一层目录文件夹权限和写数据库"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "根据management_configuration数据库,添加一层目录文件夹权限和写数据库,错误：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'Level1Folder', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response
    
# 添加二层目录文件夹权限和写数据库
class Level2Folder(APIView):
    @api_auth_post
    def post(self, request):
        try:
            path = request.POST.get('path', '')  #
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            isSuccess = dfs_folder().level2_folder(path)  # 添加二层目录文件夹权限和写数据库
            respjson = {'isSuccess': isSuccess, "message": "根据management_configuration数据库,添加二层目录文件夹权限和写数据库"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "根据management_configuration数据库,添加二层目录文件夹权限和写数据库,错误：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'Level2Folder', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response


# 添加二层目录文件夹权限和写数据库
class Level3Folder(APIView):
    @api_auth_post
    def post(self, request):
        try:
            path = request.POST.get('path', '')  #
            domain = request.POST.get('domain', '')  #
            tokenid = request.POST.get('tokenid', '')  #
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            isSuccess = dfs_folder().level3_folder(path, domain, tokenid)  # 添加三层目录文件夹权限和写数据库
            respjson = {'isSuccess': isSuccess, "message": "根据management_configuration数据库,添加三层目录文件夹权限和写数据库"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "根据management_configuration数据库,添加三层目录文件夹权限和写数据库：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'Level3Folder', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response


# 开始和停止 watchdog 监控文件夹变化
class WatchdogMonitor(APIView):
    @api_auth_post
    def post(self, request):
        try:
            monitor = request.POST.get('monitor', '')  #
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            thr_watchdog_start(monitor)
            if monitor =='monitor':
                respjson = {'isSuccess': True, "message": "开始 watchdog 监控文件夹变化"}
            else:
                respjson = {'isSuccess': True, "message": "停止 watchdog 监控文件夹变化"}
        except Exception as e:
            respjson = {'isSuccess': False, "message": "开始和停止 watchdog 监控文件夹变化：" + str(e)}
        try:
            insert_folder_api_log(ip, str(respjson['isSuccess']), 'WatchdogMonitor', str(request.POST), str(respjson))
        except Exception as e:
            pass
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(respjson, ensure_ascii=False))
        return response