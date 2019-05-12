# -*- coding: utf-8 -*-


class UserModel:

    def __init__(self, uid, face=None):
        """
        :param uid: 用户id, 对应MySQL的user id
        :param face: 人脸编码
        """
        self._uid = uid
        self._face = face

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, face):
        self.face = face

    def get(self):
        return {
            "uid": self._uid,
            "face": self._face
        }
