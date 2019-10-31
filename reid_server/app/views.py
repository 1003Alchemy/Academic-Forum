# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import uuid
import base64
from flask import render_template, request, jsonify
from flask import Blueprint
from PIL import Image
from io import BytesIO
from utils.annoy_search import AnnoySearch
from app.models import *
import utils.exts
import numpy as np
t = AnnoySearch()
t.load_annoy()

main_page = Blueprint('first', __name__)


@main_page.route('/', methods=['GET', 'POST'])
def home():
    payload = {'gae_mode': False}
    return render_template('editor.html', payload=payload)


@main_page.route('/hello/<name>')
def hello_man(name):
    print(name)
    print(type(name))
    return 'hello name:%s type:%s ' % (name, type(name))


@main_page.route('/helloint/<int:id>')
def hello_int(id):
    print(id)
    print(type(id))
    a = 'wanghaifei'
    return 'hello int:%s' % (id)


@main_page.route('/getfloat/<float:price>')
def hello_float(price):
    return 'float:%s' % price


@main_page.route('/getstr/<string:name>')
def hello_name(name):
    return 'string:%s' % name


@main_page.route('/getpath/<path:url_path>')  # 与string的区别是可以匹配到'/', 也是当做字符串返回, 而string则不行
def hello_path(url_path):
    return 'url_path:%s' % url_path


@main_page.route('/getuuid/')  # 必须加两个斜杠
def hello_get_uuid():
    a = uuid.uuid4()
    return str(a)


@main_page.route('/getbyuuid/<uuid:uuid>')  # 必须加两个斜杠
def hello_getby_uuid(uuid):
    return 'uu:%s' % uuid


@main_page.route('/Search', methods=["GET", 'POST'])
def search():
    image_url = request.form['image_url']
    # 解码base64
    image_data = base64.b64decode(image_url[22:])
    image_data = BytesIO(image_data)
    im=Image.open(image_data)
    im=im.convert('RGB')
    im.save('static/temp/temp2.jpg', 'JPEG')
    # # 获取图像特征
    feats = utils.exts.Inference_Tools.extract_feature_from_path('static/temp/temp2.jpg')
    idx = t.get_nns_by_vector(feats, 12)
    print(idx[0])
    print(select_image_by_annoy(ImageInfo,idx[0]))
    results = [select_image_by_annoy(ImageInfo,x).image_path for x in idx]
    return jsonify(results=results)


@main_page.route('/Quick', methods=['POST'])
def search_quick():
    return search()
