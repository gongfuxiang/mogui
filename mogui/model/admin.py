# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mogui.model.models import Config,Project,Release

# Register your models here.
admin.site.register([Config, Project, Release])