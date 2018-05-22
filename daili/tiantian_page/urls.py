#coding:utf-8
from django.conf.urls import url

import views

urlpatterns = [
    url(r"^$",views.Index),
    url(r'^index.html$', views.Index),
    url(r'^list(\d+)_(\d+)_(\d+)', views.list),
    url(r'^(\d+)/$', views.detail)
]
