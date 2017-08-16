# -*- coding: UTF-8 -*-

"""mogui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from controller import index,project,release,welcome

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 首页
    url(r'^$', index.index),

    # 欢迎页面
    url(r'^welcome$', welcome.index),

    # 项目列表页面
    url(r'^project/index$', project.index),

    # 获取项目列表
    url(r'^project/get_project_list$', project.get_project_list),

    # 项目删除
    url(r'^project/project_delete$', project.project_delete),

    # 项目添加页面
    url(r'^project/saveinfo$', project.saveinfo),

    # 项目保存
    url(r'^project/save$', project.save),

    # 上线单列表页面
    url(r'^release/index$', release.index),

    # 上线单添加页面
    url(r'^release/saveinfo$', release.saveinfo),

    # 获取分支列表
    url(r'^release/get_branch_list$', release.get_branch_list),

    # 获取上线工单列表
    url(r'^release/get_release_list$', release.get_release_list),

    # 上线工单删除
    url(r'^release/release_delete$', release.release_delete),

    # 上线单保存
    url(r'^release/save$', release.save),

    # 获取版本列表
    url(r'^release/get_version_list$', release.get_version_list),

    # 数据库数据添加
    url(r'^db$', index.db),
]
