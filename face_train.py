import os
import cv2 as cv
import numpy as np
from os import path


class Train_Faces:
    def __init__(self):

        with open("name_file.txt") as file:
            self.lines = file.readlines()
            self.lines = [line.rstrip() for line in self.lines]
            print(self.lines)

        self.people = self.lines
        print(self.people)
        self.DIR = r'/home/pi/camera_test/faces'

        self.haar_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')


        self.features = []
        self.labels = []

    def create_train(self):
        for person in self.people:
            path = os.path.join(self.DIR, person)
            label = self.people.index(person)

            for img in os.listdir(path):
                img_path = os.path.join(path, img)

                img_array = cv.imread(img_path)
                img_array = cv.imread(img_path)

                gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

                faces_rect = self.haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

                for (x,y,w,h) in faces_rect:
                    faces_roi = gray[y:y+h, x:x+w]
                    self.features.append(faces_roi)
                    self.labels.append(label)

    def start_training(self):
        self.create_train()
        print('Training done')

        self.features = np.array(self.features, dtype='object')
        self.labels = np.array(self.labels)

        print(f'Length of the features = {len(self.features)}')
        print(f'Length of the labels = {len(self.labels)}')

        face_recognizer = cv.face.LBPHFaceRecognizer_create()

        face_recognizer.train(self.features, self.labels)

        face_recognizer.save('face_trained.yml')
        np.save('features.npy', self.features)
        np.save('labels.npy', self.labels)

        if path.exists('/home/pi/camera_test/features.npy'):
            features = np.load('features.npy')
        else:
            pass
        if path.exists('/home/pi/camera_test/labels.npy'):
            labels = np.load('labels.npy')
        else:
            pass
        
        self.features = []
        self.labels = []
