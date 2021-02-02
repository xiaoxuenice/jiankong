import psutil,time,requests
from collections import Counter
host='192.168.116.200'   #自己ip地址
while True:
 time.sleep(45)
 qdsj=str(time.strftime("%Y-%m-%d %H:%M:%W",time.localtime(psutil.boot_time())))
 cpuhs=str(psutil.cpu_count())
 cpulv=str(psutil.cpu_percent(interval=5))+"%"
 ncdx=str(int(psutil.virtual_memory().total / 1000000))+"M"
 nclv=str(int(psutil.virtual_memory().used / psutil.virtual_memory().total *100))+"%"
 cpdx=str(int(psutil.disk_usage('/').total / 1000000000))+"G"            
 cpsy=str(int(psutil.disk_usage('/').free / 1000000000))+"G"
 wkjs=str(int(psutil.net_io_counters().bytes_sent / 1000000))+'M'
 wkfs=str(int(psutil.net_io_counters().bytes_recv / 1000000))+'M'
 ip=[]
 ljs=0
 jcs=''
 for i in psutil.net_connections():
     if i.laddr.ip not in  '::1 0.0.0.0 ::127.0.0.1' and i.status == "ESTABLISHED":
        ip.append(i.raddr.ip)
 for i in Counter(ip).most_common():    #显示前20个
     ljs+=int(i[1])
 for i in psutil.process_iter():
     if i.status() == "running":
            jcs+=str(i.name())+" "
 ti=time.strftime("%Y-%m-%d %H:%M:%W",time.localtime(time.time()))
 try:
    a=requests.get("http://xiaoxue.com/receive?host={}&qdsj={}&cpuhs={}&cpulv={}&ncdx={}&nclv={}&cpdx={}&cpsy={}&wkjs={}&wkfs={}&ljs={}&jcs={}".format(host,qdsj,cpuhs,cpulv,ncdx,nclv,cpdx,cpsy,wkjs,wkfs,ljs,jcs)).content   #xiaoxue改为监控主机的IP地址
    with open("jiankong.log",'a+') as f :
       f.write(a.decode()+ti+"\n")
 except Exception as f:
   f.write(f+ti+"\n")
