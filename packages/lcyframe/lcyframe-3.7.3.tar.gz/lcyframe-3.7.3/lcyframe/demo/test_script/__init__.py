
import os, sys
import re, requests
import logging
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

from context import InitContext
from lcyframe.libs.singleton import MongoCon
from lcyframe.libs.cprint import cprint
from lcyframe.libs.JWT import JwtToken
from utils import helper

HEARDERS = {}
token = ""
config = InitContext.get_context()
# db = MongoCon().get_database(**config["mongo_config"])

def gen_token(user_id):
    return JwtToken(config["token_config"]["secret"]).encode({"user_id": user_id})

def login(account=None, password=None):
    headers = {"token": "******"}
    return send(
        "post",
        "/login",
        {
            # "account": account or "'yourname' or '1=1';",    # 注入攻击测试
            "account": account or "yourname",
            "password": password or "123456!",
        },
        headers=headers
    )

def send(methed, url, params, **kwargs):

    if "/" not in url:
        url = "/" + url

    global HEARDERS, token
    if "headers" not in kwargs:
        kwargs["headers"] = HEARDERS
    else:
        HEARDERS.update(kwargs["headers"])
        kwargs["headers"] = HEARDERS

    if "token" not in kwargs["headers"]:
        response = login()
        if response["code"] != 0:
            raise Exception(response["msg"])
        user = response["data"]
        token = user["token"]
        user_id = user["user_id"]
        HEARDERS["user_id"] = user_id
        HEARDERS["token"] = token
        kwargs["headers"]["token"] = token
        kwargs["headers"]["user_id"] = user["user_id"]

    for k, v in kwargs["headers"].items():
        if isinstance(v, int):
            kwargs["headers"][k] = str(v)

    _url = config["wsgi"]["host"] #

    if "http" not in config["wsgi"]["host"]:
        _url = "http://" + _url + ":" + str(config["wsgi"]["port"])
    elif "127.0.0.1" in _url:
        _url = config["wsgi"]["host"] + ":" + str(config["wsgi"]["port"])
    _url += url


    if methed == "delete":
        kwargs["data"] = params
        data = eval("requests.%s" % methed)(_url, **kwargs)
    else:
        data = eval("requests.%s" % methed)(_url, params, **kwargs)

    r = data.json()
    cprint(r)
    return r

def get(url, params, **kwargs):
    send("get", url, params, **kwargs)

def post(url, params, **kwargs):
    send("post", url, params, **kwargs)

def put(url, params, **kwargs):
    send("put", url, params, **kwargs)

def delete(url, params, **kwargs):
    send("delete", url, params, **kwargs)


