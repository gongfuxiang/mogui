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
    for items in data :
        # 描述
        #items['describe'] = items['describe'].replace("\n", '<br />')
        
        # 是否集群
        if items['is_cluster'] == 0 :
            items['is_cluster_text'] = u'否'
        else :
            items['is_cluster_text'] = u'是'

        # 日期
        #items['create_time_text'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(items['create_time'])))
        # dateArray = datetime.utcfromtimestamp(int(items['create_time']))
        # items['create_time_text'] = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        #x = time.localtime(1317091800.0)
        #items['create_time_text'] = str(time.strftime('%Y-%m-%d %H:%M:%S',x))

    return function.ajax_return_exit('操作成功', 0, serializer(data))


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

    # 目录不存在则创建
    if os.path.exists(request.POST['dir_address']) == False :
        os.mkdir(request.POST['dir_address'])

    # 创建分支
    if os.path.exists(git_dir_address) == False :
        (status, output) = commands.getstatusoutput('cd '+request.POST['dir_address']+';git clone '+request.POST['git_ssh_address'])

        # 项目是否拉取成功
        if status != 0 :
            return function.ajax_return_exit('git克隆失败', -1, [], output)

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