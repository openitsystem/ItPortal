#DFS操作接口
此接口适用于所有widnows文件共享类操作

## 安装部署 API
### third-party dfs部署说明
#### 0.部署服务器要求
1. windows服务器具有所有文件权限（可以直接是文件服务器）
2. .NetFrameWork 版本4.6

#### 1.windows安装python3.5.2 和 pip安装必要包
- [python官网_python-3.5.2-amd64.exe](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe)

- [百度云盘_python-3.5.2-amd64.exe](https://pan.baidu.com/s/1HlHEKDeCLs2JqKd2aFjHZg)    密码 :9mk4

- 复制到服务器——管理员身份运行——勾选Add python 3.5 to PATH —— 安装


- 安装完成后
```
Microsoft Windows [版本 6.1.7601]
版权所有 (c) 2009 Microsoft Corporation。保留所有权利。

C:\Users\administrator>python  # 查看安装的python 版本
Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AM
D64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>

>>> exit()  #退出

C:\Users\administrator>pip list   #查看已安装的pip 包
pip (8.1.1)
setuptools (20.10.1)
You are using pip version 8.1.1, however version 18.0 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' comm
and.

```
- 在cmd 里面运行下面命令
```
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pip==9.0.1

pip install -i https://pypi.mirrors.ustc.edu.cn/simple altgraph==0.16.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple APScheduler==3.5.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple argh==0.26.2
pip install -i https://pypi.mirrors.ustc.edu.cn/simple asn1crypto==0.24.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple backports.functools-lru-cache==1.5
pip install -i https://pypi.mirrors.ustc.edu.cn/simple certifi==2018.4.16
pip install -i https://pypi.mirrors.ustc.edu.cn/simple cffi==1.11.5
pip install -i https://pypi.mirrors.ustc.edu.cn/simple chardet==3.0.4
pip install -i https://pypi.mirrors.ustc.edu.cn/simple cheroot==6.3.3
pip install -i https://pypi.mirrors.ustc.edu.cn/simple CherryPy==16.0.3
pip install -i https://pypi.mirrors.ustc.edu.cn/simple cryptography==2.2.2
pip install -i https://pypi.mirrors.ustc.edu.cn/simple Django==1.10.5
pip install -i https://pypi.mirrors.ustc.edu.cn/simple django-api-doc==0.4
pip install -i https://pypi.mirrors.ustc.edu.cn/simple django-api-docs==1.1.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple django-filter==1.1.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple django-windows-tools==0.2.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple djangorestframework==3.7.7
pip install -i https://pypi.mirrors.ustc.edu.cn/simple future==0.16.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple idna==2.7
pip install -i https://pypi.mirrors.ustc.edu.cn/simple jaraco.functools==1.20
pip install -i https://pypi.mirrors.ustc.edu.cn/simple macholib==1.10
pip install -i https://pypi.mirrors.ustc.edu.cn/simple Markdown==2.6.11
pip install -i https://pypi.mirrors.ustc.edu.cn/simple more-itertools==4.2.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pathtools==0.1.2
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pefile==2018.8.8
pip install -i https://pypi.mirrors.ustc.edu.cn/simple portend==2.3
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pycparser==2.18
pip install -i https://pypi.mirrors.ustc.edu.cn/simple PyInstaller==3.3.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple PyMySQL==0.9.2
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pypinyin==0.31.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pypiwin32==223
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pytz==2018.5
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pywin32==223
pip install -i https://pypi.mirrors.ustc.edu.cn/simple PyYAML==3.13
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pyzmq==17.0.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple requests==2.19.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple setuptools==20.10.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple six==1.11.0
pip install -i https://pypi.mirrors.ustc.edu.cn/simple tempora==1.12
pip install -i https://pypi.mirrors.ustc.edu.cn/simple tzlocal==1.5.1
pip install -i https://pypi.mirrors.ustc.edu.cn/simple urllib3==1.23
pip install -i https://pypi.mirrors.ustc.edu.cn/simple watchdog==0.8.3
pip install -i https://pypi.mirrors.ustc.edu.cn/simple WMI==1.4.9
pip install -i https://pypi.mirrors.ustc.edu.cn/simple pycrypto==2.6.1

```
- 如果安装pycrypto出现,参考最后面的PS(补充)
```
    running build_ext
    warning: GMP or MPIR library not found; Not building Crypto.PublicKey._fastm
ath.
    building 'Crypto.Random.OSRNG.winrandom' extension
    error: Unable to find vcvarsall.bat   #主要是这个
```
#### 2.把程序文件拷贝到服务器并运行 文件位置(E:\625\DFS_dacl\DFS_folder)
#### 运行成功生成的就是 http://服务器IP:8081/ 这个是dfs_api
```
C:\Windows\system32>e:  #进入E盘

E:\>cd E:\625\DFS_dacl\DFS_folder  #进入文件路径

E:\625\DFS_dacl\DFS_folder>dir   #查看当前文件，确定manage.py
 驱动器 E 中的卷是 新加卷
 卷的序列号是 0423-E6AF

 E:\625\DFS_dacl\DFS_folder 的目录

2018/08/29  12:17    <DIR>          .
2018/08/29  12:17    <DIR>          ..
2018/08/29  12:17    <DIR>          .idea
2018/08/29  12:17    <DIR>          apidoc
2018/08/23  15:58             3,072 db.sqlite3
2018/08/29  12:17    <DIR>          DFS_folder
2018/08/29  12:17    <DIR>          folder_api
2018/08/23  15:58               830 manage.py
2018/08/29  12:17    <DIR>          monitor_file
2018/08/29  12:17    <DIR>          templates
               2 个文件          3,902 字节
               8 个目录 213,984,346,112 可用字节

E:\625\DFS_dacl\DFS_folder>python manage.py runserver 0.0.0.0:8081  #执行命令，指定端口
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you
 apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
August 29, 2018 - 17:10:57
Django version 1.10.5, using settings 'DFS_folder.settings'
Starting development server at http://0.0.0.0:8081/
Quit the server with CTRL-BREAK.
[29/Aug/2018 17:20:13] "POST /dfs_api_mysqlconfig/ HTTP/1.1" 200 46

```

#### PS (安装pycrypto 失败)
- [Windows下安装Python扩展模块提示“Unable to find vcvarsall.bat”的问题](https://www.cnblogs.com/yyds/p/7065637.html)
- [error: Unable to find vcvarsall.bat解决办法](https://blog.csdn.net/a6822342/article/details/80841056)
- 这边采用安装 vs 2015 解决这个问题
- 找一个vs2015 安装包
- 自定义功能——编程语言——勾选   适用VisualC++2015的公共工具 ——勾选 Python Tools for Visual Studio  ——其他不需要——安装

TODO