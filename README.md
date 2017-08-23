# Mogui部署系统
#### 介绍
> * 魔鬼部署系统采用Python+Django+Vue+Element开发，有效提升运维效率。
> * 漂亮的操作界面、项目管理、快速上线、一键回滚。
> * 目前仅支持git项目部署、在上线过程中会放弃git当前所有的修改和创建，` 需要注意您的项目中不会存在运营过程中创建的数据，以免给您造成损失` 。
> * 环境搭建可参考博客中的文章 <a href="http://gong.gg/post-120.html" target="_blank">http://gong.gg/post-120.html</a>

#### 项目结构
```
mogui
├─mogui
│  ├─common             公共
│  │  ├─function.py         公共方法
│  │  └─config.py           公共配置文件
│  ├─controller         控制器
│  ├─model              模型
│  ├─view               视图
│  ├─settings.py        项目基础文件
│  └─urls.py            路由
├─manage.py             项目管理文件
├─public                静态资源
├─README.md             项目介绍文件
└─robots.txt            爬虫管理文件
```

#### 数据库配置信息 mogui/mogui/common/config.py
```
db = {
    'name' : 'mogui',       # 数据库名称
    'user' : 'root',        # 用户名
    'pwd'  : 'root',        # 密码
    'host' : 'localhost',   # 连接地址
    'port' : 3306           # 端口号
}
```
