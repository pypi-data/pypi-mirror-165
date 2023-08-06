#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time, datetime
import jwt

from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    MissingRequiredClaimError,
)
HS256 = "HS256"
default_headers = {"alg": HS256}

class JwtToken(object):

    def __init__(self, secret, exp=3600, algorithm=None, headers=None):
        self.secret = secret    # key
        self.exp = exp      # 小于等于0时，不过期
        self.algorithm = algorithm or HS256
        self.headers = headers or default_headers

    def encode(self, payload):
        return jwt.encode(self._get_payload(payload), self.secret, self.algorithm, self.headers)

    def decode(self, token):
        try:
            payloay = jwt.decode(token, self.secret, self.algorithm)
            return payloay
        except ExpiredSignatureError as e:
            return False
        except Exception as e:
            return {}

    def is_expire(self, token):
        """
        是否过期
        """
        if self.decode(token) is False:
            return True
        else:
            return False

    def get_expire(self, token):
        """
        获取到期时间戳
        """
        payload = self.decode(token)
        if payload:
            return payload["exp"]

    def is_validate(self, token):
        """
        是否合法
        """
        if self.decode(token):
            return True
        else:
            return False

    def refresh_token(self, token):
        """
        刷新token，仅支持带有效期的token
        """
        payload = self.decode(token)
        if not payload:
            raise Exception("token无效或已过期")
        if not payload.get("exp"):
            raise Exception("该token是永久的，无需刷新")
        return self.encode(payload)

    def _get_payload(self, payload):
        if not isinstance(payload, dict):
            payload = {"data": payload}
        if "exp" in payload:
            exp = payload["exp"]
            if isinstance(exp, int):
                if exp:
                    payload.update({"exp": int(time.time()) + exp})
                else:
                    payload.pop("exp")
        elif self.exp:
            payload.update({"exp": int(time.time()) + self.exp})
        return payload

if __name__ == '__main__':
    import json, datetime
    t = JwtToken("f465ca164f0e", 3600)
    # token = t.encode({"uid": 54887111})
    # 指定有效期为12小时
    # token = t.encode({"uid": 54887111, "exp": 3600*12})
    # 指定2022-09-06 08:00:00到期
    token = t.encode({"uid": 54887111, "exp": datetime.datetime.fromordinal(datetime.datetime.today().toordinal()) + datetime.timedelta(days=7)})
    print(token)
    print(t.decode(token))
    print(t.is_expire(token))
    print(t.is_validate(token))
    print(t.refresh_token(token))
    print(t.get_expire(token))
