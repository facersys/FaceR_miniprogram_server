# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from apps.Interface import api
from apps.Pages import pages
from apps.Library import db

__author__ = "YingJoy"


def create_app():
    app = Flask(__name__)

    # 导入配置文件
    app.config.from_object('apps.Config.FlaskSetting')

    # 注册蓝图
    app.register_blueprint(api)
    app.register_blueprint(pages)

    # 初始化应用
    CORS(app, resources=r'/*')
    db.init_app(app)

    return app
