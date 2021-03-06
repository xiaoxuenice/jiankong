# jiankong可能需要安装模块 cryptography
# 1,在服务器上使用docker安装网站<br>
docker run -dit --name  jiankong -p8888:8888 --restart always xuewenchang123/jiankong<br>
# 安装数据库<br>
docker run -dit --name mysql8.0  -p3306:3306 -e MYSQL_ROOT_PASSWORD=Pwd@123456 library/mysql<br>
create database python01;<br>
create user root identified by 'Pwd@123456';<br>
grant all privileges on python01.* to 'root'@'%';<br>
# 2，进入docker更改mysql数据库<br>
[root@a mnt]# docker exec  -it jiankong bash<br>
root@ceff2a3d8c26:/# sed -i 's/172.17.0.2/192.168.1.200/g' demo/settings.py <br>
root@ceff2a3d8c26:/# sed -i 's/python/python01/g' demo/settings.py <br>
root@ceff2a3d8c26:/# cat demo/settings.py <br>
        'ENGINE': 'django.db.backends.mysql',<br>
        'NAME': 'python01',<br>
        'USER': 'root',<br>
        'PASSWORD':'Pwd@123456',<br>
        'HOST':'172.17.0.2',<br>
        'PORT':'3306',<br>
root@ceff2a3d8c26:/# exit<br>
[root@a mnt]# docker restart jiankong<br>
[root@a mnt]# docker exec  -it jiankong bash<br>
root@ceff2a3d8c26:/# python3 manage.py makemigrations<br>
root@ceff2a3d8c26:/# python3 manage.py migrate<br>
root@ceff2a3d8c26:/# python3 manage.py createsuperuser  
后台用户名密码设置为 admin<br>

# 3,http://192.168.1.200:8888/admin/ 登陆网站<br>



# 4,被监控主机下载脚本<br>
wget https://raw.githubusercontent.com/xiaoxuenice/jiankong/master/client.py<br>
第三行写自己的IP地址        host='192.168.1.100'   <br>
第27行为服务器IP地址      http://192.168.1.200:8888/receive?<br>
# 5，写开机启动脚本，python3自己安装，pip安装好requests 和 psutil<br>
cat >> /etc/init.d/jiankong << EOF<br>
#!/bin/bash<br>
#\ chkconfig: 345 85 15<br>
python3=/usr/local/bin/python3<br>
case $1 in<br>
start)<br>
nohup $python3 /mnt/client.py &<br>
;;<br>
reload)<br>
for i in `ps -ef |grep client.py|awk '{print $2}'`;do kill -9 $i;done<br>
nohup $python3 /mnt/client.py &<br>
;;<br>
stop)<br>
for i in `ps -ef |grep client|awk '{print $2}'`;do kill -9 $i;done<br>
;;<br>
restart)<br>
for i in `ps -ef |grep client.py|awk '{print $2}'`;do kill -9 $i;done<br>
nohup $python3 /mnt/client.py &<br>
;;<br>
*)<br>
echo "what do you want to do?"<br>
;;<br>
esac<br>
EOF<br>
chmod +x /etc/init.d/jiankong<br>
chkconfig --add jiankong<br>
chkconfig jiankong on<br>

# 6，每分钟上传一次数据到监控服务器<br>
http://192.168.1.200:8888/jiankong  查看数据<br>
# 7，/目录是login后台里面创建用户，邮箱是账号，qq是密码<br>

