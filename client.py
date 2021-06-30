import psutil,time,requests,telegram
from collections import Counter
host='自己ip地址'  
while True:
 try:
   time.sleep(30)
   qdsj=str(time.strftime("%Y-%m-%d %H:%M:%W",time.localtime(psutil.boot_time())))
   cpuhs=str(psutil.cpu_count())
   cpulv=str(psutil.cpu_percent(interval=5))+"%"
   ncdx=str(int(psutil.virtual_memory().total / 1000000))+"M"
   nclv=str(int(psutil.virtual_memory().used / psutil.virtual_memory().total *100))+"%"
   cpdx=str(int(psutil.disk_usage('/').total / 1000000000))+"G"            
   cpsy=str(int(psutil.disk_usage('/').free / 1000000000))+"G"
   wkjs=str(int(psutil.net_io_counters().bytes_sent / 1000000))+'M'
   wkfs=str(int(psutil.net_io_counters().bytes_recv / 1000000))+'M'
   if 'nginx' not in [ psutil.Process(i).name() for i in psutil.pids() ]:
      bot=telegram.Bot(token="1847399485:AAHnPB_tJYzsRe6Ljpw2EFTFLcbWySjpdco")
      bot.send_message(chat_id='@jiqiren1211',text='自己IP地址 nginx done!!')
   ip=[]
   ljs=0
   jcs=0
   for i in psutil.net_connections():
       if i.laddr.ip not in  '::1 0.0.0.0 ::127.0.0.1' and i.status == "ESTABLISHED":
          ip.append(i.raddr.ip)
   for i in Counter(ip).most_common():    #显示前20个
       ljs+=int(i[1])
   for i in psutil.process_iter():
       jcs+=1
   a=requests.get("http://服务器端:8888/receive?host={}&qdsj={}&cpuhs={}&cpulv={}&ncdx={}&nclv={}&cpdx={}&cpsy={}&wkjs={}&wkfs={}&ljs={}&jcs={}".format(host,qdsj,cpuhs,cpulv,ncdx,nclv,cpdx,cpsy,wkjs,wkfs,ljs,jcs)).content   #xiaoxue改为监控主机的IP地址
 except Exception as f:
     with open("jiankong.log",'a+') as f :
       f.write(a.decode()+"\n")
