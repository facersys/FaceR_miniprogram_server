# -*- coding: utf-8 -*-

import shortuuid
from flask import request
from apps.Config import getConfig
from apps.Interface import api
from apps.Library import log, mongo, qiniu
from apps.Library.FaceTools import FaceTool
from apps.Library.ReturnResponse import _Return_Post, _Return_Error_Post
from apps.Library.ReturnStatus import USERID_LOST, UNKNOWN_ERROR, FACE_LOST
from apps.Moduel.MongoDB.user import UserModel as UserModelMongo


@api.route('/face', methods=['POST'])
def face():
    """
    获取人脸编码
    """
    face_stream = request.files.get('face').read()
    face_code = FaceTool(face_stream).encode()
    if not face_code:
        log.logger.info('获取人脸编码失败，照片上不存在人脸')
        return _Return_Error_Post(code=FACE_LOST, message='获取人脸编码失败，照片上不存在人脸')

    log.logger.info('获取人脸编码成功')
    return _Return_Post(data=face_code, message='获取人脸编码成功')


@api.route('/update_face', methods=['POST'])
def upload_face():
    """
    用户更新人脸
    :return:
    """
    uid = request.form.get('uid', None)

    if not uid:
        log.logger.warning('更新人脸，缺少用户ID')
        return _Return_Error_Post(code=USERID_LOST, message='缺少用户id')

    user_collection = getConfig('mongodb', 'user_collection')

    # 获取人脸编码
    face_stream = request.files.get('face').read()
    face_code = FaceTool(face_stream).encode()

    if not face_code:
        log.logger.info('获取人脸编码失败，照片上不存在人脸')
        return _Return_Error_Post(code=FACE_LOST, message='获取人脸编码失败，照片上不存在人脸')

    # 保存人脸照片到七牛云
    filename = f'{uid}-{shortuuid.uuid()}.png'
    qiniu.upload_file(filename, face_stream)

    if not mongo.select_one(user_collection, {'uid': uid}):
        # 不存在用户
        if mongo.insert(user_collection, UserModelMongo(uid, face_code).get(), ['uid']):
            data = {
                'uid': uid,
                'face': face_code
            }
            log.logger.info('更新人脸成功 %s' % uid)
            return _Return_Post(data=data, message='更新人脸数据成功')
    else:
        # 更新人脸
        if mongo.update(user_collection, {'uid': uid}, UserModelMongo(uid, face_code).get()):
            log.logger.info('更新人脸成功 %s' % uid)
            return _Return_Post(data=uid, message='更新人脸数据成功')
        else:
            log.logger.warning('更新人脸失败')
            return _Return_Error_Post(code=UNKNOWN_ERROR, message='更新人脸失败')


