# -*- coding: UTF-8 -*-

# ============================================================
# 公共方法
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-08-13
# ============================================================

from django.http import HttpResponse
import json

# 获取项目名称
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]    [git ssh地址]
# @return   [string]    [git项目名称]
def get_git_ssh_name(url) :
    location = url.rfind('/');
    if location == -1 :
        return ''
    return url[location+1:][0:-4]


# 获取项目地址
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]     [git目录地址]
# @return   [string]     [git目录+项目名称地址]
def get_git_address(dir_name, url) :
    # git项目名称
    git_name = get_git_ssh_name(url)

    # git项目地址处理
    if dir_name[-1] == '/' :
        git_dir = dir_name+git_name
    else :
        git_dir = dir_name+'/'+git_name
    return git_dir


# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]   [版本字符串]
# @return   [list]     [版本列表]
def get_branch_list(string) :
    branch_list = []
    temp_branch = string.split('\n')
    if len(temp_branch) > 0 :
        for temp_index in range(len(temp_branch)) :
            temp_location = temp_branch[temp_index].rfind('/');
            if temp_location != -1 :
                branch = temp_branch[temp_index][temp_location+1:]
                branch_list.append({'value':branch, 'label':branch})
    return branch_list


# 获取版本列表
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]   [版本字符串]
# @return   [list]     [版本列表]
def get_version_list(string) :
    version_list = []
    temp_version = string.split('\n')
    if len(temp_version) > 0 :
        for items in temp_version :
            version_list.append({'value':items[0:7], 'label':items})
    return version_list


# 移除list中所有空值项
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]   [字符串]
# @return   [list]     [版本列表]
def remove_list_empty(l) :
    return filter(not_empty, l)


# 移除字符串前后空字符串
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]   [字符串]
# @return   [string]   [处理后的字符串]
def not_empty(string) :
    return string and string.strip()


# ajax请求返回退出
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [string]   [字符串]
# @return   [string]   [处理后的字符串]
def ajax_return_exit(msg, code=0, data=[]) :
    return HttpResponse(json.dumps({"code":code, "msg":msg, "data":data}))