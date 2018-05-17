# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

import models


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','title']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gpic','gtitle','gkucun','gprice','gcontext','gclick','gtype','is_Delete','gjianjie','gunit']
    list_per_page = 15

admin.site.register(models.TypeInfo,TypeInfoAdmin)
admin.site.register(models.GoodsInfo,GoodsInfoAdmin)