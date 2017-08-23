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
from django.db import connection
from mogui.common import function,config
import django,platform


# 初始化页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
def index(request) :
    # 获取mysql版本号
    with connection.cursor() as cursor :
        cursor.execute('SELECT VERSION() AS `ver`')
        mysql_version = cursor.fetchone()[0]
    
    # 所有相关信息
    context = {
        'python_version' : platform.python_version(),
        'django_version' : django.VERSION,
        'mysql_version'  : mysql_version,
        'system'         : platform.system()
    }
    return render(request, 'welcome/index.html', context)