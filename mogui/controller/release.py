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
from django.http import HttpResponse
from dss.Serializer import serializer
import json,commands
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

    result = {"code":0, "msg":"操作成功", "data":branch_list}
    return HttpResponse(json.dumps(result))