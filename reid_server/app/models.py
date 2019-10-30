# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class ImageInfo(db.Model):
    __tablename__ = 'image'
    image_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String(80), unique=True)
    class_id = db.Column(db.INTEGER, db.ForeignKey('class_info.class_id'))
    cid = db.Column(db.INTEGER, db.ForeignKey('camera_info.cid'))
    annoy_index = db.Column(db.String(80), unique=True, nullable=False)
    time = db.Column(db.DateTime(80), nullable=False)


class ClassInfo(db.Model):
    __tablename = 'class_info'
    class_id = db.Column(db.INTEGER, primary_key=True)
    class_name = db.Column(db.String(80), nullable=False)


class CameraInfo(db.Model):
    __tablename = 'camera_info'
    cid = db.Column(db.INTEGER, primary_key=True)
    cam_name = db.Column(db.String(80), nullable=False)
    ip_addr = db.Column(db.String(80), nullable=False)


class User(db.Model):
    """User"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        """called on get password attributes"""
        raise AttributeError('not readable')

    @password.setter
    def password(self, passwd):
        """called on set password attributes , set encrypted password"""
        self.password_hash = generate_password_hash(passwd)

    def check_password(self, passwd):
        """check password correctness"""
        return check_password_hash(self.password_hash, passwd)


class AdminUser(db.Model):
    """User"""
    __tablename__ = "admin_users"
    admin_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_name = db.Column(db.String(32), db.ForeignKey('users.user_name'))


def add_image(image_path, class_id, cid, annoy_index, time):
    image_db = ImageInfo()
    image_db.image_path = image_path
    image_db.cid = cid
    image_db.time = time
    image_db.class_id = class_id
    image_db.annoy_index = annoy_index
    # 将新创建的用户添加到数据库会话中
    db.session.add(image_db)
    # 将数据库会话中的变动提交到数据库中, 记住, 如果不 commit, 数据库中是没有变化的.
    db.session.commit()


def del_image(image_id):
    image = ImageInfo.query.filter_by(id=image_id).first()
    # 将新创建的用户添加到数据库会话中
    db.session.delete(image)
    # 将数据库会话中的变动提交到数据库中, 记住, 如果不 commit, 数据库中是没有变化的.
    db.session.commit()


def add_class(class_id, class_name):
    # 添加新类
    class_db = ClassInfo()
    class_db.class_id = class_id
    class_db.class_name = class_name
    db.session.add(class_db)
    db.session.commit()


def del_class(class_id):
    # 删除类
    class_item = ClassInfo.query.filter_by(class_id=class_id).first()
    db.session.delete(class_item)
    db.session.commit()


def add_camera(camera_id, cam_name, ip_addr):
    camera_db = CameraInfo()
    camera_db.camera_id = camera_id
    camera_db.cam_name = cam_name
    camera_db.ip_addr = ip_addr
    db.session.add(camera_db)
    db.session.commit()


def del_camera(camera_id, cam_name, ip_addr):
    camera_db = CameraInfo()
    camera_db.camera_id = camera_id
    camera_db.cam_name = cam_name
    camera_db.ip_addr = ip_addr
    db.session.add(camera_db)
    db.session.commit()


def select_image_by_annoy(annoy_index):
    image = ImageInfo.query.filter(ImageInfo.annoy_index==annoy_index).first()
    return image


def select_image_by_id(image_id):
    image = ImageInfo.query.filter(ImageInfo.image_id==image_id).first()
    return image


def select_image_by_path(path):
    image = ImageInfo.query.filter(ImageInfo.image_path==path).first()
    return image
