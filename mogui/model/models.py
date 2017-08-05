# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# 配置表
class Config(models.Model) :
    name = models.CharField(max_length=60)

# 项目表
class Project(models.Model) :
    project_id = models.AutoField(u'项目id', primary_key=True)
    project_name = models.CharField(u'项目名称', max_length=60)
    git_ssh_address = models.CharField(u'git ssh地址', max_length=255)
    dir_address = models.CharField(u'项目路径地址', max_length=160)
    is_cluster = models.SmallIntegerField(u'是否集群模式', default=0)
    describe = models.CharField(u'描述', max_length=255)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)