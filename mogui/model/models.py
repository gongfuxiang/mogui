# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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

# 上线工单表
class Release(models.Model) :
    release_id = models.AutoField(u'上线工单id', primary_key=True)
    project_id = models.IntegerField(u'项目id', default=0)
    title = models.CharField(u'标题', max_length=60)
    branch = models.CharField(u'分支', max_length=160)
    version = models.CharField(u'版本', max_length=80)
    backup_name = models.CharField(u'备份分支名称(以backup_开头)', max_length=255)
    status = models.SmallIntegerField(u'状态[ 0未发布, 1已发布, 2已回滚 ]', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)