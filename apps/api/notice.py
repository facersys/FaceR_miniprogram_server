# -*- coding: utf-8 -*-

from flask import request

from apps.api import api
from apps.libs import mongo
from apps.libs.restful import success
from apps.models.notice import NoticeModel
from apps.security import MONGO_USER_COLLECTION, MONGO_NOTICE_COLLECTION


@api.route('/notice', methods=["POST", "PUT"])
def notice():
    """发送通知
    {
        "t": "0" 0: 全体用户, uid: 某个用户
        "title": title
        "content": 内容
    }
    """
    rbody = request.json

    if request.method == "POST":
        to = rbody.get('t')
        title = rbody.get("title")
        content = rbody.get("content")

        if to == "0":
            # 发给全体
            results = mongo.find(MONGO_USER_COLLECTION, {})
            if results:
                [NoticeModel(sid=result.get('sid'), title=title, content=content).save() for result in results]
        else:
            NoticeModel(sid=to, title=title, content=content).save()

        data = {
            "title": title,
            "content": content,
            "t": to
        }
        return success(data=data, message='发送成功')
    elif request.method == "PUT":
        sid = rbody.get('sid')
        ni = int(rbody.get('ni'))

        mongo.do(MONGO_NOTICE_COLLECTION).find_one_and_update({"_id": ni, "sid": sid}, {"$set": {"is_read": True}})
        return success(data=ni, message='读取通知成功')
