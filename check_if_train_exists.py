import os
from os import path
from os.path import exists
import numpy as np
import cv2 as cv

def check_train_existance():
    if path.exists('/home/pi/group_20/features.npy'):
        features = np.load('features.npy')
    else:
        pass
    if path.exists('/home/pi/group_20/labels.npy'):
        labels = np.load('labels.npy')
    else:
        pass

    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    if path.exists('/home/pi/group_20/face_trained.yml'):
        face_recognizer.read('face_trained.yml')
    else:
        pass
    return face_recognizer