# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from tiantian.models import * # 导入用户模型，查询用户地址

from tiantian_cart.models import *

from django.db import transaction #　事务

from tiantian_order.models import *

from datetime import datetime

from tiantian_page.models import *

from decimal import Decimal # 指定的十进制长度，小数位数

from django.http import JsonResponse

from tiantian import user_decorator


@user_decorator.login
def order(request):
    user = UserInfo.objects.get(id = request.session['user_id']) # 通过查询ｓｅｓｓｉｏｎ中的用户ｉｄ，获取当前用户数据库对象

    # 获取html表单get提交的键名下的值,checkbox属性，勾选了表示有此标签属性，未勾选则无
    order = request.GET.getlist('orderid') # 以一个Python列表的形式返回指定键的值.若该键不存在,返回一个空的列表.该列表是以某种方式排序的.
    print ('*')* 100     # GET['orderid']只能接收一个参数，所以要用ｇｅｔｌｉｓｔ

    list = [] #　创建个新列表添加传来的id值,转化为购物车中的对象
    for order_list in order:
        list.append(Cart_info.objects.get(id=int(order_list))) # 获取在购物车数据库中的对象

    if user.u_phone=='':
        user.u_phone=''
    else:                                                  #到字符串下标　－４
        user_phone = user.u_phone[0:3]+'****'+user.u_phone[-4:]  #　切割给手机号加****
    context = {'title':'订单中心','title2':'订单中心', 'user':user,'list':list, 'user_phone':user_phone}
    return render(request,'tiantian_order/place_order.html',context)


 # 判断订单中的数据是否正确，保存到数据库

@user_decorator.login
#　获取ｐｏｓｔ保存订单数据到服务器
def order_hadler(request):
    # 保存一个事务点
    tran_id = transaction.savepoint()

    try:
        # 接收购物车编号
        post = request.POST
        order_list = post.getlist('id[]')# 因为post传送的为购物车多个ｉｄ值是在ｈｔｔｐ头中所以加[]列表获取，需要用getlist 接收
        sums1 = post.get('sum')
        address = post.get('address') # 接收的是地址手机号用户名等信息字符串

        # 创建订单主表对象，　用户信息等　(放在ｉｆ前面的目的是好知道订单的状态，如果未支付，显示未支付，如果库存不够显示此订单下了但是库存不足)
        order = order_info()
        now = datetime.now()  # 获取当前时间
        u_id = request.session.get('user_id')# 通过ｓｅｓｓｉｏｎ获取用户ｉｄ

        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),u_id) # 订单编号存入当前时间2018053001183163"和用户id
        order.user_id = u_id # 用户名存入到订单表的用户名中
        order.odate = now # 当前时间存入
        order.momeys = Decimal(sums1) # 数据库中指定的十进制位数与２位小数
        order.address = address # 当前地址用户名手机号存入到订单表的　地址中
        order.save()


       # 遍历购物车中提交的信息
        for cartid in order_list:

            cart_info = Cart_info.objects.get(id = cartid) # 获取购物车当前的主键ｉｄ
            good = GoodsInfo.objects.get(id = cart_info.goods.id) # 获取当前购物车中此商品ｉｄ


            # 如果购物车中的该商品小于等于库存
            if int(cart_info.count)<= int(good.gkucun):
                # 移除购买数量并保存
                good.gkucun = int(good.gkucun) - int(cart_info.count)
                good.save()

                # 另种方法获取当前商品         # 一查多的关系表字段　需要两个__　而且表名必须小写
                good_info = GoodsInfo.objects.get(cart_info__id=cartid)  # 获取在当前购物车主键ｉｄ号中的商品ｉｄ
                # 获取　在购物车的ｉｄ主键编号是此号的商品

                # 创建订单详情表（商品信息)，保存至订单详情表中，　放在ｉｆ中如果未支付成功的会不存到数据库中，在订单中心不显示该商品名，图片
                detailinfo = order_detailinfo()
                detailinfo.goods = good_info  # 商品信息
                detailinfo.order_id = int(order.oid)  # 关联当前订单主表的主键ｉｄ,在同一模型中直接通过一的关系表对象的值获取给多的关系表外键，该属性不加_id　会出错
                detailinfo.price = Decimal(good_info.gprice)  # 购买时商品的价格，,数据库中指定的十进制位数和小数
                detailinfo.count = int(cart_info.count)  # 获取购物车提交订单时商品的数量,确保万一就转ｉｎｔ呗
                detailinfo.save()

                # 循环删除购物车对象
                cart_info.delete()

            #(****)如果有支付接口，此时判断完库存，保存好订单数据库就提交到支付接口中，支付接口进行支付操作，错误就回滚，正确就标记支付成功'''
                # 当前没有接口环境，无法判断是否支付成功，所以默认判断完库存就为成功
                detailinfo.order.Ispay = True
                detailinfo.order.save() # 根据当前用户的详情表外键到该用户的主表赋值。不可直接用主表赋值，不然保存出错。
                                # 因主表字段在if外面，for循环再判断时主表无法确认是哪个用户，除非主表字段全部重新赋值


                #循环删除购物车显示数量的　ｓｅｓｓｉｏｎ
                a = request.session['count']
                if int(a) >=1: # 购物车中的数量不能为负数（如成功提交后页面返回上级未刷新再次提交会造成执行，就为负数）
                    request.session['count'] = int(a)-1
                else:
                    request.session['count'] = 0  # ａ为负数或０　不执行减数量，　购物车就等于０
            # 库存不够回滚到指定位置
            else:
                transaction.savepoint_rollback(tran_id)
                #　返回ｊｓｏｎ供前台展示失败原因
                return JsonResponse({'erro':1})

        # 如果查询不到出错
    except Exception as e:
        print('***************************%s'%e) # 提示错误信息
        transaction.savepoint_rollback(tran_id) #　回滚

        # 返回ｊｓｏｎ　购买成功
    return JsonResponse({'erro':0})



# 点击订单中心的去付款按钮，　再次判断库存(未设计)，　完成支付　在减去库存（未设计），
def pay(request, oid): # 接收当前订单的主键oｉｄ　根据主键获取当前主表对象
    pay = order_info.objects.get(oid= oid)
    #　没有接口也无法判断　所以直接算成功购买, 操作保存时会更新odate字段当前时间
    pay.Ispay = True
    a = pay.order_detailinfo_set.count()

    print(a)
    pay.save()
    context = {'oid':pay}
    return render(request, 'tiantian_order/pay.html', context)



