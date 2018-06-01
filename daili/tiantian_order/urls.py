# coding:utf-8
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^order',views.order),  # 屁股后面会跟ｇｅｔ传参所以不加$
    url(r'^hadler$',views.order_hadler),
    url(r'^pay(\d+)', views.pay)

]
