# -*- coding: utf-8 -*-

from flask import request

from apps.api import api
from apps.libs import mongo
from apps.libs.restful import success, params_error, server_error
from apps.libs.stbu import Stbu
from apps.libs.string_tool import str2json, get_gender_num
from apps.models.user import UserModel
from apps.security import MONGO_USER_COLLECTION


@api.route('/user', methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == "GET":
        oid = request.args.get('oid')
        tmp_user = mongo.select_one(MONGO_USER_COLLECTION, {'openid': oid})
        return success(data=tmp_user, message='查询成功') if tmp_user else params_error(message='未找到')

    elif request.method == "POST":
        rbody = request.json
        tmp_user = UserModel(**rbody)
        if tmp_user.save():
            return success(data=str2json(tmp_user.get), message='创建用户成功')
        else:
            return params_error('用户已经存在')

    elif request.method == "PUT":
        oid = request.args.get('oid')
        rbody = request.json

        tmp_user = mongo.select_one(MONGO_USER_COLLECTION, {'openid': oid})
        if not tmp_user:
            return params_error(message='用户不存在')

        for k, v in rbody.items():
            tmp_user[k] = v
        if mongo.update(MONGO_USER_COLLECTION, {'openid': oid}, tmp_user):
            return success(data=str2json(tmp_user), message='更新用户信息成功')
        else:
            return params_error('更新用户信息失败')

    elif request.method == 'DELETE':
        oid = request.args.get('oid')

        if mongo.delete(MONGO_USER_COLLECTION, {'openid': oid}):
            return success(message='注销成功')
        else:
            return server_error(message='注销失败')


@api.route('/sync_stbu', methods=["POST"])
def sync_stbu():
    """同步教务系统"""
    rbody = request.json

    s = Stbu(rbody.get("u"), rbody.get("p"))
    stbu_user = s.sync()
    if stbu_user == 0:
        return params_error(message='账户或密码错误')
    elif stbu_user:
        su = str2json(stbu_user.get)
        user = mongo.select_one(MONGO_USER_COLLECTION, {"openid": rbody.get('oid')})
        # 合并一下数据
        su['city'] = user.get('city')
        su['province'] = user.get('province')
        su['avatar'] = user.get('avatar')
        su['openid'] = user.get('openid')
        su['unionid'] = user.get('unionid')
        su['gender'] = get_gender_num(su.get('gender'))
        su['is_bind_jw'] = True

        # print(su)
        # 判断数据库是否存在该用户，存在则更新现有信息，不存在则新增用户
        if mongo.select_one(MONGO_USER_COLLECTION, {"openid": rbody.get('oid')}):
            # 去除_id
            su.pop('_id')
            mongo.update(MONGO_USER_COLLECTION, {"openid": rbody.get('oid')}, su)
        else:
            mongo.insert(MONGO_USER_COLLECTION, su)
        return success(data=su, message='同步成功')
    else:
        return params_error(message='账户或密码错误')
