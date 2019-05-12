# -*- coding: utf-8 -*-

from flask import request
from datetime import datetime
from apps.Interface import api
from apps.Library import db
from apps.Library import log
from apps.Library.ReturnResponse import _Return_Error_Post, _Return_Post
from apps.Library.ReturnStatus import NOTICE_LOST_PARAM, NOTICE_NOT_FOUND, NOTICEID_LOST
from apps.Moduel.MySQL.user import UserModel
from apps.Moduel.MySQL.notice import NoticeModel


@api.route('/notice', methods=["GET", "POST", "PUT", "DELETE"])
def notice():
    """发送通知
    {
        "target": "0" 0: 全体用户, uid: 某个用户
        "title": title
        "content": 内容
    }
    """
    rbody = request.json or {}

    if request.method == "POST":
        # 发送通知

        target = rbody.get('target', None)
        title = rbody.get("title", None)
        content = rbody.get("content", None)

        # 参数不完整
        if not bool(target and title and content):
            log.logger.warning("发送通知失败，缺少参数")
            return _Return_Error_Post(code=NOTICE_LOST_PARAM, message='发送通知失败，缺少参数')

        # 判断发送类型
        if target == "0":
            # 发给全体
            users = UserModel.query.all()
            for user in users:
                new_notice = NoticeModel(title=title, content=content, user_id=user.id)
                db.session.add(new_notice)
                db.session.flush()
        else:
            # 发给个人
            user = UserModel.query.get(target)
            new_notice = NoticeModel(title=title, content=content, user_id=user.id)
            db.session.add(new_notice)
            db.session.flush()

        log.logger.info("通知发送成功" + target)
        return _Return_Post(data=target, message='通知发送成功')

    elif request.method == 'DELETE':
        # 删除通知

        nid = rbody.get('nid', None)

        if not nid:
            log.logger.warning('删除通知，缺少通知ID')
            return _Return_Error_Post(code=NOTICEID_LOST, message='缺少通知id')

        need_delete_notice = NoticeModel.query.get(nid)

        # 判断用户是否存在
        if not need_delete_notice:
            log.logger.warning('通知不存在')
            return _Return_Error_Post(code=NOTICE_NOT_FOUND, message='通知不存在')

        db.session.delete(need_delete_notice)
        db.session.commit()

        log.logger.info("删除通知成功: %s" % nid)
        return _Return_Post(data=nid, message='删除通知成功')

    elif request.method == 'GET':
        # 获取通知详细内容

        nid = rbody.get('nid', None)

        if not nid:
            log.logger.warning('缺少通知id')
            return _Return_Error_Post(code=NOTICEID_LOST, message='缺少通知id')

        query_notice = NoticeModel.query.get(nid)

        # 判断用户是否存在
        if not query_notice:
            log.logger.warning('通知不存在')
            return _Return_Error_Post(code=NOTICE_NOT_FOUND, message='通知不存在')

        data = {
            "nid": query_notice.id,
            "title": query_notice.title,
            "content": query_notice.content,
            "is_read": query_notice.is_read
        }
        log.logger.info("查询通知成功: %s" % nid)
        return _Return_Post(data=data, message='查询通知成功')

    elif request.method == 'PUT':
        # 更新通知内容

        nid = rbody.get('nid', None)

        if not nid:
            log.logger.warning('缺少通知id')
            return _Return_Error_Post(code=NOTICEID_LOST, message='缺少通知id')

        need_update_notice = NoticeModel.query.get(nid)

        # 判断用户是否存在
        if not need_update_notice:
            log.logger.warning('通知不存在')
            return _Return_Error_Post(code=NOTICE_NOT_FOUND, message='通知不存在')

        need_update_notice.title = rbody.get('title', need_update_notice.title)
        need_update_notice.content = rbody.get('content', need_update_notice.content)
        need_update_notice.is_read = rbody.get('is_read', need_update_notice.is_read)
        need_update_notice.update_time = datetime.now()

        db.session.add(need_update_notice)
        db.session.commit()

        log.logger.info("更新通知成功: %s" % nid)
        return _Return_Post(data=nid, message='更新通知成功')


