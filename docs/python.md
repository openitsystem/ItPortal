

## 部署

### 01.centos安装python3
##### 001.建议停用防火墙
```
systemctl  stop firewalld  (停用防火墙）
```
##### 002.安装依赖关系：(先更新下yum)
```
yum update
yum groupinstall 'Development Tools'
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
yum install zlib-devel bzip2-devel openssl-devel ncurese-devel
```
##### 003.下载安装包
- [在python官网下载](https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz.asc)
- [在百度云下载](https://pan.baidu.com/s/10575Yr1FA8EE6lDYMpDqRw) 密码：k73z
##### 004.解压文件并安装
```
tar -xf Python-3.5.2.tgz
#解压之后有一个目录Python-3.5.2，进入目录
cd Python-3.5.2
#开始安装，使用编译的方法进行安装
#在python的目录中有一个README文件，他介绍了如何安装python。 但是我们要指定这个安装目录

mkdir /usr/python35
./configure --prefix=/usr/python35
make
make install


#说明./configure命令执行完毕之后创建一个文件creating Makefile，供下面的make命令使用 执行make install之后就会把程序安装到我们指定的目录中去
```
##### 005.给python 3.52 安装我们需要的pip 包
- 先看下默认的python 版本
```
python
```
![python版本](/Users/haifeng/opensource/ITPortal/docs/imgs/python/01.python2.7.png)
```
exit() #退出
/usr/python35/bin/python3.5  #python3.5
```
![python3.5版本](/Users/haifeng/opensource/ITPortal/docs/imgs/python/02.python3.5.png)
```
exit() #退出
/usr/python35/bin/python3.5 -m pip list #查看已安装的包
```
![pip_list](/Users/haifeng/opensource/ITPortal/docs/imgs/python/03.python3.5piplist.png)


##### 006.下面开始用 pip 安装运行程序必须的包
```
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pip==9.0.1

/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple appdirs==1.4.3
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple APScheduler==2.1.2
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple cached-property==1.3.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple DBUtils==1.3
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple defusedxml==0.5.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple Django==1.10
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple django-pipeline==1.6.13
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple et-xmlfile==1.0.1
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple futures==3.1.1
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple ipaddress==1.0.17
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple IPy==0.83
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple isodate==0.5.4
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple jdcal==1.4
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple lxml==3.8.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple openpyxl==2.5.0

/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple ply==3.9
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pyasn1==0.1.9
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pycrypto==2.6.1
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pymssql==2.1.3
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple PyMySQL==0.7.9
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pypinyin==0.33.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pysmi==0.0.7
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pysnmp==4.3.2
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple pytz==2017.2
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple requests==2.12.4
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple requests-toolbelt==0.8.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple setuptools==20.10.1
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple six==1.10.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple urllib3==1.23
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple uWSGI==2.0.13.1
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple wakeonlan==0.2.2
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple xlrd==1.0.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple XlsxWriter==1.0.5
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple xlwt==1.3.0
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple zeep==1.2.0
```
- 安装完成后,再看下
```
/usr/python35/bin/python3.5 -m pip list
```

##### 007.把运行程序拷贝到指定目录(xftp5)
```
cd /    #进入根目录
mkdir www    # 新建一个www的文件夹
cd /www     # 进入这个文件夹
```
###### 打开 xftp 5
![打开 xftp 5](/Users/haifeng/opensource/ITPortal/docs/imgs/python/04.xftp5.png)
###### 找到新建的文件夹
![找到新建的文件夹](/Users/haifeng/opensource/ITPortal/docs/imgs/python/05.xftp5.png)

![移动到系统](/Users/haifeng/opensource/ITPortal/docs/imgs/python/06.xftp5.png)


##### 008.安装nginx
```
yum install nginx  #安装nginx
systemctl status nginx   #查看 nginx 是否启用
```
![nginx](/Users/haifeng/opensource/ITPortal/docs/imgs/python/07.nginx.png)

```
systemctl start nginx   #开启
systemctl stop nginx   #关闭
systemctl restart nginx  #重启

#修改nginx 配置
cd /etc/nginx
```
![nginx](/Users/haifeng/opensource/ITPortal/docs/imgs/python/08.xftp.png)
```
# nginx.conf  是配置文件，修改前，请先备份
#主要配置说明
server {
        listen       80 default_server;    # 我要监听那个端口
        listen       [::]:80 default_server;
        server_name  127.0.0.1;   # 服务器IP  # 你访问的路径前面的url名称 
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;
		# 指定项目路径uwsgi
        location / {
			proxy_pass   http://127.0.0.1:8001/;   #用来和uWSGI进行通讯的
           proxy_set_header  HTTP_X_REAL_IP  $http_RealIP;
           proxy_set_header  Host  $host;
           proxy_set_header HTTP_X_FORWARDED_FOR $http_RealIP;
        }
		# 指定静态文件路径
		location /static {
            alias /www/open_itportal/static;
        }
        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
}


#文件配置好，并保存，上传

systemctl restart nginx  #重启nginx

```
##### 009.后台运行uwsgi
```
#注意保存log 文件路径,log 可能会满
# /var/log/uwsgi.log  #log目录
# 启用uwsgi
/usr/python35/bin/uwsgi --http-socket 0.0.0.0:8001 --chdir /www/open_itportal/ --plugin /usr/python35/bin/python3.5 --wsgi-file /www/open_itportal/itportal/wsgi.py --master --processes 2 --threads 2 --threads 2 --daemonize /var/log/uwsgi.log


#关闭uwsgi
pkill -9 uwsgi #关闭uwsgi
```
![uwsgi](/Users/haifeng/opensource/ITPortal/docs/imgs/python/09.python_uwsgi.png)

##### 010.参考文档
- [Django Nginx+uwsgi 安装配置](http://www.runoob.com/django/django-nginx-uwsgi.html)
- [Django + Uwsgi + Nginx 的生产环境部署](https://www.cnblogs.com/chenice/p/6921727.html)
- [uWSGI官方文档](https://uwsgi-docs.readthedocs.io/en/latest/index.html)
- [uWSGI配置文档翻译](http://www.cnblogs.com/zhouej/archive/2012/03/25/2379646.html) 
