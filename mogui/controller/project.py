# -*- coding: UTF-8 -*-

# ============================================================
# 项目管理
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-07-27
# ============================================================

from django.shortcuts import render
from django.views.decorators import csrf
from mogui.model.models import Project
import time,os
from mogui.common import function,config
from mogui.lib import git


# 项目列表页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
def index(request) :
    context = {
        'count' : Project.objects.count(),
        'page' : config.page
    }
    return render(request, 'project/index.html', context)


# 数据编辑页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
def saveinfo(request) :
    # 项目id
    project_id = request.GET.get('id', '')
    if len(project_id) > 0 :
        # 获取项目数据
        data = Project.objects.filter(project_id=project_id).first()
        if data != None :
            data.describe = data.describe.replace("\n", '\\n')
    else :
        data = None

    context = {
        'project_id' : project_id,
        'data' : data
    }
    return render(request, 'project/saveinfo.html', context)


# 列表获取
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_project_list(request) :
    keywords = request.POST.get('keywords', '')
    page = int(request.POST.get('page', 1))-1
    page_size = int(request.POST.get('page_size', config.page['page_size']))
    page_start = page*page_size
    data = Project.objects.filter(project_name__contains=keywords).all().order_by('-project_id').values('project_id', 'project_name', 'git_ssh_address', 'dir_address', 'git_alias', 'is_cluster', 'describe', 'create_time')[page_start:page_start+page_size]
    result = []
    for items in data :
        # 描述
        #items['describe'] = items['describe'].replace("\n", '<br />')
        
        # 是否集群
        if items['is_cluster'] == 0 :
            items['is_cluster_text'] = u'否'
        else :
            items['is_cluster_text'] = u'是'

        # 日期
        items['create_time'] = items['create_time'].strftime('%Y-%m-%d %H:%M');

        # 追加到列表中
        result.append(items);

    return function.ajax_return_exit('操作成功', 0, result)


# 数据保存
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def save(request) :
    # 项目id
    project_id = request.POST.get('project_id', '')

    # 等于0则添加
    if len(project_id) == 0 :
        # 临时操作地址
        project_temp_dir = function.get_project_handle_temp_dir()

        # 项目原始名称
        project_git_name = function.get_git_ssh_name(request.POST['git_ssh_address'])

        # git别名
        git_alias = request.POST.get('git_alias', '')

        # 获取项目地址
        git_dir_address = function.get_git_address(request.POST['dir_address'], request.POST['git_ssh_address'])

        # git别名地址
        git_git_alias_address = function.get_git_address(request.POST['dir_address'], '', git_alias)

        # 项目实际地址-目录不存在则创建
        ret = function.mg_mkdir(request.POST['dir_address'])
        if ret != True :
            return function.json_exit(ret)

        # 临时操作地址-目录不存在则创建
        ret = function.mg_mkdir(project_temp_dir)
        if ret != True :
            return function.json_exit(ret)


        # 项目实际地址-克隆代码
        if os.path.exists(git_dir_address) == False :
            ret = git.clone(request.POST['dir_address'], request.POST['git_ssh_address'])
            if ret != True :
                return function.json_exit(ret)

        # 临时操作地址-克隆代码
        if os.path.exists(project_temp_dir+'/'+project_git_name) == False :
            ret = git.clone(project_temp_dir, request.POST['git_ssh_address'])
            if ret != True :
                return function.json_exit(ret)


        # 项目别名处理
        if len(git_alias) > 0 and git_alias != project_git_name :
            ret = git_alias_rename(git_dir_address, project_git_name, project_temp_dir, git_alias, git_git_alias_address)
            if ret != True :
                return function.json_exit(ret)


        # 数据添加
        Project(
            project_name=request.POST['project_name'],
            git_ssh_address=request.POST['git_ssh_address'],
            git_alias=request.POST['git_alias'],
            dir_address=request.POST['dir_address'],
            is_cluster=request.POST['is_cluster'],
            describe=request.POST['describe']
        ).save()
    else :
        # 数据更新
        Project.objects.filter(project_id=project_id).update(
            project_name=request.POST['project_name'],
            git_ssh_address=request.POST['git_ssh_address'],
            git_alias=request.POST['git_alias'],
            dir_address=request.POST['dir_address'],
            is_cluster=request.POST['is_cluster'],
            describe=request.POST['describe']
        )

    # 返回数据
    return function.ajax_return_exit('操作成功')


# 项目别名处理
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [git_dir_address]         [git原始地址]
# @param    [project_git_name]        [git原始名称]
# @param    [project_temp_dir]        [git临时操作路径地址]
# @param    [git_alias]               [git别名]
# @param    [git_git_alias_address]   [git别名地址]
# @return   [boolean|dic]             [成功True, 失败字典]
def git_alias_rename(git_dir_address, project_git_name, project_temp_dir, git_alias, git_git_alias_address) :
    # 项目实际操作地址处理
    if os.path.exists(git_dir_address) == True :
        # 目标目录存在则删除
        ret = function.mg_dirrm(git_git_alias_address)
        if ret != True :
            return ret

        # 开始重命名
        ret = function.mg_mv(git_dir_address, git_git_alias_address)
        if ret != True :
            return ret

    # 临时操作地址处理
    if os.path.exists(project_temp_dir+'/'+project_git_name) == True :
        # 目标目录存在则删除
        ret = function.mg_dirrm(project_temp_dir+'/'+git_alias)
        if ret != True :
            return ret

        # 开始重命名
        ret = function.mg_mv(project_temp_dir+'/'+project_git_name, project_temp_dir+'/'+git_alias)
        if ret != True :
            return ret
    return True


# 数据删除
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def project_delete(request) :
    project_id = request.POST.get('project_id', '0')
    if project_id == '0' :
        return function.ajax_return_exit('参数错误', -1)
    Project.objects.filter(project_id=project_id).delete()

    # 返回数据
    return function.ajax_return_exit('删除成功')