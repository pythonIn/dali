# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from tiantian_page.models import  *

from django.core.paginator import  Paginator
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
def list(request,pid,pindex,sort): # fliter只是过滤不能获取到使用goodsinfo多关系查询.
    typeinfo = TypeInfo.objects.get(id=int(pid)); # 查询类型为1的产品名，当前数据库id为1是水果类型
    goods = typeinfo.goodsinfo_set.order_by('-id')
    context = {'list':goods}
    return render(request,'df_goods/list.html',context)



