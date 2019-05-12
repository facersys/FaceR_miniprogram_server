# -*- coding: utf-8 -*-

import os
from apps.Log.Logger import Logger

# 项目根路径
root_path = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]

log = Logger(
    os.path.join(
        root_path,
        'logs',
        'FaceR.log'
    ), level='debug'
)
