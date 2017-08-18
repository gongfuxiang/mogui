# -*- coding: UTF-8 -*-

# ============================================================
# 后台管理首页
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render


# 项目列表页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
def index(request) :
    return render(request, 'index/index.html')