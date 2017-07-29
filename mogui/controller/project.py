# -*- coding: UTF-8 -*-

# 引入模板视图类库
from django.shortcuts import render

# 引入model config数据表
from mogui.model.models import Config

def index(request) :
    context          = {}
    context['hello'] = 'project index'
    return render(request, 'project/index.html', context)

def saveinfo(request) :
    context          = {}
    context['hello'] = 'project saveinfo'
    return render(request, 'project/saveinfo.html', context)