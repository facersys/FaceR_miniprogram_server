# -*- coding: utf-8 -*-

from flask import request

from apps.Config import getConfig
from apps.Interface import api
from apps.Library import log, mongo
from apps.Library.ReturnResponse import _Return_Error_Post, _Return_Post
from apps.Library.ReturnStatus import JW_LOST_PARAM, JW_ACCOUNT_ERROR, USER_NOT_FOUND, JW_FAILURE
from apps.Library.Stbu import Stbu
from apps.Library.StringTools import get_gender_num

from apps.Moduel.MySQL.user import UserModel as UserModelMySQL
from apps.Moduel.MongoDB.user import UserModel as UserModelMongo


@api.route('/stbu', methods=["POST"])
def stbu():
    """同步教务系统"""
    rbody = request.json or {}

    uid = rbody.get('uid', None)
    user = rbody.get('u', None)
    pwd = rbody.get('p', None)

    if not bool(uid and user and pwd):
        log.logger.warning('绑定教务系统缺少参数')
        return _Return_Error_Post(code=JW_LOST_PARAM, message='绑定教务系统缺少参数')

    # 开始同步，获取用户信息
    s = Stbu(rbody.get("u"), rbody.get("p"))
    stbu_user = s.sync()

    if stbu_user and (stbu_user != 0):
        # 把用户放到数据库里
        need_update_user = UserModelMySQL.query.get(uid)

        if not need_update_user:
            log.logger.warning('用户不存在')
            return _Return_Error_Post(code=USER_NOT_FOUND, message='用户不存在')

        # 更新用户信息 -> MySQL
        need_update_user.sid = stbu_user.get('sid')
        need_update_user.name = stbu_user.get('name')
        need_update_user.gender = get_gender_num(stbu_user.get('gender'))
        need_update_user.grade = stbu_user.get('grade')
        need_update_user.major = stbu_user.get('major')
        need_update_user.grade = stbu_user.get('grade')
        need_update_user.class_name = stbu_user.get('class_name')
        need_update_user.college = stbu_user.get('college')
        need_update_user.email = stbu_user.get('email')
        need_update_user.phone = stbu_user.get('phone')
        need_update_user.face_url = getConfig('qiniu', 'domain') + "/" + stbu_user.get('face_url')
        need_update_user.is_bind_jw = True

        # 更新用户信息 -> MongoDB
        user_collection = getConfig('mongodb', 'user_collection')

        if not mongo.select_one(user_collection, {'uid': uid}):
            # 不存在则创建
            if mongo.insert(user_collection, UserModelMongo(uid, stbu_user.get('face')).get(), ['uid']):
                log.logger.info('绑定教务成功: %s' % uid)
                return _Return_Post(data=uid, message='绑定教务系统成功')
            else:
                log.logger.warning('绑定教务系统失败，在插入人脸数据出出错')
                return _Return_Error_Post(code=JW_FAILURE, message='账户或密码错误')
        else:
            # 存在则更新
            if mongo.update(user_collection, {'uid': uid}, UserModelMongo(uid, stbu_user.get('face')).get()):
                log.logger.info('绑定教务成功: %s' % uid)
                return _Return_Post(data=uid, message='绑定教务系统成功')
            else:
                log.logger.warning('绑定教务系统失败，在更新人脸数据出出错')
                return _Return_Error_Post(code=JW_FAILURE, message='账户或密码错误')
    else:
        log.logger.warning('绑定教务系统账户或密码错误')
        return _Return_Error_Post(code=JW_ACCOUNT_ERROR, message='账户或密码错误')
