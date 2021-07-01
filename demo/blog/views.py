from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
import time,telegram
from blog.models import *
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AddForm
def error(request):
       return  HttpResponse(str("别瞎研究，你看不懂"))
def add1(request):
        a = request.GET['a']
        b = request.GET['b']
        c = int(a)+int(b)
        return HttpResponse(str(c))
@cache_page(60 * 2)
def index(request):
	if request.session.get("login",None):
		a=Article.objects.values("title").count()
		if a>20:
			aa=Article.objects.all().prefetch_related("author").order_by("-id")[:6]
		else:
			aa=Article.objects.all().prefetch_related("author").order_by("-id")[:a]
		wz=[]
		n=0
		for i in aa:
			wz.append({})
			wz[n]['zz']=i.author.name
			wz[n]['bt']=i.title
			wz[n]['wza']=i.content[0:45]
			wz[n]['core']=i.score
			wz[n]['id']=i.id
			try:
				wz[n]['tags']=i.tags.all()[0]
			except Exception as f:
				wz[n]['tags']='好心情'
			n+=1
		string = time.strftime("%Y-%m-%d %H:%M",time.localtime(time.time()))
		return  render(request,'index.html',{'string': string,"a":a,'wz':wz,'name':request.session['name']})
	else:
		return HttpResponseRedirect("/login/")

@cache_page(60 * 2)
def index1(request):
	if request.session.get("login",None):
		ido = request.GET['id']
		sc=Article.objects.filter(id=ido)[0].score+1
		c=Article.objects.filter(id=ido)
		c.update(score=sc)
		a=Article.objects.get(id=ido)
		imageid=Article.objects.get(id=ido).image
		images=[i.image.name for i  in Images.objects.filter(image__contains=imageid)]
		wz={"zz":a.author.name,"bt":a.title,"wza":a.content,"core":a.score,"tags":a.tags.all()[0]}
		string = time.strftime("%Y-%m-%d %H:%M",time.localtime(time.time()))
		return  render(request,'home.html',{'string': string,'wz':wz,'name':request.session['name'],'images':images})
	else:
		return HttpResponseRedirect("/login/")
def indexa(request):
        List= ['a','b','c','','d']
        Dict={"one":'it one','two':'it two'}
        return render(request,'a.html',{'List': List,'var':100,'test': 'it test',"Dict":Dict})

@csrf_exempt
def login(request):
	if request.method == 'POST':
		try:
			m= Author.objects.get(email=request.POST['username'])
			if str(m.qq) == str(request.POST['password']):
				request.session['name']=m.name
				request.session['login']=True
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/login/")
		except  Exception as f:
				return HttpResponseRedirect("/login/")
	return render(request,'login.html')
def logout(request):
	cache._cache.flush_all()
	request.session.flush()
	return HttpResponseRedirect("/login/")
def receive(request):
	if  time.strftime("%Y%m%d%H%M",time.localtime(time.time()))[10:12] == '00':
				sj=int(time.strftime("%Y%m%d%H%M",time.localtime(time.time())))-41
	else:
				sj=int(time.strftime("%Y%m%d%H%M",time.localtime(time.time())))-1
	host=request.GET['host']
	qdsj=request.GET['qdsj']
	cpuhs=request.GET['cpuhs']
	cpulv=request.GET['cpulv']
	ncdx=request.GET['ncdx']
	nclv=request.GET['nclv']
	cpdx=request.GET['cpdx']
	cpsy=request.GET['cpsy']
	wkjs=request.GET['wkjs']
	wkfs=request.GET['wkfs']
	ljs=request.GET['ljs']
	jcs=request.GET['jcs']
	timeo=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
	de=int(time.strftime("%Y%m%d",time.localtime(time.time())))-1
	zhuji=[] #获取id
	qbzj=[]
	a=Hostnamea.objects.all().prefetch_related()
	for i in a:
		zhuji.append(i.id)
	for i in zhuji:
		try:
			Host.objects.all().prefetch_related('host').filter(time__contains=str(sj)).order_by('-time').filter(host_id=i)[0]
		except Exception as f:
			qbzj.append(Hostnamea.objects.get(id=i).hostname)
	if '1200' == time.strftime("%H%M",time.localtime(time.time())) or '1201' == time.strftime("%H%M",time.localtime(time.time())): #每天12点删除前一天监控日志
		Host.objects.filter(time__contains=str(de)).delete()
	try:
		hostid=Hostnamea.objects.get(hostname=host).id
	except Exception as f:
		Hostnamea.objects.create(hostname=host)
		hostid=Hostnamea.objects.get(hostname=host).id
	Host.objects.create(time=timeo,host_id=hostid,qdsj=qdsj,cpuhs=cpuhs,cpulv=cpulv,cpsy=cpsy,ncdx=ncdx,nclv=nclv,cpdx=cpdx,wkjs=wkjs,wkfs=wkfs,ljs=ljs,jcs=jcs)
	for i in qbzj:
				bot=telegram.Bot(token="1847399485:AAHnPB_tJYzsRe6Ljpw2EFTFLcbWySjpdco")
				bot.send_message(chat_id='@jiqiren1211',text='{} 主机监控不到！！'.format(i))
	return HttpResponse("ok")
def jiankong(request):
	if  time.strftime("%Y%m%d%H%M",time.localtime(time.time()))[10:12] == '00':
				sj=int(time.strftime("%Y%m%d%H%M",time.localtime(time.time())))-41
	else:
				sj=int(time.strftime("%Y%m%d%H%M",time.localtime(time.time())))-1
	sjnow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	zhuji=[] #获取id
	qbzj=[]	#全部主机
	a=Hostnamea.objects.all().prefetch_related()
	for i in a:
		zhuji.append(i.id)
		qbzj.append(i.hostname)
	xx=[]
	hqbd=[]	#获取不到
	n=0
	chzj=[]
	for i in zhuji:
			try:
				aa=Host.objects.all().prefetch_related('host').filter(time__contains=str(sj)).order_by('-time').filter(host_id=i)[0]
			except Exception as f:
				hqbd.append(Hostnamea.objects.get(id=i).hostname)
				continue
			xx.append({})
			xx[n]['host']=aa.host.hostname
			chzj.append(str(aa.host.hostname))
			xx[n]['qdsj']=aa.qdsj
			xx[n]['hqsj']=aa.time[0:4]+"-"+aa.time[4:6]+"-"+aa.time[6:8]+" "+aa.time[8:10]+":"+aa.time[10:12]+":"+aa.time[12:14]
			xx[n]['cpuhs']=aa.cpuhs
			xx[n]['cpulv']=aa.cpulv
			xx[n]['ncdx']=aa.ncdx
			xx[n]['nclv']=aa.nclv
			xx[n]['cpdx']=aa.cpdx
			xx[n]['cpsy']=aa.cpsy
			xx[n]['wkjs']=aa.wkjs
			xx[n]['wkfs']=aa.wkfs
			xx[n]['ljs']=aa.ljs
			xx[n]['jcs']=aa.jcs
			n+=1
	return  render(request,'jiankong.html',{'xx':xx,'sjnow':sjnow,'hqbd':hqbd,'qbzj':qbzj})
