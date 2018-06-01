# coding:utf-8
from django.conf.urls import url, include
import views


urlpatterns = [

    url(r"^register$", views.register),
    url(r"^registerhland", views.registerhland),
    url(r"^login$", views.login),
    url(r"^register_judge/", views.register_judge),
    url(r"^loginhland", views.login_hland),
    url(r"^info", views.info),
    url(r"^order$", views.user_order), # 供用户通过标题浏览到订单中心，共用一个试图所以该试图设置了默认参数，否则报错
    url(r'^order(\d+)$', views.user_order), #供切换分页时带着页码　显示的指定订单中心，默认参数１
    url(r"^site", views.site),
    url(r"^logout",views.logout)

]
