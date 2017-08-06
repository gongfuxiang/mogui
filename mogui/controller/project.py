# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from mogui.model.models import Project
from django.http import HttpResponse
from dss.Serializer import serializer
import json

# 项目列表页面
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
def index(request) :
    context          = {}
    context['hello'] = 'project index'
    return render(request, 'project/index.html', context)


# 数据编辑页面
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
def saveinfo(request) :
    # 项目id
    try :
        project_id = int(request.GET.get('id', 0))
    except ValueError :
        project_id = 0

    # 获取项目数据
    if project_id != 0 :
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
# @blog     http://gongfuxiang.com/
# @date     2017-08-05
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def get_project_list(request) :
    keywords = request.POST.get('keywords', '')
    data = Project.objects.filter(project_name__contains=keywords).all().values('project_id', 'project_name', 'git_ssh_address', 'dir_address', 'is_cluster', 'describe', 'create_time')[0:100]
    for items in data :
        #items['describe'] = items['describe'].replace("\n", '<br />')
        if items['is_cluster'] == 0 :
            items['is_cluster_text'] = u'否'
        else :
            items['is_cluster_text'] = u'是'

    result = {"code":0, "msg":"操作成功", "data":serializer(data)}
    return HttpResponse(json.dumps(result))


# 数据保存
# @author   Devil
# @version  0.0.1
# @blog     http://gongfuxiang.com/
# @date     2017-08-04
# @param    [request]   [请求对象]
# @return   [json]      [josn]
def save(request) :
    project_id = request.POST.get('project_id', 0)
    if project_id == 0 :
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
    result = {"code":0, "msg":"操作成功", "data":[]}
    return HttpResponse(json.dumps(result))