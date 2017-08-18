# -*- coding: UTF-8 -*-

# ============================================================
# 初始化页面
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render
from django.conf import settings


# 初始化页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
def index(request) :
    context = {
        'python_version' : '2.7'
    }
    return render(request, 'welcome/index.html', context)