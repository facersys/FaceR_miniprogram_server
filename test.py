# -*- coding: utf-8 -*-

<<<<<<< HEAD
import cv2
import face_recognition

# Load the jpg file into a numpy array
image = cv2.imread('2.jpg')

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

print(face_landmarks_list)


# pil_image.show()
cv2.imshow('', image)
cv2.waitKey(0)
=======

>>>>>>> dcab4223f7d47855f642a33018cf9b3b0f2b9d9b
