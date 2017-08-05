# -*- coding: UTF-8 -*-

# 引入模板视图类库
from django.shortcuts import render
 
def index(request) :
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'welcome/index.html', context)