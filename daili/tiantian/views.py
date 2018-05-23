# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse,HttpResponseRedirect

from models import *

from hashlib import sha1

import user_decorator

from tiantian_page.models import *

from tiantian_cart.models import * # 导入购物车数据库　进行查询购物车信息

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
            # 判断cookie中url键是否保存指定的转向地址，如果没有，默认为user/info页面,
            url = request.COOKIES.get('url','/user/info')
            red = HttpResponseRedirect(url) # 转向，并让red成为response对象，调用cookie方法发送cookie

            cart_count = Cart_info.objects.filter(user_id=get_name[0].id).count()# 当前用户购物车商品的种类数量

            if jizhu!=0: # 如果不等于0 就说明点击了记住用户名，向转向的user/info发送cookie，浏览器保存cookie
                red.set_cookie('uname',name) # 设置cookie


            else:# 设置cookie为空 立马过期，
                red.set_cookie("unmae","",max_age=-1)

            # 存入到django默认服务端session中用于个人中心显示,进入订单或个人中心时验证是否登入
            request.session['user_id'] = get_name[0].id # 存入当前用户在数据库中的的id用于个人中心做数据库查询判断当前的email
            request.session['user_name'] = name # session也是一个类字典的类型，通过user_name键获取值
            red.delete_cookie('goods_ids') #　重新登入后，默认删除所有用户浏览记录
            request.session['count']=cart_count # 登入后显示购物车数量。
            return red # 返回设置的cookie,return给当前表单所属浏览器。

        # 如果密码不正确，上下文提交至页面，js判断写入出错为密码 重新渲染页面，显示之前输入的错误的账户与密码
        else:
            context ={'title':'用户登陆','error_name':0,'error_pwd':1,'uname':name,'upwd':pwd1}
            return render(request, 'tiantian/login.html', context)

    else:
        context = {'title':'用户登陆','error_name':1,'error_pwd':0,'uname':name,'upwd':pwd1}
        return render(request, 'tiantian/login.html', context)



# 用户中心，个人信息
@user_decorator.login # 调用装饰器判断是否登入。已有登入信息就执行，未有返回登入
def info(request): # 数据库通过 缓存的id 获取当前用户的eamil
    user_email = UserInfo.objects.get(id=request.session['user_id']).u_email
    u_name =request.session['user_name'] # 直接获取存入缓存中的name

    # 浏览记录,从商品详情视图中存入的cookie键获取
    goods_ids = request.COOKIES.get('goods_ids','')# 获取最新浏览的id主键，如果ｃｏｏｋｉｅ没有最新浏览记录就显示默认''
    if goods_ids != '': # 判断是否为空，
        goods_ids = goods_ids.split(',') # 切割成列表遍历最新浏览顺序后,在添加到列表中
        good_list = []
        for good_id in goods_ids:  # 添加最新浏览商品信息为，从商品详情cookie中保存的最近浏览的商品id。
            good_list.append(GoodsInfo.objects.get(id=int(good_id))) #  解包后根据id按最新顺序再放到列表中
    else: # 如果为空就执行
        good_list = []
        good_list = goods_ids

    context = {'title':'用户中心', 'uname':u_name, 'email':user_email,'title2':'用户中心','good_list':good_list}# page_name:1继承de_goods/base.html模板判断使用。
    return render(request,'tiantian/user_center_info.html',context)



# 退出``， 清除session即可
def logout(request):
    request.session.flush()  # 清除当前会话数据和cookie， session靠cookie来链接的
    return redirect('/') # 重定向到 主页


# 订单
@user_decorator.login
def order(request):
    context = {'title':'用户中心','title2':'全部订单' }
    return render(request, 'tiantian/user_center_order.html',context)
# 收货地址
@user_decorator.login
def site(requst):
    # 通过缓存 获取该用户的数据库对象
    user = UserInfo.objects.get(id = requst.session['user_id'])
    if requst.method=='POST': # 如果是表单提交存入数据库
        user.u_addressee = requst.POST['recipinet']
        user.u_add = requst.POST['site_addr']
        user.u_phone = requst.POST['phone']
        user.u_this = requst.POST['zip_code']
        user.save()
    context = {'list':user, 'title':'用户中心','title2':'收货地址' }

    return render(requst, 'tiantian/user_center_site.html',context)



