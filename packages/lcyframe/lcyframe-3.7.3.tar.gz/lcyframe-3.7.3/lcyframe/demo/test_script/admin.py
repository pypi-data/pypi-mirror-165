#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random, string
from test_script import *
from lcyframe.libs import cprint, utils


def get_admin_member(*args, **kwargs):
    """
    无说明:
    
    参数:
    - uid # 必填, ,int,uid
    """
    headers = {}
    files = {}
    params = {
        "uid": "(必填)uid",
        }
    return send(methed="get", url="/admin/member", params=params, headers=headers, files=files)

def post_admin_member(*args, **kwargs):
    """
    无说明:
    
    参数:
    - user_name # 必填, ,str,
    - pass_word # 必填, ,str,无说明，无说明
    - nick_name # 必填, ,str,
    - sex # 必填, ,int,1 无说明 0 无说明
    - mobile # 必填, ,str,无说明
    - email # 必填, ,str,无说明
    - gid # 必填, ,int,无说明 1 无说明 2 无说明
    """
    headers = {}
    files = {}
    params = {
        "user_name": "(必填)无描述",
        "pass_word": "(必填)无说明，无说明",
        "nick_name": "(必填)无描述",
        "sex": "(必填)1 无说明 0 无说明",
        "mobile": "(必填)无说明",
        "email": "(必填)无说明",
        "gid": "(必填)无说明 1 无说明 2 无说明",
        }
    return send(methed="post", url="/admin/member", params=params, headers=headers, files=files)

def put_admin_member(*args, **kwargs):
    """
    无说明:
    
    参数:
    - uid # 必填, ,int,
    - nick_name # 选填，,str,
    - sex # 选填，,int,1 无说明 0 无说明
    - mobile # 选填，,str,无说明
    - email # 选填，,str,无说明
    - gid # 选填，,int,无说明 1 无说明 2 无说明
    """
    headers = {}
    files = {}
    params = {
        "uid": "(必填)无描述",
        "nick_name": "(选填)无描述",
        "sex": "(选填)1 无说明 0 无说明",
        "mobile": "(选填)无说明",
        "email": "(选填)无说明",
        "gid": "(选填)无说明 1 无说明 2 无说明",
        }
    return send(methed="put", url="/admin/member", params=params, headers=headers, files=files)

def delete_admin_member(*args, **kwargs):
    """
    无说明:
    
    参数:
    - uid # 选填，,int,uid
    """
    headers = {}
    files = {}
    params = {
        "uid": "(选填)uid",
        }
    return send(methed="delete", url="/admin/member", params=params, headers=headers, files=files)


def post_admin_login(*args, **kwargs):
    """
    登录:
    
    参数:
    - user_name # 必填, ,str,用户名
    - pass_word # 必填, ,str,密码
    """
    headers = {}
    files = {}
    params = {
        "user_name": "(必填)用户名",
        "pass_word": "(必填)密码",
        }
    return send(methed="post", url="/admin/login", params=params, headers=headers, files=files)


def post_admin_resetpwd(*args, **kwargs):
    """
    忘记密码:
    
    参数:
    - pass_word # 必填, ,str,旧密码
    - 新密码 # 必填, ,str,无说明
    """
    headers = {}
    files = {}
    params = {
        "pass_word": "(必填)旧密码",
        "新密码": "(必填)无说明",
        }
    return send(methed="post", url="/admin/resetpwd", params=params, headers=headers, files=files)


def post_admin_find(*args, **kwargs):
    """
    无说明:无说明（无说明）
    
    参数:
    - page # 必填, ,str,无说明
    """
    headers = {}
    files = {}
    params = {
        "page": "(必填)无说明",
        }
    return send(methed="post", url="/admin/find", params=params, headers=headers, files=files)

def get_admin_find(*args, **kwargs):
    """
    无说明:无说明
    """
    headers = {}
    files = {}
    params = {
        }
    return send(methed="get", url="/admin/find", params=params, headers=headers, files=files)


if __name__ == "__main__":
    # 无说明
    get_admin_member()
    # 无说明
    post_admin_member()
    # 无说明
    put_admin_member()
    # 无说明
    delete_admin_member()
    # 登录
    post_admin_login()
    # 忘记密码
    post_admin_resetpwd()
    # 无说明
    post_admin_find()
    # 无说明
    get_admin_find()
    