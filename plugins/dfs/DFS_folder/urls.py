"""DFS_folder URL Configuration

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
from django.conf.urls import url, include
from folder_api import views
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]
urlpatterns = [
    url('^docs/', include('django_api_doc.urls', namespace='接口文档')),
    url(r'^dfs_api_test/', views.dfs_api_test.as_view(), name='接口测试'),
    url(r'^dfs_api_mysqlconfig/', views.dfs_api_mysqlconfig.as_view(), name='写数据库配置'),
    url(r'^CreateFolder/', views.CreateFolder.as_view(), name='创建文件夹'),
    url(r'^DeleteFolder/', views.DeleteFolder.as_view(), name='删除文件夹'),
    url(r'^RenameFolder/', views.RenameFolder.as_view(), name='重命名文件夹'),
    url(r'^FirstFolderAuthority/', views.FirstFolderAuthority.as_view(), name='更新数据'),
    url(r'^Level1Folder/', views.Level1Folder.as_view(), name='添加一层目录文件夹权限和写数据库'),
    url(r'^Level2Folder/', views.Level2Folder.as_view(), name='添加二层目录文件夹权限和写数据库'),
    url(r'^Level3Folder/', views.Level3Folder.as_view(), name='添加三层目录文件夹权限和写数据库'),
    url(r'^WatchdogMonitor/', views.WatchdogMonitor.as_view(), name='开始和停止watchdog监控文件夹变化'),
]