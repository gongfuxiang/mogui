# -*- coding: UTF-8 -*-

# 引入模板视图类库
from django.shortcuts import render

# 引入model config数据表
from mogui.model.models import Config

# 引入http response类库
from django.http import HttpResponse
 
def index(request) :
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index/index.html', context)

def db(request) :
    # test1 = Config(name='魔鬼')
    # insert_id = test1.save()
    return HttpResponse(request.path)