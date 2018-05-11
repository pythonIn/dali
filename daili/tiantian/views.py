# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse,HttpResponseRedirect

from models import *

from hashlib import sha1

# 显示注册页面
def register(request):
    return render(request, "tiantian/register.html")

# 接收用户输入
def registerhland(request):
    post = request.POST
    user1 = post.get('user_name')
    password = post.get('pwd')
    password1 = post.get('cpwd')
    email = post.get('email')
# 判断两次密码
    if password != password1:
        return redirect("/user/register")
    # 密码加密
    s1 = sha1()
    s1.update(password)
    pwd = s1.hexdigest()
    # 创建对象，写入到数据库
    user = UserInfo()
    user.u_name = user1
    user.u_pwd = pwd
    user.u_email = email
    user.save()
    # 重定向到登入页面
    return redirect("/user/login")

    # 接收js的get请求，判断是否用户名存在
def register_judge(request):
    get = request.GET
    judge = get.get('user_name')
    count = UserInfo.objects.filter(u_name=judge).count()
    return JsonResponse({'list':count})

# 登入页面，获取cookie，如果有就显示cookie保存的用户名，没有显示""
def login(request):
    uname = request.COOKIES.get('uname', "")
    context ={'title':'用户登陆','error_name':0,'error_pwd':0,'uname':uname}
    return render(request, "tiantian/login.html",context)

def login_hland(request):
    # 接收表单请求信息
    post = request.POST
    name = post.get("username")
    pwd1 = post.get('pwd')
    jizhu = post.get('jizhu',0)
    # 根据用户名查询数据库是否存在
    get_name = UserInfo.objects.filter(u_name=name)
    # 如果未查到则用户名错，如果查到则判断密码是否正确，正确转入用户中心
    if len(get_name)==1:
        s1 = sha1()
        s1.update(pwd1)
        pwd = s1.hexdigest()
        # 判断密码是否正确， 正确发送重定向转向用户中心，并设置cookie 与 session
        if get_name[0].u_pwd == pwd:
            red = HttpResponseRedirect('/user/info') # 转向，并让red成为response对象，调用cookie方法发送cookie
            if jizhu!=0: # 如果不等于0 就说明点击了记住用户名，向转向的user/info发送cookie，浏览器保存cookie
                red.set_cookie('uname',name) # 设置cookie
                # 设置cookie为 空 立马过期，

            else:
                red.set_cookie("unmae","",max_age=-1)

            # 存入到django默认服务端session中用于个人中心显示
            #request.session['user_id'] = get_name[0].id # 存入当前用户的id用于个人中心显示
            #request.session['user_name'] = get_name # session也是一个类字典的类型，通过user_name键获取值
            return red # 返回设置的cookie,return给当前表单所属浏览器。

        # 如果密码不正确，上下文提交至页面，js判断写入出错为密码 重新渲染页面，显示之前输入的错误的账户与密码
        else:
            context ={'title':'用户登陆','error_name':0,'error_pwd':1,'uname':name,'upwd':pwd1}
            return render(request, 'tiantian/login.html', context)

    else:
        context = {'title':'用户登陆','error_name':1,'error_pwd':0,'uname':name,'upwd':pwd1}
        return render(request, 'tiantian/login.html', context)


# 用户中心，个人信息
def info(request):
    return render(request,'tiantian/user_center_info.html')
# 订单
def order(request):
    return render(request, 'tiantian/user_center_order.html')
# 收货地址
def site(requst):
    return render(requst, 'tiantian/user_center_site.html')