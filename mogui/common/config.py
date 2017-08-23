# -*- coding: UTF-8 -*-

# ============================================================
# 配置文件
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-08-13
# ============================================================

# 站点
site = {
    'name' : 'Mogui',
    'name_tips' : '部署系统',
    'title' : '魔鬼部署系统',
    'version' : 'v1.0.0',
    'language_code' : 'zh-Hans',
    'time_zone' : 'Asia/Shanghai'
}


# 视图
view = {
    'version' : 'v1'
}


# 数据库
db = {
    'name' : 'mogui',
    'user' : 'root',
    'pwd'  : 'root',
    'host' : 'localhost',
    'port' : 3306
}


# 分页
page = {
    'page_sizes' : '[10, 30, 60, 100]',
    'page_size' : 10,
    'page_layout' : 'total, sizes, prev, pager, next, jumper'
}