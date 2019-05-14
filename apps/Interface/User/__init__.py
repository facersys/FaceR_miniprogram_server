# -*- coding: utf-8 -*-

from flask import request
from datetime import datetime
from apps.Library import db, log
from apps.Interface import api
from apps.Library.ReturnResponse import _Return_Post, _Return_Error_Post
from apps.Library.ReturnStatus import USERID_LOST, USER_EXISTS, USER_NOT_FOUND
from apps.Moduel.MySQL.user import UserModel
from apps.Config.Others import DEFAULT_AVATAR


@api.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    """
    用户接口
    GET: 查, POST: 增, PUT: 改, DELETE: 删
    """
    rbody = request.json or {}

    if request.method == 'POST':
        # 新增用户(用户不存在则创建)

        name = rbody.get('name', None)
        gender = rbody.get('gender', 0)
        grade = rbody.get('grade', None)
        major = rbody.get('major', None)
        class_name = rbody.get('class_name', None)
        face_url = rbody.get('face_url', None)
        email = rbody.get('email', None)
        openid = rbody.get('openid', None)
        unionid = rbody.get('unionid', None)
        is_bind_jw = rbody.get('is_bind_jw', False)
        avatar = rbody.get('avatar', DEFAULT_AVATAR)
        city = rbody.get('city', None)
        province = rbody.get('province', None)

        # 查找用户
        find_user = UserModel.query.filter(UserModel.unionid == unionid).first()
        if find_user:
            log.logger.info("用户已存在")
            return _Return_Error_Post(code=USER_EXISTS, message='用户已经存在')

        # 用户不存在，创建新用户
        new_user = UserModel(
            name=name,
            gender=gender,
            grade=grade,
            major=major,
            class_name=class_name,
            face_url=face_url,
            email=email,
            openid=openid,
            unionid=unionid,
            is_bind_jw=is_bind_jw,
            avatar=avatar,
            city=city,
            province=province
        )

        # 创建用户
        db.session.add(new_user)
        # 这里采用flush，记得在配置文件中使SQLALCHEMY_COMMIT_ON_TEARDOWN为True
        # 使用commit无法得到插入的id
        db.session.flush()

        log.logger.info("新增用户成功" + new_user.id)
        return _Return_Post(data=new_user.id, message='新增用户成功')

    elif request.method == 'DELETE':
        # 删除用户

        uid = rbody.get('uid', None)

        if not uid:
            log.logger.warning('删除用户，缺少用户ID')
            return _Return_Error_Post(code=USERID_LOST, message='缺少用户id')

        need_delete_user = UserModel.query.get(uid)

        # 判断用户是否存在
        if not need_delete_user:
            log.logger.warning('用户不存在')
            return _Return_Error_Post(code=USER_NOT_FOUND, message='用户不存在')

        db.session.delete(need_delete_user)
        db.session.commit()

        log.logger.info("删除用户成功" + uid)
        return _Return_Post(data=uid, message='删除用户成功')

    elif request.method == 'GET':
        uid = rbody.get('uid', None)

        if not uid:
            log.logger.warning('获取用户信息，缺少用户ID')
            return _Return_Error_Post(code=USERID_LOST, message='缺少用户id')

        query_user = UserModel.query.get(uid)

        # 判断用户是否存在
        if not query_user:
            log.logger.warning('用户不存在')
            return _Return_Error_Post(code=USER_NOT_FOUND, message='用户不存在')

        data = query_user.get_json()
        log.logger.info("查询用户成功" + uid)
        return _Return_Post(data=data, message='查询用户成功')

    elif request.method == 'PUT':
        uid = rbody.get('uid', None)

        if not uid:
            log.logger.warning('更新用户信息，缺少用户ID')
            return _Return_Error_Post(code=USERID_LOST, message='缺少用户id')

        need_update_user = UserModel.query.get(uid)

        # 判断用户是否存在
        if not need_update_user:
            log.logger.warning('用户不存在')
            return _Return_Error_Post(code=USER_NOT_FOUND, message='用户不存在')

        need_update_user.name = rbody.get('name', need_update_user.name)
        need_update_user.gender = rbody.get('gender', need_update_user.gender)
        need_update_user.grade = rbody.get('grade', need_update_user.grade)
        need_update_user.major = rbody.get('major', need_update_user.major)
        need_update_user.class_name = rbody.get('class_name', need_update_user.class_name)
        need_update_user.face_url = rbody.get('face_url', need_update_user.face_url)
        need_update_user.email = rbody.get('email', need_update_user.email)
        need_update_user.is_bind_jw = rbody.get('is_bind_jw', need_update_user.is_bind_jw)
        need_update_user.avatar = rbody.get('avatar', need_update_user.avatar)
        need_update_user.city = rbody.get('city', need_update_user.city)
        need_update_user.province = rbody.get('province', need_update_user.province)
        need_update_user.update_time = datetime.now()

        db.session.add(need_update_user)
        db.session.commit()

        log.logger.info("更新用户成功" + uid)
        return _Return_Post(data=uid, message='更新用户成功')
