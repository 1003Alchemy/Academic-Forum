# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2019/10/22
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from .webapi import Search, Upload
from flask_restful import Api
from flask import Blueprint

api = Blueprint("api", __name__)  # 设置蓝图

resource = Api(api)
resource.add_resource(Search, "/api/search/")  # 设置路由
resource.add_resource(Upload, "/api/upload/")  # 设置路由
