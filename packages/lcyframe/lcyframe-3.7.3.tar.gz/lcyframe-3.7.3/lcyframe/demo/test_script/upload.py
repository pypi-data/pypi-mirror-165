#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random, string
from test_script import *
from lcyframe.libs import cprint, utils


def post_authorization(*args, **kwargs):
    """
    签发授权:授权开通使用某个服务、套餐。开通后，分自动激活和客户邮件连接激活
    
    参数:
    - company_id # 必填, ,int,客户id
    - product_id # 必填, ,int,产品id
    - service_life # 必填, ,int,授权时长，即产品有效期，单位天
    - domain_name_list # 必填, ,json,授权主域列表
    - active_mode # 必填, ,int,激活方式, 0直接激活，1邮件激活
    - email # 选填，,str,授权邮箱
    """
    headers = {}
    files = {}
    params = {
        "company_id": "(必填)客户id",
        "product_id": "(必填)产品id",
        "service_life": "(必填)授权时长，即产品有效期，单位天",
        "domain_name_list": "(必填)授权主域列表",
        "active_mode": "(必填)激活方式, 0直接激活，1邮件激活",
        "email": "(选填)授权邮箱",
        }
    return send(methed="post", url="/authorization", params=params, headers=headers, files=files)

def get_authorization(*args, **kwargs):
    """
    详情:
    
    参数:
    - id # 必填, ,int,id
    """
    headers = {}
    files = {}
    params = {
        "id": "(必填)id",
        }
    return send(methed="get", url="/authorization", params=params, headers=headers, files=files)

def put_authorization(*args, **kwargs):
    """
    编辑:
    
    参数:
    - id # 必填, ,int,记录id
    - service_list # 选填，,json,服务条目
    - domain_name_list # 选填，,json,授权域名
    - service_end # 选填，,datetime,到期时间
    """
    headers = {}
    files = {}
    params = {
        "id": "(必填)记录id",
        "service_list": "(选填)服务条目",
        "domain_name_list": "(选填)授权域名",
        "service_end": "(选填)到期时间",
        }
    return send(methed="put", url="/authorization", params=params, headers=headers, files=files)

def delete_authorization(*args, **kwargs):
    """
    删除:删除记录
    
    参数:
    - id # 必填, ,int,记录id
    """
    headers = {}
    files = {}
    params = {
        "id": "(必填)记录id",
        }
    return send(methed="delete", url="/authorization", params=params, headers=headers, files=files)


def get_authorization_list(*args, **kwargs):
    """
    授权列表:
    
    参数:
    - page # 选填，,integer,翻页码
    - count # 选填，,integer,每页显示条数
    - auth_state # 选填，,int,授权状态：0待激活，1已激活，2已过期
    - search # 选填，,str,搜索授权客户名称或产品名称等关键字查询
    - order_key # 选填，,str,排序字段,service_end=-1
    """
    headers = {}
    files = {}
    params = {
        "page": "(选填)翻页码",
        "count": "(选填)每页显示条数",
        "auth_state": "(选填)授权状态：0待激活，1已激活，2已过期",
        "search": "(选填)搜索授权客户名称或产品名称等关键字查询",
        "order_key": "(选填)排序字段,service_end=-1",
        }
    return send(methed="get", url="/authorization/list", params=params, headers=headers, files=files)


if __name__ == "__main__":
    # 签发授权
    post_authorization()
    # 详情
    get_authorization()
    # 编辑
    put_authorization()
    # 删除
    delete_authorization()
    # 授权列表
    get_authorization_list()
    