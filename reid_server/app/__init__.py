# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2019/10/22
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import os
from flask import Flask
from app.views import main_page
from app.api import api
from config import config
from app.models import *


def create_app(env='production'):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)
    # 导入配置文件
    app.config.from_object(config[env])
    # 数据库初始化
    db.init_app(app)
    ctx = app.app_context()
    ctx.push()
    # 注册蓝图
    app.register_blueprint(blueprint=main_page)
    app.register_blueprint(blueprint=api)
    return app
