# -*- coding: utf-8 -*-

import os

from aip import AipOcr

from apps.Config import getConfig
from apps.Library.MongoDBTools import MongoTools
from apps.Log.Logger import Logger
from apps.Library.QiniuTools import MyQiNiu
from flask_sqlalchemy import SQLAlchemy

# 项目根路径
root_path = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]

log = Logger(
    os.path.join(
        root_path,
        'logs',
        'FaceR.log'
    ), level='debug'
)

# SQLAlchemy
db = SQLAlchemy()

# MongoDB
mongo = MongoTools(
    getConfig('mongodb', 'db'),
    "mongodb://%s:%s@%s:%s" % (
        getConfig('mongodb', 'user'),
        getConfig('mongodb', 'pwd'),
        getConfig('mongodb', 'host'),
        getConfig('mongodb', 'port')
    )
)

# 七牛云
qiniu = MyQiNiu(
    access_key=getConfig('qiniu', 'access_key'),
    secret_key=getConfig('qiniu', 'secret_key'),
    bucket_name=getConfig('qiniu', 'bucket_name'),
    domain=getConfig('qiniu', 'domain')
)

# 百度API
aipOcr = AipOcr(
    getConfig('baidu-aip', 'app_id'),
    getConfig('baidu-aip', 'api_key'),
    getConfig('baidu-aip', 'secret_key')
)
