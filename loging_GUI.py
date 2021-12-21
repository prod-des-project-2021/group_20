
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2 as cv
import os
from os import path
from os.path import exists
import numpy as np
import time
from imutils.video import VideoStream

import face_train
import check_if_train_exists

import pyrebase #sudo pip install pyrebase

#firebase_config = {
#    "apiKey": "AIzaSyD2PRJDK0XZc7AXoV4EIYAT39lARK4WKb8",
#    "authDomain": "naamakirja-dea54.firebaseapp.com",
#    "databaseURL": "https://naamakirja-dea54-default-rtdb.europe-west1.firebasedatabase.app",
#    "projectId": "naamakirja-dea54",
#    "storageBucket": "naamakirja-dea54.appspot.com",
#    "serviceAccount": "serviceAccountKey.json"
    #need to download serviceKey and rename it to serviceAccountKey
    #project settings -> service accounts -> python -> generate new private key
#    }

#firebase_storage = pyrebase.initialize_app(firebase_config)
#storage = firebase_storage.storage()

class Login_GUI:
    def __init__(self, vs):
        self.trainer = face_train.Train_Faces()
        self.train_checker = check_if_train_exists.check_train_existance()

        self.vs = vs
        self.frame = None
        self.cameraThread = None
        self.stopEvent = None
        self.path = path

        with open("name_file.txt") as file:
            self.lines = file.readlines()
            self.lines = [line.rstrip() for line in self.lines]
            print(self.lines)

        self.people = self.lines
        print(self.people)

        self.root = tki.Tk()
        self.panel = None

        self.name_var = tki.StringVar()
        self.name = None

        take_pic_btn = tki.Button(self.root, text='Take a picture!', 
                                    command=self.takeSnapshot)
        take_pic_btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        train_pic_btn = tki.Button(self.root, text='Train face recognition!',
                                     command=self.trainer.start_training)
        train_pic_btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        set_name_btn = tki.Button(self.root, text='Login with your name!', 
                                    command=self.set_name)
        set_name_btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        set_name_label = tki.Label(self.root, text='Set your name!')
        set_name_label.pack(side='left')

        set_name_entry = tki.Entry(self.root, bd = 5, textvariable = self.name_var)
        set_name_entry.pack(side='right')

        self.stopEvent = threading.Event()
        self.cameraThread = threading.Thread(target=self.videoLoop, args=())
        self.cameraThread.start()

        self.root.wm_title('asd')
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

#Video loop with face detector and recognizer running in it
    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                #gets the videofeed
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=500)

                #makes the cideofeed into cv2 compatible forms to be displayed in tkinter
                #and to the face recognizer
                image = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
                gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                
                haar_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
                faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
                for (x,y,w,h) in faces_rect:
                    faces_roi = gray[y:y+h,x:x+w]
                    
                    #checks if trained faces axists and  if they do runs the recognizer
                    if path.exists('/home/pi/group_20/camera_test/face_trained.yml'):
                        self.train_checker
                        label, confidence = self.train_checker.predict(faces_roi)
                        print(f'Label = {self.people[label]} with a confidence of {confidence}')
                        if confidence >= 70:
                            cv.putText(self.frame, str(self.people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
                            cv.rectangle(self.frame, (x,y), (x+w,y+h), (0,255,0), thickness=2)
                        else:
                            cv.rectangle(self.frame, (x,y), (x+w,y+h), (255,0,0), thickness=2)
                    else:
                        cv.rectangle(self.frame, (x,y), (x+w,y+h), (255,0,0), thickness=2)
                    

                image = Image.fromarray(self.frame)
                image = ImageTk.PhotoImage(image)             
                
                #updating the screen
                if self.panel is None:
                    self.panel = tki.Label(image = image)
                    self.panel.image = image
                    self.panel.pack(side='left', padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError :
            print("runtimeError")

#picture taking function
#only works if name is set
    def takeSnapshot(self):
        
        #loops thru all files with .jpg ending and deletes them
        #so it doesnt keep on downloading same images
        #filelist = [ f for f in os.listdir("/home/pi/group_20/faces/" + self.name) if f.endswith(".jpg") ]
        #for f in filelist:
        #    os.remove(os.path.join("/home/pi/group_20/faces/" + self.name, f))
        
        #download images from storage
        #all_storage_files = storage.list_files()
        #for storage_file in all_storage_files:
        #    print("filename in storage:" + storage_file.name) #prints filenames
        #    storage_file.download_to_filename("/home/pi/group_20/faces/" + storage_file.name)
        
        ts = datetime.datetime.now()
        if self.name:
            filename = '/home/pi/group_20/faces/' + self.name + "/image_{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
            cv.imwrite(filename, self.frame.copy())
            print("{}".format(filename))
            
            #upload image to firebase storage
            #storage.child(self.name + "/image_{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))).put(filename)
        else:
            pass

#set name function that checks if the name is used.
#if not then it creates a folder for it to save pictures into
#also creates name in a text file for the trainer labels THIS IS TEMP SOLUTION
    def set_name(self):
        self.name = self.name_var.get()
        if self.path.exists('/home/pi/group_20/faces/' + self.name):
            print(self.name)
        else:
            name_file = open("name_file.txt", "a+")
            name_file.write(f"{self.name}\r\n")  
            name_file.close()    
            directory = self.name
            parent_dir = '/home/pi/group_20/faces'
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            mode = 0o666
            return self.name
#closes the program, windows and videostreams
    def onClose(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

    