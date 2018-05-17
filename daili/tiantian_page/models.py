#coding:utf-8
from __future__ import unicode_literals

from django.db import models

from tinymce.models import HTMLField
class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    def __str__(self):   # 调用时的编码，
        return self.title.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    is_Delete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20,default='500g')
    gjianjie = models.CharField(max_length=100)
    gclick = models.IntegerField()
    gcontext = HTMLField()
    gkucun = models.IntegerField()
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self): # 调用时的编码
        return self.gtitle.encode('utf-8')



