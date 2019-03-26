# -*- coding: utf-8 -*-

<<<<<<< HEAD
import cv2
import numpy as np

=======
>>>>>>> dcab4223f7d47855f642a33018cf9b3b0f2b9d9b
from apps.libs import aipOcr


def img2txt(stream):
    """图片转文字"""
    result = aipOcr.basicAccurate(stream).get("words_result")
    return result[0].get('words') if result else ""
<<<<<<< HEAD


def get_polylines_data(arr):
    return [np.array([list(item) for item in arr], np.int32)]


def draw_face(image, face_landmarks_list):
    """画人脸"""
    for face_landmarks in face_landmarks_list:
        # 眉毛
        cv2.polylines(image, get_polylines_data(face_landmarks['left_eyebrow']), False, (68, 54, 39, 128), 5)
        cv2.polylines(image, get_polylines_data(face_landmarks['right_eyebrow']), False, (68, 54, 39, 128), 5)

        # 嘴唇
        cv2.polylines(image, get_polylines_data(face_landmarks['top_lip']), False, (150, 0, 0, 64), 5)
        cv2.polylines(image, get_polylines_data(face_landmarks['bottom_lip']), False, (150, 0, 0, 128), 5)

        # 眼睛
        cv2.polylines(image, get_polylines_data(face_landmarks['left_eye']), True, (255, 255, 255, 30))
        cv2.polylines(image, get_polylines_data(face_landmarks['right_eye']), True, (255, 255, 255, 30))

        # 下巴
        cv2.polylines(image, get_polylines_data(face_landmarks['chin']), False, (255, 255, 255, 30))

        # 鼻子
        cv2.polylines(image, get_polylines_data(face_landmarks['nose_bridge']), False, (255, 255, 255, 30))
        cv2.polylines(image, get_polylines_data(face_landmarks['nose_tip']), False, (255, 255, 255, 30))

    return image
=======
>>>>>>> dcab4223f7d47855f642a33018cf9b3b0f2b9d9b
