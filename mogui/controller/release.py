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
import commands,os,time
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
# @blog     http://gong.gg/
# @date     2017-08-16
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_release_list(request) :
    keywords = request.POST.get('keywords', '')
    data = Release.objects.filter(title__contains=keywords).all().order_by('-release_id').values('release_id', 'project_id', 'title', 'branch', 'version', 'status', 'create_time')
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
            #items['create_time_text'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(items['create_time'])))
            # dateArray = datetime.utcfromtimestamp(int(items['create_time']))
            # items['create_time_text'] = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            #x = time.localtime(1317091800.0)
            #items['create_time_text'] = str(time.strftime('%Y-%m-%d %H:%M:%S',x))

    return function.ajax_return_exit('操作成功', 0, serializer(data))


# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
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
        git_dir_address = function.get_git_address(function.get_project_handle_temp_dir(), data.git_ssh_address)

        if os.path.exists(git_dir_address) == False:
            return function.ajax_return_exit('项目路径地址不存在', -2)

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
# @blog     http://gong.gg/
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
        git_dir_address = function.get_git_address(function.get_project_handle_temp_dir(), data.git_ssh_address)
        if os.path.exists(git_dir_address) == False:
                return function.ajax_return_exit('项目路径地址不存在', -1)

        # 清除当前项目改动项
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout .;git clean -fd')
        if status != 0 :
            return function.ajax_return_exit('git清除本地改动项失败', -10, [], output)

        # 拉取远程分支最新代码
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git fetch origin '+branch)
        if status != 0 :
            return function.ajax_return_exit('git拉取远程分支失败', -11, [], output)

        # 分支切换
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout '+branch)
        if status != 0 :
            return function.ajax_return_exit('git分支切换失败', -12, [], output)

        # 拉取分支最新代码到本地分支
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git pull origin '+branch)
        if status != 0 :
            return function.ajax_return_exit('git拉取分支代码失败', -13, [], output)

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
    git_dir_address = function.get_git_address(project.dir_address, project.git_ssh_address)
    if os.path.exists(git_dir_address) == False:
        return function.ajax_return_exit('项目路径地址不存在', -5)

    # 清除当前项目改动项
    (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout .;git clean -fd')
    if status != 0 :
        return function.ajax_return_exit('git清除本地改动项失败', -10, [], output)
    
    # 上线操作
    if handle_type == 1 :
        # 备份当前代码
        backup_name = 'backup_'+time.strftime('%Y%m%d%H%M%S', time.localtime())
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git branch '+backup_name)
        if status != 0 :
            return function.ajax_return_exit('git创建备份失败', -11, [], output)

        # 备份分支推送到远程仓库
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git push origin '+backup_name)
        if status != 0 :
            return function.ajax_return_exit('git备份到远程仓库失败', -12, [], output)

        # 拉取远程分支最新代码
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git fetch origin '+release.branch)
        if status != 0 :
            return function.ajax_return_exit('git拉取远程分支失败', -13, [], output)

        # 分支切换
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout '+release.branch)
        if status != 0 :
            return function.ajax_return_exit('git分支切换失败', -14, [], output)

        # 拉取分支最新代码到本地分支
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git pull origin '+release.branch)
        if status != 0 :
            return function.ajax_return_exit('git拉取分支代码失败', -15, [], output)

        # git更新到工单指定分支与版本
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git reset --hard '+release.version)
        if status != 0 :
            return function.ajax_return_exit('上线失败', -100, [], output)

        # 更新工单数据
        Release.objects.filter(release_id=release_id).update(
            status=1,
            backup_name=backup_name
        )
        return function.ajax_return_exit('上线成功')

    # 回滚操作
    elif handle_type == 2 :
        # 拉取远程分支最新代码
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git fetch origin '+release.backup_name)
        if status != 0 :
            return function.ajax_return_exit('git远程备份分支拉取失败', -13, [], output)

        # 分支切换
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git checkout '+release.backup_name)
        if status != 0 :
            return function.ajax_return_exit('git分支切换失败', -14, [], output)

        # 拉取分支最新代码到本地分支
        (status, output) = commands.getstatusoutput('cd '+git_dir_address+';git pull origin '+release.backup_name)
        if status != 0 :
            return function.ajax_return_exit('回滚失败', -100, [], output)

        # 更新工单数据
        Release.objects.filter(release_id=release_id).update(status=2)
        return function.ajax_return_exit('回滚成功')

    # 操作类型有误
    else :
        return function.ajax_return_exit('上线工单类型错误', -99)
        
    # 默认失败返回
    return function.ajax_return_exit('操作失败', -1000)
