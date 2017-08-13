# -*- coding: UTF-8 -*-

# ============================================================
# 公共方法
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-08-13
# ============================================================

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


# 获取版本列表
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