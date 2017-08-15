# -*- coding: UTF-8 -*-

# ============================================================
# 发布上线单
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render
from django.views.decorators import csrf
from mogui.model.models import Project
from dss.Serializer import serializer
import commands
from mogui.common import function

def index(request) :
    context          = {}
    context['hello'] = 'release index'
    return render(request, 'release/index.html', context)

def saveinfo(request) :
    data = Project.objects.all().order_by('-project_id').values('project_id', 'project_name')
    context = {
        'project_list' : data,
    }
    return render(request, 'release/saveinfo.html', context)

# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_branch_list(request) :
    # 项目id
    try :
        project_id = int(request.POST.get('project_id', 0))
    except ValueError :
        project_id = 0

    # 获取项目数据
    ret = {}
    branch_list = {}
    if project_id != 0 :
        data = Project.objects.filter(project_id=project_id).first()
        if data != None :
            # 获取项目名称
            git_dir_address = function.get_git_address(data.dir_address, data.git_ssh_address)

            # 获取版本列表
            (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git branch -a')
            if status == 0 :
                branch_list = function.get_branch_list(output)

    return function.ajax_return_exit('操作成功', 0, branch_list)


# 获取版本列表
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_version_list(request) :
    # 项目id
    try :
        project_id = int(request.POST.get('project_id', 0))
    except ValueError :
        project_id = 0
    if project_id == 0 :
        return function.ajax_return_exit('项目id不能为空', -1)

    # 分支
    branch = request.POST.get('branch')
    if len(branch) == 0 :
        return function.ajax_return_exit('请选择项目分支', -2)

    # 获取项目数据
    data = Project.objects.filter(project_id=project_id).first()
    if data != None :
        # 获取项目名称
        git_dir_address = function.get_git_address(data.dir_address, data.git_ssh_address)

        # 切换分支
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout .;git fetch origin '+branch+';git checkout '+branch)
        if status != 0 :
            return function.ajax_return_exit('git分支切换失败['+output+']', -4)

        # 获取版本列表
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git log --pretty=format:"%h - %s [%cd] <%an>" --date=format:"%Y-%m-%d %H:%M:%S"')
        if status == 0 :
            version_list = function.get_version_list(output)
            if len(version_list) == 0 :
                return function.ajax_return_exit('没有版本列表', -100)
            else :
                return function.ajax_return_exit('操作成功', 0, version_list)
        else :
            return function.ajax_return_exit('git执行失败['+output+']', -4)
    else :
        return function.ajax_return_exit('没有找到相关的项目', -3)