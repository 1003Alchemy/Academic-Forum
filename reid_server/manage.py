# -*- encoding: utf-8 -*-
"""
@File    : manage.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from flask_script import Manager
from flask_migrate import Migrate
from app import create_app, db
app = create_app()

migrate = Migrate(app, db)
manager = Manager(app=app)
if __name__ == '__main__':
    manager.run()
