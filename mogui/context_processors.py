# -*- coding: UTF-8 -*-

# ============================================================
# 自定义全局上下文处理器
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.conf import settings

# 配置信息
def config(request) :
    return {
        'config' : settings,
        'host' : get_host(request),
        'nav_left' : nav_left(request),
    }

# 获取host
def get_host(request) :
    if(request.is_secure() == True) :
        http = 'https://'
    else :
        http = 'http://'
    return http+request.get_host()+'/'

# 左侧导航
def nav_left(request) :
    host = get_host(request)
    return [
        {
            'name' : '项目管理',
            'url' : host+'project/index',
            'is_show' : True,
            'index' : '1',
            'items' : [
                {
                    'name' : '项目列表',
                    'url' : host+'project/index',
                    'is_show' : True,
                    'index' : '1-1',
                }
            ]
        },
        {
            'name' : '上线管理',
            'url' : host+'release/index',
            'is_show' : True,
            'index' : '2',
            'items' : [
                {
                    'name' : '上线列表',
                    'url' : host+'release/index',
                    'is_show' : True,
                    'index' : '2-1',
                }
            ]
        },
    ]