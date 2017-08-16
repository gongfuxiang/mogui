# -*- coding: UTF-8 -*-

# ============================================================
# 公共错误信息
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-08-13
# ============================================================

# 获取git错误信息
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]    [错误码]
# @return   [string]    [错误信息|不存在则返回空字符串]
def git(key) :
    # git错误列表
    error_list = {
        32768 : '项目不存在'
    }

    # 返回错误码信息, 不存在则返回空字符串
    return error_list.get(key, '')
