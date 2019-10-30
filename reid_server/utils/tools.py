# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2019/10/24
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import numpy as np
import base64
from io import BytesIO
from PIL import Image


def embed2str(feats):
    return feats.tostring()


def str2embed(str_):
    return np.fromstring(str_,dtype=np.float32)


def decode_image(data):
    data = data.replace(" ", "+")
    try:
        im = Image.open(BytesIO(base64.b64decode(data)))
    except:
        im = None
    return im
