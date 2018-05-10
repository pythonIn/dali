# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse

from models import *

from hashlib import sha1


def register(request):
    return render(request, "tiantian/register.html")

def registerhland(request):
    post = request.POST
    user1 = post.get('user_name')
    password = post.get('pwd')
    password1 = post.get('cpwd')
    email = post.get('email')

    if password != password1:
        return redirect("/user/register")
    s1 = sha1()
    s1.update(password)
    pwd = s1.hexdigest()
    user = UserInfo()
    user.u_name = user1
    user.u_pwd = pwd
    user.u_email = email
    user.save()
    return redirect("/user/login")

def register_judge(request):
    get = request.GET
    judge = get.get('user_name')
    count = UserInfo.objects.filter(u_name=judge).count()
    return JsonResponse({'list':count})

def login(request):
    return render(request, "tiantian/login.html")


