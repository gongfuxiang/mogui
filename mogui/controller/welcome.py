# -*- coding: UTF-8 -*-

# 引入模板视图类库
from django.shortcuts import render
from django.conf import settings
 
def index(request) :
    context          = {}
    context['hello'] = 'Hello World!'+settings.BASE_DIR
    return render(request, 'welcome/index.html', context)