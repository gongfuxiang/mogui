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
from controller import index,project,release

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 首页
    url(r'^$', index.index),

    # 项目列表页面
    url(r'^project/index$', project.index),

    # 项目添加页面
    url(r'^project/saveinfo$', project.saveinfo),

    # 上线单列表页面
    url(r'^release/index$', release.index),

    # 上线单添加页面
    url(r'^release/saveinfo$', release.saveinfo),

    # 数据库数据添加
    url(r'^db$', index.db),
]
