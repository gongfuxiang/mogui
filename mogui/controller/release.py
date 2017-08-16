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
from mogui.model.models import Project,Release
from dss.Serializer import serializer
import commands,os
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


# 列表获取
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-16
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_release_list(request) :
    keywords = request.POST.get('keywords', '')
    data = Release.objects.filter(title__contains=keywords).all().order_by('-release_id').values('release_id', 'project_id', 'title', 'branch', 'version', 'status', 'create_time')
    status_list = [u'未发布', u'已发布', u'已回滚']
    for items in data :
        # 获取项目信息
        project = Project.objects.filter(project_id=items['project_id']).first()
        if data != None :
            items['project_name'] = project.project_name

        # 状态操作按钮处理
        if items['status'] == 0 :
            items['is_release_show'] = True
            items['is_delete_show'] = True
            items['is_rollback_show'] = False
        elif items['status'] == 1 :
            items['is_release_show'] = False
            items['is_delete_show'] = False
            items['is_rollback_show'] = True
        elif items['status'] == 2 :
            items['is_release_show'] = False
            items['is_delete_show'] = False
            items['is_rollback_show'] = False

        # 状态处理
        items['status_text'] = status_list[items['status']]


        # 日期
        #items['create_time_text'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(items['create_time'])))
        # dateArray = datetime.utcfromtimestamp(int(items['create_time']))
        # items['create_time_text'] = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        #x = time.localtime(1317091800.0)
        #items['create_time_text'] = str(time.strftime('%Y-%m-%d %H:%M:%S',x))

    return function.ajax_return_exit('操作成功', 0, serializer(data))


# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_branch_list(request) :
    # 项目id
    project_id = request.POST.get('project_id', '0')
    if project_id == '0' :
        return function.ajax_return_exit('项目id不能为空', -1)

    # 获取项目数据
    data = Project.objects.filter(project_id=project_id).first()
    if data != None :
        # 获取项目名称
        git_dir_address = function.get_git_address(data.dir_address, data.git_ssh_address)
        if os.path.exists(git_dir_address) == False:
            return function.ajax_return_exit('项目路径地址不存在', -1)

        # 获取版本列表
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git branch -a')
        if status == 0 :
            return function.ajax_return_exit('操作成功', 0, function.get_branch_list(output))
        else :
            return function.ajax_return_exit('git执行失败', -4, [], output)
    else :
        return function.ajax_return_exit('没有找到相关的项目', -3)


# 获取版本列表
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_version_list(request) :
    # 项目id
    project_id = request.POST.get('project_id', '0')
    if project_id == '0' :
        return function.ajax_return_exit('项目id不能为空', -1)

    # 分支
    branch = request.POST.get('branch')
    if len(branch) == '0' :
        return function.ajax_return_exit('请选择项目分支', -2)

    # 获取项目数据
    data = Project.objects.filter(project_id=project_id).first()
    if data != None :
        # 获取项目名称
        git_dir_address = function.get_git_address(data.dir_address, data.git_ssh_address)
        if os.path.exists(git_dir_address) == False:
                return function.ajax_return_exit('项目路径地址不存在', -1)

        # 放弃本地修改
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout .')
        if status != 0 :
            return function.ajax_return_exit('git丢弃本地修改项失败', -4, [], output)

        # 拉取远程分支最新代码
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git fetch origin '+branch)
        if status != 0 :
            return function.ajax_return_exit('git拉取远程分支失败', -4, [], output)

        # 切换分支
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout '+branch)
        if status != 0 :
            return function.ajax_return_exit('git切换分支失败', -4, [], output)

        # 获取版本列表
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git log --pretty=format:"%h{|}%s{|}[%cd]{|}<%an>" --date=format:"%Y-%m-%d %H:%M:%S" -30')
        if status == 0 :
            version_list = function.get_version_list(output)
            if len(version_list) == 0 :
                return function.ajax_return_exit('没有版本列表', -100)
            else :
                return function.ajax_return_exit('操作成功', 0, version_list)
        else :
            return function.ajax_return_exit('git执行失败', -4, [], output)
    else :
        return function.ajax_return_exit('没有找到相关的项目', -3)


# 数据保存
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-16
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def save(request) :
    # 数据添加
    Release(
        project_id=request.POST['project_id'],
        title=request.POST['title'],
        branch=request.POST['branch'],
        version=request.POST['version'],
        status=request.POST.get('status', 0)
    ).save()

    # 返回数据
    return function.ajax_return_exit('操作成功')


# 数据删除
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-16
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def release_delete(request) :
    release_id = request.POST.get('release_id', '0')
    if release_id != '0' :
        Project.objects.filter(release_id=release_id).delete()

    # 返回数据
    return function.ajax_return_exit('删除成功')