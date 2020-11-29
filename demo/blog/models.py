from django.db import models
class Author(models.Model):
    name = models.CharField(max_length=50,verbose_name="名字")
    qq = models.CharField(max_length=10)
    addr = models.TextField(verbose_name="地址")
    email = models.EmailField()
    class Meta:
      verbose_name = '作者'
      verbose_name_plural = '作者'
 
    def __str__(self):
        return self.name
 
 
class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name="标题")
    author = models.ForeignKey(Author, on_delete=models.CASCADE,verbose_name="作者") #引用时候以1,2,3代表
    content = models.TextField(verbose_name="内容")
    score = models.IntegerField(verbose_name="打分")  # 文章的打分
    tags = models.ManyToManyField('Tag',verbose_name="标记")
    class Meta:
       verbose_name = '文章'
       verbose_name_plural = '文章'
 
    def __str__(self):
        return self.title
 
 
class Tag(models.Model):
    name = models.CharField(max_length=50,verbose_name="名称")
    class Meta:
        verbose_name = '标记'
        verbose_name_plural = '标记'
 
    def __str__(self):
        return self.name
class Hostnamea(models.Model):
    hostname = models.CharField(max_length=50,verbose_name="hostname")
    class Meta:
      verbose_name = '监控主机ip'
      verbose_name_plural = '监控主机ip'

    def __str__(self):
        return self.hostname
class Host(models.Model):
    host = models.ForeignKey(Hostnamea, on_delete=models.CASCADE,verbose_name="主机") #引用时候以1,2,3代表
    time = models.TextField(verbose_name="time")
    qdsj = models.TextField(verbose_name="启动时间")
    cpuhs = models.TextField(verbose_name="cpu核数")
    cpulv = models.TextField(verbose_name="cpu利率")
    ncdx = models.TextField(verbose_name="内存大小")
    nclv = models.TextField(verbose_name="内存利率")
    cpdx = models.TextField(verbose_name="磁盘大小")
    cpsy = models.TextField(verbose_name="磁盘剩余")
    wkjs = models.TextField(verbose_name="网卡接收")
    wkfs = models.TextField(verbose_name="网卡发送")
    ljs = models.TextField(verbose_name="连接数")
    jcs = models.TextField(verbose_name="进程数")
    class Meta:
       verbose_name = '监控日志'
       verbose_name_plural = '监控日志'

    def __str__(self):
        return str(self.host)



