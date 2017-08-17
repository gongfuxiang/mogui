# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from mogui.model.models import Project
from django.http import HttpResponse
from dss.Serializer import serializer
import json,time,datetime,commands,os,shutil
from mogui.common import function

# 项目列表页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
def index(request) :
    context          = {}
    context['hello'] = 'project index'
    return render(request, 'project/index.html', context)


# 数据编辑页面
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-05
# @param    [request]   [请求对象]
def saveinfo(request) :
    # 项目id
    project_id = request.GET.get('id', '0')
    if project_id != '0' :
        # 获取项目数据
        data = Project.objects.filter(project_id=project_id).first()
        if data != None :
            data.describe = data.describe.replace("\n", '\\n')
    else :
        data = {}

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
    data = Project.objects.filter(project_name__contains=keywords).all().order_by('-project_id').values('project_id', 'project_name', 'git_ssh_address', 'dir_address', 'is_cluster', 'describe', 'create_time')
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
    project_id = request.POST.get('project_id', '0')

    # 获取项目名称
    git_dir_address = function.get_git_address(request.POST['dir_address'], request.POST['git_ssh_address'])

    # 等于0则添加
    if project_id == '0' :
        # 添加情况下 项目存在则删除
        if os.path.exists(git_dir_address) == True :
            shutil.rmtree(git_dir_address)

    # 项目实际地址-目录不存在则创建
    if os.path.exists(request.POST['dir_address']) == False :
        os.mkdir(request.POST['dir_address'])

    # 项目实际地址-克隆代码
    if os.path.exists(git_dir_address) == False :
        (status, output) = commands.getstatusoutput('cd '+request.POST['dir_address']+';git clone '+request.POST['git_ssh_address'])
        if status != 0 :
            return function.ajax_return_exit('git克隆失败', -10, [], output)

    # 临时操作地址
    project_temp_dir = function.get_project_handle_temp_dir()
    project_git_name = function.get_git_ssh_name(request.POST['git_ssh_address'])

    # 临时操作地址-目录不存在则创建
    if os.path.exists(project_temp_dir) == False :
        os.mkdir(project_temp_dir)

    # 临时操作地址-克隆代码
    if os.path.exists(project_temp_dir+'/'+project_git_name) == False :
        (status, output) = commands.getstatusoutput('cd '+project_temp_dir+';git clone '+request.POST['git_ssh_address'])
        if status != 0 :
            return function.ajax_return_exit('git克隆失败', -10, [], output)

    # 等于0则添加
    if project_id == '0' :
        # 数据添加
        Project(
            project_name=request.POST['project_name'],
            git_ssh_address=request.POST['git_ssh_address'],
            dir_address=request.POST['dir_address'],
            is_cluster=request.POST['is_cluster'],
            describe=request.POST['describe']
        ).save()
    else :
        # 数据更新
        Project.objects.filter(project_id=project_id).update(
            project_name=request.POST['project_name'],
            git_ssh_address=request.POST['git_ssh_address'],
            dir_address=request.POST['dir_address'],
            is_cluster=request.POST['is_cluster'],
            describe=request.POST['describe']
        )

    # 返回数据
    return function.ajax_return_exit('操作成功')


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