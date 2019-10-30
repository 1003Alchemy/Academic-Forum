# -*- encoding: utf-8 -*-
"""
@File    : util.py
@Time    : 2019/10/22
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import flask_restful
from flask import Flask, abort
from flask import jsonify
import base64
from io import BytesIO
import re
from PIL import Image


# def generate_response(results=None, code=Code.SUCCESS):
#     print(jsonify({"code": code, "msg": Code.msg[code], "results": results}))
#     return jsonify({"code": code, "msg": Code.msg[code], "results": results})


def decode_image(data):
    data = data.replace(" ", "+")
    try:
        im = Image.open(BytesIO(base64.b64decode(data)))
    except:
        im = None
    return im


def is_base64(data):
    data = data.replace(" ", "+")
    base64_non_alphabet_re = re.compile(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$')
    if base64_non_alphabet_re.search(data):
        return True
    else:
        return False


def upload_image():
    # 插入图像
    return 0
