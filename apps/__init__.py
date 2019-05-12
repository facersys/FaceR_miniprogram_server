# -*- coding: utf-8 -*-

from flask import Flask
from apps.api import api

__author__ = "YingJoy"


def register_blueprint(app, target):
    app.register_blueprint(target)


def create_app():
    app = Flask(__name__)

    # 导入配置文件
    app.config.from_object('apps.settings')
    app.config.from_object('apps.security')
    app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'

    # 注册蓝图
    register_blueprint(app, api)

    # 初始化应用
    # mongo.init_app(app)

    return app
