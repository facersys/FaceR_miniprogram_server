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

    # 注册蓝图
    register_blueprint(app, api)

    # 初始化应用
    # mongo.init_app(app)

    return app
