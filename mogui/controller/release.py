# -*- coding: UTF-8 -*-

# ============================================================
# 上线单管理
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render
from django.views.decorators import csrf
from mogui.model.models import Project,Release
import os,time
from mogui.common import function,config
from mogui.lib import git


# 上线单列表页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
def index(request) :
    context = {
        'count' : Release.objects.count(),
        'page' : config.page
    }
    return render(request, 'release/index.html', context)


# 上线单添加页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
def saveinfo(request) :
    project_list = Project.objects.all().order_by('-project_id').values('project_id', 'project_name')
    context = {
        'project_list' : project_list,
    }
    return render(request, 'release/saveinfo.html', context)


# 列表获取
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_release_list(request) :
    keywords = request.POST.get('keywords', '')
    page = int(request.POST.get('page', 1))-1
    page_size = int(request.POST.get('page_size', config.page['page_size']))
    page_start = page*page_size
    data = Release.objects.filter(title__contains=keywords).all().order_by('-release_id').values('release_id', 'project_id', 'title', 'branch', 'version', 'status', 'create_time')[page_start:page_start+page_size]
    result = []
    if data != None :
        status_list = [u'未发布', u'已发布', u'已回滚']
        for items in data :
            # 获取项目信息
            project = Project.objects.filter(project_id=items['project_id']).first()
            if project != None :
                items['project_name'] = project.project_name
            else :
                items['project_name'] = ''

            # 状态操作按钮处理
            if items['status'] == 0 :
                items['is_release_show'] = True
                items['is_delete_show'] = True
                items['is_rollback_show'] = False
            elif items['status'] == 1 :
                items['is_release_show'] = False
                items['is_delete_show'] = False
                items['is_rollback_show'] = True
            else :
                items['is_release_show'] = False
                items['is_delete_show'] = False
                items['is_rollback_show'] = False

            # 状态处理
            items['status_text'] = status_list[items['status']]

            # 日期
            items['create_time'] = items['create_time'].strftime('%Y-%m-%d %H:%M');

            # 追加到列表中
            result.append(items);

    return function.ajax_return_exit('操作成功', 0, result)


# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_branch_list(request) :
    # 项目id
    project_id = request.POST.get('project_id', '')
    if len(project_id) == 0 :
        return function.ajax_return_exit('项目id不能为空', -1)

    # 获取项目数据
    data = Project.objects.filter(project_id=project_id).first()
    if data != None :
        # 获取项目名称
        git_dir_address = function.get_git_address(function.get_project_handle_temp_dir(), data.git_ssh_address, data.git_alias)

        if os.path.exists(git_dir_address) == False:
            return function.ajax_return_exit('项目路径地址不存在', -2)

        # 获取版本列表
        return function.json_exit(git.get_branch(git_dir_address, '-a'))
    else :
        return function.ajax_return_exit('没有找到相关的项目', -3)


# 获取版本列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_version_list(request) :
    # 项目id
    project_id = request.POST.get('project_id', '')
    if len(project_id) == 0 :
        return function.ajax_return_exit('项目id不能为空', -1)

    # 分支名称
    branch = request.POST.get('branch')
    if len(branch) == 0 :
        return function.ajax_return_exit('请选择项目分支', -2)

    # 获取项目数据
    data = Project.objects.filter(project_id=project_id).first()
    if data != None :
        # 获取项目名称
        git_dir_address = function.get_git_address(function.get_project_handle_temp_dir(), data.git_ssh_address, data.git_alias)
        if os.path.exists(git_dir_address) == False:
                return function.ajax_return_exit('项目路径地址不存在', -1)

        # 清除当前项目改动项
        ret = git.clean(git_dir_address)
        if ret != True :
            return function.json_exit(ret)

        # 拉取远程分支最新代码
        ret = git.fetch(git_dir_address, branch)
        if ret != True :
            return function.json_exit(ret)

        # 分支切换
        ret = git.checkout(git_dir_address, branch)
        if ret != True :
            return function.json_exit(ret)

        # 拉取分支最新代码到本地分支
        ret = git.pull(git_dir_address, branch)
        if ret != True :
            return function.json_exit(ret)

        # 获取版本列表
        return function.json_exit(git.log(git_dir_address, 30))
    else :
        return function.ajax_return_exit('没有找到相关的项目', -3)


# 数据保存
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
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
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def release_delete(request) :
    release_id = request.POST.get('release_id', '0')
    if release_id == '0' :
        return function.ajax_return_exit('参数错误', -1)
    Release.objects.filter(release_id=release_id).delete()

    # 返回数据
    return function.ajax_return_exit('删除成功')


# 上线工单发布
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-17
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def handle_release(request) :
    # 参数校验
    project_id = request.POST.get('project_id', '0')
    release_id = request.POST.get('release_id', '0')
    handle_type = int(request.POST.get('handle_type', 1))
    if project_id == '0' or release_id == '0' :
        return function.ajax_return_exit('参数错误', -1)

    # 获取项目数据
    project = Project.objects.filter(project_id=project_id).first()
    if project == None :
        return function.ajax_return_exit('没有找到相关的项目', -3)

    # 获取上线工单数据
    release = Release.objects.filter(release_id=release_id).first()
    if release == None :
        return function.ajax_return_exit('没有找到相关的上线工单', -4)

    # 获取项目名称
    git_dir_address = function.get_git_address(project.dir_address, project.git_ssh_address, project.git_alias)
    if os.path.exists(git_dir_address) == False:
        return function.ajax_return_exit('项目路径地址不存在', -5)

    # 清除当前项目改动项
    ret = git.clean(git_dir_address)
    if ret != True :
        return function.json_exit(ret)
    
    # 上线操作
    if handle_type == 1 :
        # 备份当前代码
        backup_name = 'backup_'+time.strftime('%Y%m%d%H%M%S', time.localtime())
        ret = git.branch(git_dir_address, backup_name)
        if ret != True :
            return function.json_exit(ret)

        # 备份分支推送到远程仓库
        ret = git.push(git_dir_address, backup_name)
        if ret != True :
            return function.json_exit(ret)

        # 拉取远程分支最新代码
        ret = git.fetch(git_dir_address, release.branch)
        if ret != True :
            return function.json_exit(ret)

        # 分支切换
        ret = git.checkout(git_dir_address, release.branch)
        if ret != True :
            return function.json_exit(ret)

        # 拉取分支最新代码到本地分支
        ret = git.pull(git_dir_address, release.branch)
        if ret != True :
            return function.json_exit(ret)

        # git更新到工单指定分支与版本
        ret = git.reset(git_dir_address, release.version)
        if ret != True :
            return function.json_exit(ret)

        # 更新工单数据
        Release.objects.filter(release_id=release_id).update(
            status=1,
            backup_name=backup_name
        )
        return function.ajax_return_exit('上线成功')

    # 回滚操作
    elif handle_type == 2 :
        # 拉取远程分支最新代码
        ret = git.fetch(git_dir_address, release.backup_name)
        if ret != True :
            return function.json_exit(ret)

        # 分支切换
        ret = git.checkout(git_dir_address, release.backup_name)
        if ret != True :
            return function.json_exit(ret)

        # 拉取分支最新代码到本地分支
        ret = git.pull(git_dir_address, release.backup_name)
        if ret != True :
            return function.json_exit(ret)

        # 更新工单数据
        Release.objects.filter(release_id=release_id).update(status=2)
        return function.ajax_return_exit('回滚成功')

    # 操作类型有误
    else :
        return function.ajax_return_exit('上线工单类型错误', -99)