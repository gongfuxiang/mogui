# -*- coding: UTF-8 -*-

# ============================================================
# 公共方法
# author    Devil
# blog      http://gong.gg/
# version   0.0.1
# datetime  2017-08-13
# ============================================================

from django.http import HttpResponse
from django.conf import settings
import commands,re,os
try :
    import json # python >= 2.6
except ImportError:
    import simplejson as json # python <= 2.5

# 特殊字符处理（超出ascii处理的范围）
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# git版本号大小判断
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-21
# @param    [list]       [版本号(如: [1,3,6])]
# @return   [boolean]    [系统版本大于参数版本True, 则False]
def git_version_determine_size(ver_list) :
    if len(ver_list) <= 0 :
        return False
    (status, output) = commands.getstatusoutput('git --version')
    if status == 0 :
        re_list = re.compile(r'[1-9]\d*').findall(output)
        re_count = len(re_list)
        print re_list
        if re_count > 0 :
            for index in range(len(ver_list)) :
                if index < re_count :
                    if int(re_list[index]) < int(ver_list[index]) :
                        return False
    else :
        return False
    return True


# 获取项目临时操作地址
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @return   [string]    [项目临时操作地址]
def get_project_handle_temp_dir() :
    return settings.BASE_DIR+'/temp_project'


# 获取项目名称
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]    [git ssh地址]
# @return   [string]    [git项目名称]
def get_git_ssh_name(url) :
    location = url.rfind('/');
    if location == -1 :
        return ''
    return url[location+1:][0:-4]


# 获取项目地址
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]     [git目录地址]
# @return   [string]     [git目录+项目名称地址]
# @param    [string]     [git别名（可选）]
def get_git_address(dir_name, url='', git_alias='') :
    # git项目名称
    if len(git_alias) == 0 :
        git_name = get_git_ssh_name(url)
    else :
        git_name = git_alias

    # git项目地址处理
    if dir_name[-1] == '/' :
        git_dir = dir_name+git_name
    else :
        git_dir = dir_name+'/'+git_name
    return git_dir


# 获取分支列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]   [版本字符串]
# @return   [list]     [版本列表]
def get_branch_list(string) :
    branch_list = []
    temp_branch = string.split('\n')
    if len(temp_branch) > 0 :
        for temp_index in range(len(temp_branch)) :
            if temp_branch[temp_index].rfind('->') == -1 :
                temp_location = temp_branch[temp_index].rfind('/');
                if temp_location != -1 :
                    branch = temp_branch[temp_index][temp_location+1:]
                    branch_list.append({'value':branch, 'label':branch})
    return branch_list


# 获取版本列表
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]   [版本字符串]
# @return   [list]     [版本列表]
def get_version_list(string) :
    version_list = []
    temp_version = string.split('\n')
    max_length = 30
    if len(temp_version) > 0 :
        for items in temp_version :
            temp_ver = items.split('{|}')
            if len(temp_ver[1]) > max_length :
                temp_join = '...'
            else :
                temp_join = ''
            version_list.append({'value':temp_ver[0], 'label':temp_ver[0]+' - '+temp_ver[1].decode('utf8')[0:max_length]+temp_join+' '+temp_ver[2]+' '+temp_ver[3]})
    return version_list


# 移除list中所有空值项
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]   [字符串]
# @return   [list]     [版本列表]
def remove_list_empty(l) :
    return filter(not_empty, l)


# 移除字符串前后空字符串
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]   [字符串]
# @return   [string]   [处理后的字符串]
def not_empty(string) :
    return string and string.strip()


# ajax请求返回退出
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]   [错误信息]
# @param    [int]      [错误码]
# @param    [list]     [返回数据]
# @param    [string]   [提示信息]
# @return   [json]     [json数据]
def ajax_return_exit(msg, code=0, data=[], tips='') :
    return json_exit({'code':code, 'msg':msg, 'data':data, 'tips':tips})


# 输出json并退出
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [dic]      [输出数据]
# @return   [json]     [json数据]
def json_exit(data) :
    return HttpResponse(json.dumps(data))


# 业务数据返回方法
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]   [错误信息]
# @param    [int]      [错误码]
# @param    [list]     [返回数据]
# @param    [string]   [提示信息]
# @return   [json]     [json数据]
def business_return(msg, code=0, data=[], tips='') :
    return {'code':code, 'msg':msg, 'data':data, 'tips':tips}


# 目录创建（支持多级目录）
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def mg_mkdir(dir_address) :
    if os.path.exists(dir_address) == False :
        try :
            os.makedirs(dir_address)
        except OSError, e :
            return business_return('请检查目录或权限是否正确', -3, [], str(e))
    return True


# 目录删除（支持多级目录）
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [目录地址]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def mg_dirrm(dir_address) :
    if os.path.exists(dir_address) == True :
        try :
            shutil.rmtree(dir_address)
        except OSError, e :
            return business_return('请检查目录或权限是否正确', -4, [], str(e))
    return True


# 目录重命名
# @author   Devil
# @version  0.0.1
# @blog     http://gong.gg/
# @date     2017-08-04
# @param    [string]                 [原目录地址]
# @param    [string]                 [新目录地址]
# @return   [dictionary|boolean]     [成功 True, 失败 字典]
def mg_mv(dir_address, new_dir_address) :
    (status, output) = commands.getstatusoutput('mv '+dir_address+' '+new_dir_address)
    if status != 0 :
        return business_return('目录重命名失败', -11, [], output)
    return True