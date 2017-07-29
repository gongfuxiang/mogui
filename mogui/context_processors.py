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
        'config' : settings
    }