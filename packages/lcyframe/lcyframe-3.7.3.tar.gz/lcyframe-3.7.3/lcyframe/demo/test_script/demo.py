#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random, string
from test_script import *
from lcyframe.libs import cprint, utils


def post_demo(*args, **kwargs):
    """
    添加:测试post
    
    参数:
    - str # 选填，,string,描述
    - str # 选填，,string,手机号
    - int # 必填, ,integer,整形
    - float # 必填, ,float,浮点型
    - json # 必填, ,json,json格式
    - form-data # 选填，,json,位置：body_json，参数放在body内，以multipart/form-data方式，json格式。json类型的参数，设为非必须时，需提供默认值
    - form-data2 # 选填，,string,位置：body_json，参数放在body内，以multipart/form-data方式，json格式。json类型的参数，设为非必须时，需提供默认值
    - www-form # 选填，,string,位置：body_form，参数放在body表单内，以multipart/x-www-form-urlencoded方式提交。手机号正则限定
    - excel # 选填，,file,上传文件，参数放在body内，以multipart/form-data方式提交;excel=self.params["excel"]
    """
    headers = {}
    files = {}
    # 上传文件，参数放在body内，以multipart/form-data方式提交;excel=self.params["excel"]
    files["excel"] = open("../请指定文件路径")
    
    params = {
        "str": "(选填)描述",
        "str": "(选填)手机号",
        "int": "(必填)整形",
        "float": "(必填)浮点型",
        "json": "(必填)json格式",
        "form-data": "(选填)位置：body_json，参数放在body内，以multipart/form-data方式，json格式。json类型的参数，设为非必须时，需提供默认值",
        "form-data2": "(选填)位置：body_json，参数放在body内，以multipart/form-data方式，json格式。json类型的参数，设为非必须时，需提供默认值",
        "www-form": "(选填)位置：body_form，参数放在body表单内，以multipart/x-www-form-urlencoded方式提交。手机号正则限定",
        }
    return send(methed="post", url="/demo", params=params, headers=headers, files=files)

def get_demo(*args, **kwargs):
    """
    查看:测试get
    
    参数:
    - _id # 选填，,str,id
    - a # 必填, ,integer,角色id
    - b # 选填，,string,供应商id
    - d # 选填，,int,城市全拼列表
    """
    headers = {"token": "1111"}
    files = {}
    params = {
        # "_id": "(选填)id",
        "a": 1,
        # "b": "(选填)供应商id",
        # "d": "(选填)城市全拼列表",
        }
    return send(methed="get", url="/demo", params=params, headers=headers, files=files)


def get_demo_list(*args, **kwargs):
    """
    列表:
    
    参数:
    - page # 选填，,integer,翻页码
    - count # 选填，,integer,每页显示条数
    - search # 选填，,str,搜索关键字
    - search # 选填，,str,搜索关键字
    - state # 选填，,int,申请状态
    - time_range # 选填，,str,申请时间范围，逗号隔开。2020-12-12 12:12:12,2022-12-12 12:12:12
    """
    headers = {}
    files = {}
    params = {
        "page": "(选填)翻页码",
        "count": "(选填)每页显示条数",
        "search": "(选填)搜索关键字",
        "search": "(选填)搜索关键字",
        "state": "(选填)申请状态",
        "time_range": "(选填)申请时间范围，逗号隔开。2020-12-12 12:12:12,2022-12-12 12:12:12",
        }
    return send(methed="get", url="/demo/list", params=params, headers=headers, files=files)


if __name__ == "__main__":
    # 添加
    # post_demo()
    # 查看
    get_demo()
    # 列表
    # get_demo_list()
    