# -*- encoding: utf-8 -*-
"""
@File    : apiResult.py.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from flask import jsonify, abort
import flask_restful
from app.tools.errors import *


def custom_abord(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        abort(400, ab_enum(BaseEnum.Bad_Request))
    if http_status_code == 401:
        abort(ab_enum(BaseEnum.NOT_AUTHORIZED))
    if http_status_code == 403:
        abort(ab_enum(BaseEnum.FORBIDDEN))
    if http_status_code == 500:
        abort(500,ab_enum(BaseEnum.ServerError))
    abort(http_status_code)


flask_restful.abort = custom_abord


# 返回格式
def generate_response(code=BaseEnum.SUCCESS.value[0], message=BaseEnum.SUCCESS.value[1], results=None):
    result = {
        "code": code,
        "msg": message,
        "results": results,
    }
    if not result['results']:
        result.pop('results')
        return jsonify(result)
    return jsonify(result)
