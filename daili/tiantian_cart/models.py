# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Cart_info(models.Model):
    user = models.ForeignKey('tiantian.UserInfo') # 关联ｔｉａｎｔｉａｎ应用的　ｕｓｅｒｉｎｆｏ表
    goods = models.ForeignKey('tiantian_page.GoodsInfo')
    count = models.IntegerField()
