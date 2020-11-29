from django.contrib import admin
from django.urls import path
from blog.views import *
urlpatterns = [
    path("",index),
    path("user/",index1),
    path('admin/', admin.site.urls),
    path("and/",add1),
    path("add/",add1),
    path("a/",indexa),
    path("login/",login),
    path("logout/",logout),
    path("404/",error),
    path("jiankong/",jiankong),
    path("receive/",receive),
]
