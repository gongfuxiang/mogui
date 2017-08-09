# -*- coding: UTF-8 -*-

# ============================================================
# 发布上线单
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render
from django.views.decorators import csrf
from mogui.model.models import Project
from django.http import HttpResponse
from dss.Serializer import serializer
import json

def index(request) :
    context          = {}
    context['hello'] = 'release index'
    return render(request, 'release/index.html', context)

def saveinfo(request) :
    data = Project.objects.all().order_by('-project_id').values('project_id', 'project_name')
    context = {
        'data' : data
    }
    return render(request, 'release/saveinfo.html', context)