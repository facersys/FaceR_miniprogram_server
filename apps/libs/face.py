# -*- coding: utf-8 -*-
import os
import requests
import face_recognition
from tempfile import NamedTemporaryFile


class FaceTool:
    def __init__(self, img):
        """
        :param img: 图片地址或数据流
        """
        self.__img = img

    def is_face(self):
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img

        with NamedTemporaryFile('w+b', delete=False) as f:
            f.write(stream)
            image = face_recognition.load_image_file(f.name)
            tmp_filename = f.name
        os.remove(tmp_filename)
        return True if face_recognition.face_encodings(image) else False

    def encode(self):
        """编码"""
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            # stream = BytesIO(self.__img).read()
            stream = self.__img

        with NamedTemporaryFile('w+b', delete=False) as f:
            f.write(stream)
            image = face_recognition.load_image_file(f.name)
            # 一张图片可能会有多张人脸, 本应用只取第一张
            face_code = list(face_recognition.face_encodings(image)[0])
            tmp_filename = f.name

        os.remove(tmp_filename)
        return face_code

    def face_detection(self):
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img
        with NamedTemporaryFile('w+b', delete=False) as f:
            f.write(stream)
            image = face_recognition.load_image_file(f.name)
            # 一张图片可能会有多张人脸, 本应用只取第一张
            face_landmarks_ = face_recognition.face_landmarks(image)
            tmp_filename = f.name
        os.remove(tmp_filename)
        return face_landmarks_

    def get_face_arr(self):
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img

        with NamedTemporaryFile('w+b', delete=False) as f:
            f.write(stream)
            image = face_recognition.load_image_file(f.name)
            tmp_filename = f.name
        os.remove(tmp_filename)
        return image

# if __name__ == '__main__':
#     ft = FaceTool("https://www.yingjoy.cn/logo.png")
#     print(ft.is_face())
