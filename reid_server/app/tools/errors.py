# -*- encoding: utf-8 -*-
"""
@File    : errors.py
@Time    : 2019/10/22
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from enum import Enum
class BaseEnum(Enum):
    SUCCESS = (200, 'success')
    Bad_Request = (400, '参数类型错误')
    NOT_AUTHORIZED = (401, '未登录-认证信息失败-令牌过期')
    FORBIDDEN = (403, '无权限')
    ServerError = (500, '服务器内部异常')


def ab_enum(data):
    code = data.value[0]
    msg = data.value[1]
    results = {}
    r = {
        "code": code,
        "msg": msg,
        "results": results,
    }
    return r
