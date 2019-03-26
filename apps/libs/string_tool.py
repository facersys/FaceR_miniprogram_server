# -*- coding: utf-8 -*-

import json


def str2json(item):
    return json.loads(json.dumps(item, ensure_ascii=False))


def get_gender_num(gender):
    """获取性别"""
    g = gender.strip()
    return 1 if g == '男' else 2 if g == '女' else 0
