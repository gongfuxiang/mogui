# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# 配置表
class Config(models.Model) :
    name = models.CharField(max_length=20)