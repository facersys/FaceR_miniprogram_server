# -*- coding: utf-8 -*-

from apps.Library import db
from datetime import datetime


class NoticeModel(db.Model):
    __tablename__ = 'notice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)

    # 和用户表进行外键关联
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'))

    def __repr__(self):
        return '[NoticeModel]: %s, %s' % (self.id, self.name)
