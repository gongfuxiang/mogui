# -*- coding: UTF-8 -*-

# ============================================================
# git操作
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-08-13
# ============================================================

import commands
from mogui.common import function

# 克隆
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [git地址]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def clone(dir_address, git_address) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git clone '+git_address)
    if status != 0 :
        return function.business_return('克隆失败', -700, [], output)
    return True


# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [git地址]
# @return   [dictionary]             [字典]
def get_branch(dir_address, params='') :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git branch '+params)
    if status == 0 :
        return function.business_return('获取分支成功', 0, function.get_branch_list(output))
    else :
        return function.business_return('获取分支失败', -701, [], output)


# 清除当前项目改动项（包括创建的文件与目录）
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def clean(dir_address) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git checkout .;git clean -fd')
    if status != 0 :
        return function.business_return('清除本地改动项失败', -702, [], output)
    return True


# 拉取远程分支最新代码
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [分支名称（空则同步所有分支）]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def fetch(dir_address, branch_name='') :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git fetch origin '+branch_name)
    if status != 0 :
        return function.business_return('同步远程分支失败', -703, [], output)
    return True


# 分支切换
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [分支名称]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def checkout(dir_address, branch_name) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git checkout '+branch_name)
    if status != 0 :
        return function.business_return('分支切换失败', -704, [], output)
    return True


# 拉取分支代码失败
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [分支名称]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def pull(dir_address, branch_name) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git pull origin '+branch_name)
    if status != 0 :
        return function.business_return('拉取分支失败', -705, [], output)
    return True


# 获取log列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [int]                    [获取条数]
# @return   [dictionary]             [字典]
def log(dir_address, number=30) :
    if function.git_version_determine_size([2,4]) == True :
        date_format = '--date=format:"%Y-%m-%d %H:%M:%S"'
    else :
        date_format = ''
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git log --pretty=format:"%h{|}%s{|}[%cd]{|}<%an>" '+date_format+' -'+str(number))
    if status == 0 :
        return function.business_return('获取版本成功', 0, function.get_version_list(output))
    else :
        return function.business_return('获取版本失败', -706, [], output)


# 创建分支
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [分支名称]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def branch(dir_address, branch_name) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git branch '+branch_name)
    if status != 0 :
        return function.business_return('创建分支失败', -707, [], output)
    return True


# 推送分支代码失败
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [分支名称]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def push(dir_address, branch_name) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git push origin '+branch_name)
    if status != 0 :
        return function.business_return('推送分支失败', -708, [], output)
    return True


# 版本重置
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @param    [string]                 [版本名称]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def reset(dir_address, version_name) :
    (status, output) = commands.getstatusoutput('cd '+dir_address+';git reset --hard '+version_name)
    if status != 0 :
        return function.business_return('版本重置失败', -709, [], output)
    return True