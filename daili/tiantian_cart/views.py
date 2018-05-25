# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import tiantian.user_decorator  # 装饰器，判断是否登入

from tiantian_cart.models import *

from django.http import JsonResponse



@tiantian.user_decorator.login  # 装饰其判断用户是否登入，如果登入就执行，未登入转到登入页面。对于局部刷新的不判断，需单独在ｈｔｍｌ判断
def cart(request): # 获取用户添加到购物车的产品
    uids = request.session['user_id'] # 获取当前用户的ID
                            #使用ｆｉｌｔｅｒ目的是，新用户没有添加购物车如果为空也不会报错，
    cart = Cart_info.objects.filter(user = uids) # 获取当前用户对象，通过用户对象就可获得对应的购物车的商品

    context = {'title': '购物车', 'title2': '购物车','cart_goods':cart}


    return render(request, 'tiantian_cart/cart.html', context)


@tiantian.user_decorator.login
def add(request,gid,count): # 用户添加商品到购物车
    # 用户ｕｉｄ购买了ｇｉｄ商品，数量为ｃｏｕｎｔ
    uid = request.session['user_id']#获取当前用户的ｉｄ添加商品
    gid = int(gid) # 用户添加的商品
    count = int(count) # 商品的数量
    # 查询当前用户之前是否添加过此商品到购物车，如果添加过直接加数量
    carts = Cart_info.objects.filter(user_id=uid,goods_id=gid) # user_id为关联用户ｉｄ后，显示在购物车数据库中的字段，
                                                        # 购物车这两个字段存贮的是用户名与商品的关系，多对多关系，
                                                     # 即可以在购物车中根据用户名查询到该用户下的多个商品，根据商品可以查询该商品下的所有用户
                                                   # Care_info_ｓｅｔ filter(user_id = 用户id) 查询用户下的购物车商品信息。
    if len(carts)>=1: # 如果查询到购物车中有此商品则数量相加
        cart =carts[0]  # 因为一个用户只可能有一个不同的商品，取到该商品在商品列表中的位置直接在该商品中添加数量，而不是在商品列表中添加总商品数量
        cart.count = cart.count + count

    else: # 直接存入到购物车内，　把它添加到用户的商品列表中
        cart = Cart_info() # 获取购物车表对象
        cart.user_id = uid # 关联后ｕｓｅｒ在数据库中显示为ｕｓｅｒ_id把用户ｉｄ存入到购物车数据库字段ｕｓｅｒ_id中。
        cart.goods_id = gid #把当前商品的ｉｄ主键存入到购物车中。根据当前商品的主键在ｈｔｍｌ中{{cart.goods.gtitle}}获取当前商品的名字。
        cart.count = count # 关联的作用是在购物车这个平台中可以根据这个商品获取到其下所有的用户，反之一样
    cart.save()   # 在这里把id和商品id它们保存在一个对象中到购物车数据库，所以在查询的时候可以根据一方查询到另一方
    count_s = Cart_info.objects.filter(user_id = uid ).count() # 获取当前用户购物车中有多少种商品，反过来写可判断这个商品有多少用户

    request.session['count'] = count_s # 如有添加新产品到购物车就更新当前购物车数量的ｓｅｓｓｉｏｎ，用于显示购物车商品数量的页面使用ｓｅｓｓｉｏｎ显示
    # 如果是ajax 请求返回json，否则转向到购物车
    if request.is_ajax():
        return JsonResponse({'count':count_s})# ajax请求的只为添加到购物车中显示购物车的商品数量，而不转向

    else:
        return redirect('/cart/cart') # 转到页面进行查询显示


# ｊｓ加减数量等操作，都存入到数据库中，
def mend(request,cid,count):
    cid = int(cid)#获取购物车的主键ｉｄ
    count = int(count)
    try:

        cart = Cart_info.objects.get(id=cid,) # 在数据库中查询传来的当前商品所在购物车ｉｄ,如果没有获取到就出错
        cart.count = count  # 更改此商品的数量存到ｃｏｕｎｔ1中
        cart.save()

        countxt = {'ok':1}
    except Exception:
        countxt = {'ok':0}# 如果出错就返回0
    return JsonResponse(countxt)

# 删除产品操作
def cart_del(request,cid):
    try:
        cart = Cart_info.objects.get(id=int(cid)) # 根据商品在购物车的主键ｉｄ　获取到该主键ｉｄ
        cart.delete()    #　删除操作不需要保存，不然会删不掉。

        context = {'ok':1}
    except Exception:
        context = {'ok':0}
    return JsonResponse(context)
