#!/bin/bash
# jiankong可能需要安装模块 cryptography
# 1,在服务器上使用docker安装网站
docker run -dit --name  jiankong -p8888:8888 --restart always xuewenchang123/jiankong
# 安装数据库
docker run -dit --name mysql8.0  -p3306:3306 -e MYSQL_ROOT_PASSWORD=Pwd@123456 library/mysql
create database python01;
create user root identified by 'Pwd@123456';
grant all privileges on python01.* to 'root'@'%';
# 2，进入docker更改mysql数据库<br>
[root@a mnt]# docker exec  -it jiankong bash
root@ceff2a3d8c26:/# pip install cryptography
root@ceff2a3d8c26:/# sed -i 's/172.17.0.2/192.168.1.200/g' demo/settings.py 
root@ceff2a3d8c26:/# sed -i 's/python/python01/g' demo/settings.py 
root@ceff2a3d8c26:/# cat demo/settings.py 
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python01',
        'USER': 'root',
        'PASSWORD':'Pwd@123456',
        'HOST':'172.17.0.2',
        'PORT':'3306',
root@ceff2a3d8c26:/# exit
[root@a mnt]# docker restart jiankong
[root@a mnt]# docker exec  -it jiankong bash
root@ceff2a3d8c26:/# python3 manage.py makemigrations
root@ceff2a3d8c26:/# python3 manage.py migrate
root@ceff2a3d8c26:/# python3 manage.py createsuperuser  
后台用户名密码设置为 admin

# 3,http://192.168.1.200:8888/admin/ 登陆网站



# 4,被监控主机下载脚本<br>
wget https://raw.githubusercontent.com/xiaoxuenice/jiankong/master/client.py
第三行写自己的IP地址        host='192.168.1.100'   
第27行为服务器IP地址      http://192.168.1.200:8888/recive?
# 5，写开机启动脚本，python3自己安装，pip安装好requests 和 psutil
cat >> /etc/init.d/jiankong << EOF
#!/bin/bash
# chkconfig: 345 85 15
python3=/usr/local/bin/python3
case $1 in
start)
nohup $python3 /mnt/client.py &
;;
reload)
for i in `ps -ef |grep client.py|awk '{print $2}'`;do kill -9 $i;done
nohup $python3 /mnt/client.py &
;;
stop)
for i in `ps -ef |grep client|awk '{print $2}'`;do kill -9 $i;done
;;
restart)
for i in `ps -ef |grep client.py|awk '{print $2}'`;do kill -9 $i;done
nohup $python3 /mnt/client.py &
;;
*)
echo "what do you want to do?"
;;
esac
EOF
chmod +x /etc/init.d/jiankong
chkconfig --add jiankong
chkconfig jiankong on

# 6，每分钟上传一次数据到监控服务器
http://192.168.1.200:8888/jiankong  查看数据
# 7，/目录是login后台里面创建用户，邮箱是账号，qq是密码

