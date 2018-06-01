# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



# 订单主表，　包含用户下订单方面的信息，　
class order_info(models.Model):
    oid = models.CharField(max_length=20,primary_key=True) # 订单的编号，
    user = models.ForeignKey('tiantian.UserInfo')# 是哪个用户的,关联到ｔｉａｎｔｉａｎ表中的数据库
    odate = models.DateTimeField(auto_now=True) # 订单的时间，当前时间
    Ispay = models.BooleanField(default=False) # 是否支付
    momeys = models.DecimalField(max_digits=6, decimal_places=2)# 总计费用，包含小数最大６位数，留两位小数
    address = models.CharField(max_length=150) # 下订单用户的地址

    def __str__(self):  # 支付成功页面调用显示订单编号时显示编码为ｕｔｆ－８的
        return self.oid.encode('utf-8')
# 无法实现真实价格，物流信息。　　需要支付端口，以及物流端口

# 订单详表　包含商品方面的信息.商品，数量价格,等，　要关联订单主表。
class order_detailinfo(models.Model):
    goods = models.ForeignKey('tiantian_page.GoodsInfo') # 商品信息
    order = models.ForeignKey(order_info) # 关联订单主表。当前详单属于哪个订单的
    price = models.DecimalField(max_digits=5, decimal_places=2) # 购买时的商品价格
    count = models.IntegerField() # 商品的数量
