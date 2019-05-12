# -*- coding: utf-8 -*-

from apps.Config import getConfig

DEBUG = True

TEMPLATES_AUTO_RELOAD = True

SERVER_NAME = "facer.yingjoy.cn"

FILE_ALLOWED = ['image/png', 'image/jpg', 'image/jpeg']

SECRET_KEY = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    getConfig('mysql', 'user'),
    getConfig('mysql', 'pwd'),
    getConfig('mysql', 'host'),
    getConfig('mysql', 'port'),
    getConfig('mysql', 'db')
)

