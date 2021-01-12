# 1,在服务器上使用docker安装网站<br>
docker run -dit --name  jiankong -p8888:8888 --restart always xuewenchang123/jiankong<br>
# 2，进入docker更改mysql数据库<br>
[root@a mnt]# docker exec  -it jiankong bash<br>
root@ceff2a3d8c26:/# sed -i 's/192.168.116.200/172.17.0.2/g' demo/settings.py <br>
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

# 3,http://192.168.1.200:8888/login/ 登陆网站<br>


# 4,被监控主机下载脚本<br>
wget https://raw.githubusercontent.com/xiaoxuenice/jiankong/master/client.py<br>
第三行写自己的IP地址        host='192.168.1.100'   <br>
第27行为服务器IP地址      http://192.168.1.200:8888/receive?<br>
# 5，写开机启动脚本，python3自己安装，pip安装好requests 和 psutil<br>
cat >> /etc/init.d/jiankong << EOF<br>
#!/bin/bash
#\ chkconfig: 345 85 15
python3=/usr/local/bin/python3
case $1 in
start)
nohup python3 /mnt/client.py &
;;
reload)
for i in `ps -ef |grep client.py|awk '{print $2}'`;do kill -9 $i;done
nohup python3 /mnt/client.py &
;;
stop)
for i in `ps -ef |grep client|awk '{print $2}'|sed -n '2,5p'`;do kill -9 $i;done
;;
restart)
for i in `ps -ef |grep client.py|awk '{print $2}'`;do kill -9 $i;done
nohup python3 /mnt/client.py &
;;
*)
echo "what do you want to do?"
;;
esac
EOF<br>
chmod +x /etc/init.d/jiankong<br>
chkconfig --add jiankong<br>
chkconfig jiankong on<br>

# 6，每分钟上传一次数据到监控服务器<br>
http://192.168.1.200:8888/jiankong  查看数据<br>

# 7，/目录是login后台里面创建用户，邮箱是账号，qq是密码<br>
