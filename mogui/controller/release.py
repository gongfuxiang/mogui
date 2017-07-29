# -*- coding: UTF-8 -*-

# ============================================================
# 发布上线单
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render
from mogui.model.models import Config

def index(request) :
    context          = {}
    context['hello'] = 'release index'
    return render(request, 'release/index.html', context)

def saveinfo(request) :
    context          = {}
    context['hello'] = 'release saveinfo'
    #context['v'] = settings.TEMPLATES_DEFAULT_VERSION
    return render(request, 'release/saveinfo.html', context)