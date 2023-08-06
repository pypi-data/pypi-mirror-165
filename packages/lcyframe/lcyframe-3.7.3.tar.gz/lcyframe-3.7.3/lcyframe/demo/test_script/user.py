#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random, string
from test_script import *
from lcyframe.libs import cprint, utils


def post_user(*args, **kwargs):
    """
    添加:测试post
    
    参数:
    - a # 必填, ,integer,角色id
    - b # 选填，,string,供应商id
    - c # 选填，,string,手机号
    - d # 选填，,int,城市全拼列表
    - pic # 选填，,file,文件
    """
    headers = {}
    files = {}
    # 文件
    files["pic"] = open("../请指定文件路径")
    
    params = {
        "a": "(必填)角色id",
        "b": "(选填)供应商id",
        "c": "(选填)手机号",
        "d": "(选填)城市全拼列表",
        }
    return send(methed="post", url="/user", params=params, headers=headers, files=files)

def get_user(*args, **kwargs):
    """
    查看:测试get
    
    参数:
    - a # 必填, ,integer,角色id
    - b # 选填，,string,供应商id
    - d # 选填，,int,城市全拼列表
    """
    headers = {}
    files = {}
    params = {
        "a": "(必填)角色id",
        "b": "(选填)供应商id",
        "d": "(选填)城市全拼列表",
        }
    return send(methed="get", url="/user", params=params, headers=headers, files=files)


def post_user_list(*args, **kwargs):
    """
    添加:测试post
    
    参数:
    - a # 必填, ,integer,角色id
    - b # 选填，,string,供应商id
    - c # 选填，,string,手机号
    - d # 选填，,int,城市全拼列表
    - pic # 选填，,file,文件
    """
    headers = {}
    files = {}
    # 文件
    files["pic"] = open("../请指定文件路径")
    
    params = {
        "a": "(必填)角色id",
        "b": "(选填)供应商id",
        "c": "(选填)手机号",
        "d": "(选填)城市全拼列表",
        }
    return send(methed="post", url="/user_list", params=params, headers=headers, files=files)

def get_user_list(*args, **kwargs):
    """
    查看:测试get
    
    参数:
    - a # 必填, ,integer,角色id
    - b # 选填，,string,供应商id
    - d # 选填，,int,城市全拼列表
    """
    headers = {}
    files = {}
    params = {
        "a": "(必填)角色id",
        "b": "(选填)供应商id",
        "d": "(选填)城市全拼列表",
        }
    return send(methed="get", url="/user_list", params=params, headers=headers, files=files)


if __name__ == "__main__":
    # 添加
    post_user()
    # 查看
    get_user()
    # 添加
    post_user_list()
    # 查看
    get_user_list()
    