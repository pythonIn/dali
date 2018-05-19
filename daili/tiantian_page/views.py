# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from tiantian_page.models import *

from django.core.paginator import Paginator


def Index(request):
      # 每条类中4条最新的，4条最热的
    typelist = TypeInfo.objects.all() # 获取所有类型，通过类型的一对多关系获取该类型下的商品
    #  查询下标为0即第一个类型中的最新，与最热，根据id先排序，然后-id降序 然后取出前4个id，（最新添加的），gclick点击最多的
    typelist0 = typelist[0].goodsinfo_set.order_by('-id')[0:4] #惰性原理是不会立马执行会运行时在执行所以可以加获取[0:4]个数据，-id倒序排序
    typelist01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4] # 最热的商品
    typelist1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    typelist11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    typelist2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    typelist22 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    typelist3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    typelist33 =typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    typelist4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    typelist44 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    typelist5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    typelist55 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {'title':'首页', 'guest_cart':1,  # 进行判断是首页继承还是用户继承页面
                'typelist0':typelist0, 'typelist01':typelist01
                ,'typelist1':typelist1, 'typelist11':typelist11
                ,'typelist2':typelist2, 'typelist22':typelist22
                ,'typelist3':typelist3, 'typelist33':typelist33
                ,'typelist4':typelist4, 'typelist44':typelist44
                ,'typelist5':typelist5, 'typelist55':typelist55
               }
    return render(request, 'df_goods/index.html', context)


  # 从index页面中传来的自定义值，1_1_1 ，1代表产品类型，1，代表分页从第1页开始，1，代表默认以index中的最新的排序
def list(request,pid,pindex,sort): # fliter获取满足条件的数据返回为对象列表类型
    typeinfo = TypeInfo.objects.get(id=int(pid)) # 查询类型为1的产品名，当前数据库id为1是水果类型
    new_goods = typeinfo.goodsinfo_set.order_by('-id')[0:2] # 获取两个最新的商品

    if int(sort) == 1: # 默认排序 按最新的,sort转化为int类型做比较，比较完后sort还是字符类型的
        goods = typeinfo.goodsinfo_set.order_by('-id') # oreder_by先排序，后-id降序 就是最新的
    if int(sort) == 2: # 按价格排序
        goods = typeinfo.goodsinfo_set.order_by('-gprice')
    if int(sort) ==3:# 按热度排序
        goods = typeinfo.goodsinfo_set.order_by('-gclick')


    pages = Paginator(goods,10) # 分10页 # 获取分页对象
    paginator = pages.page(int(pindex))   # 使用对象的page方法获取第几页的数据
    index_list = pages.page_range  # 获取  给对象分的页数。  # pindex,转化为数值返回用于判断是否在当前页
    context = {'goodstype':typeinfo,  'pindex':int(pindex),'sort':int(sort),# int(sort)转化为数值传送，进行页面显示特效的判断
                'pageinator':paginator, 'index_list':index_list, 'title':'商品列表',
               'new_goods':new_goods,'lists':1, 'ups':1}# lists,ups为了进行父页面判断后，加载页面。
            #'pageinator':paginator, html获取当前页数据。不可直接用goods 那样不受分页的数量控制了，

    return render(request, 'df_goods/list.html', context)

def detail(request, pid):
    typeinfo = TypeInfo.objects.get(id=int(pid))
    new_goods = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    context1 = {'title':'商品详情','lists':1, 'ups':1,'ups1':1,'new_goods':new_goods}
    return render(request, 'df_goods/detail.html',context1)


