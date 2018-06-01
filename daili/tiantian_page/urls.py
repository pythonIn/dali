#coding:utf-8
from django.conf.urls import url

import views#　函数进入
from views import *#　为了进入试图类

urlpatterns = [
    url(r"^$",views.Index),
    url(r'^index.html$', views.Index),
    url(r'^list(\d+)_(\d+)_(\d+)', views.list),
    url(r'^(\d+)/$', views.detail),

    url(r'^search/', MySeachView())  # 因为是进入到类　所以不要加views,此试图额外增加ｈａｙｓｔａｃｋ上下文
]
