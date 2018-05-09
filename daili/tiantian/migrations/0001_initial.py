# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-09 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_name', models.CharField(max_length=20)),
                ('u_pwd', models.CharField(max_length=40)),
                ('u_addressee', models.CharField(default='', max_length=20)),
                ('u_add', models.CharField(default='', max_length=100)),
                ('u_phone', models.CharField(default='', max_length=11)),
                ('u_this', models.CharField(default='', max_length=6)),
                ('u_email', models.CharField(max_length=15)),
            ],
        ),
    ]
