#!/usr/bin/env python
# -*- coding:utf-8 -*-
import webbrowser, os
from ..base import BaseHandler
import platform

from tornado.web import HTTPError, StaticFileHandler

class StaticHandler(BaseHandler):
    """
    static
    """
    def get(self, path):
        if not path:
            raise HTTPError(404)
        else:
            return StaticFileHandler.get(path)