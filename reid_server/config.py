# -*- encoding: utf-8 -*-
"""
@File    : config.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = r"%S-D*d\uk/j@51.65!_?"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 5
    CNN_MODEL_PATH = "static/model.pth"


class ProductionConfig(Config):
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'Zzz123456.'
    HOST = '10.5.100.49'
    PORT = '3306'
    DATABASE = 'reid'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)



class DevelopementConfig(Config):
    """开发模式的配置信息"""

    BEBUG = True


config = {
    'testing': ProductionConfig,
    'develope': DevelopementConfig,
    'production': ProductionConfig,
}
