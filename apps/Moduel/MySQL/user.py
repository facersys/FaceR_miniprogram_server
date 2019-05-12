# -*- coding: utf-8 -*-

import shortuuid
from datetime import datetime
from apps.Library import db
from apps.Config.Others import DEFAULT_AVATAR
from apps.Moduel.MySQL.notice import NoticeModel


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(20), primary_key=True, default=shortuuid.uuid)
    # 学号
    sid = db.Column(db.String(20))
    # 姓名
    name = db.Column(db.String(20), nullable=False)
    # 性别: 男1女2
    gender = db.Column(db.SmallInteger, nullable=False, default=0)
    # 年级
    grade = db.Column(db.Integer)
    # 专业
    major = db.Column(db.String(50))
    # 学院
    college = db.Column(db.String(50))
    # 班级
    class_name = db.Column(db.String(50))
    # 人脸图像url
    face_url = db.Column(db.String(200))
    # 邮箱
    email = db.Column(db.String(100))
    # 电话
    phone = db.Column(db.String(20))
    # openid
    openid = db.Column(db.String(100))
    # unionid
    unionid = db.Column(db.String(100), unique=True)
    # 是否绑定教务系统
    is_bind_jw = db.Column(db.Boolean, nullable=False, default=False)
    # 头像
    avatar = db.Column(db.String(200), nullable=False, default=DEFAULT_AVATAR)
    # 城市
    city = db.Column(db.String(30))
    # 省份
    province = db.Column(db.String(30))

    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 更新时间
    update_time = db.Column(db.DateTime, default=datetime.now)

    # 通知
    notices = db.relationship("NoticeModel", backref="user", lazy="dynamic")

    def get_json(self):
        return {
            "id": self.id,
            "sid": self.sid,
            "name": self.name,
            "gender": self.gender,
            "grade": self.grade,
            "major": self.major,
            "college": self.college,
            "class_name": self.class_name,
            "face_url": self.face_url,
            "email": self.email,
            "phone": self.phone,
            "openid": self.openid,
            "unionid": self.unionid,
            "is_bind_jw": self.is_bind_jw,
            "avatar": self.avatar,
            "city": self.city,
            "province": self.province,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "notices": [item.id for item in self.notices],
        }