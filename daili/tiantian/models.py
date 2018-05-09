# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserInfo(models.Model):
    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_addressee = models.CharField(max_length=20, default="")
    u_add = models.CharField(max_length=100, default="")
    u_phone = models.CharField(max_length=11, default="")
    u_this = models.CharField(max_length=6, default="")
    u_email = models.CharField(max_length=15)
