from picamera import PiCamera
from time import sleep
import os
import tkinter as tk
import tkinter.font
from PIL import Image, ImageTk
import pyrebase #sudo pip install pyrebase

firebase_config = {
    "apiKey": "AIzaSyD2PRJDK0XZc7AXoV4EIYAT39lARK4WKb8",
    "authDomain": "naamakirja-dea54.firebaseapp.com",
    "databaseURL": "https://naamakirja-dea54-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "naamakirja-dea54",
    "storageBucket": "naamakirja-dea54.appspot.com",
    "serviceAccount": "serviceAccountKey.json"
    #need to download serviceKey and rename it to serviceAccountKey
    #project settings -> service accounts -> python -> generate new private key
    }

firebase_storage = pyrebase.initialize_app(firebase_config)
storage = firebase_storage.storage()

camera = PiCamera()

#Set Camera Properties
camera.resolution = (2592, 1944)
camera.framerate = 15

#Create a window with tkinter
win=tk.Tk()
win.title("CameraTest")
myFont=tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

#method to use when pressing 'take a picture' button:
def capture():
    pic_name = pic_name_entry.get()
    if pic_name_entry.get() != '':     
        camera.start_preview(alpha = 200)
        print(f"name will be '{pic_name}'")
        print("taking picture...")
        sleep(2)
        camera.capture('/home/pi/group_20/pics/%s.jpg' %pic_name)
        print("saved a picture named '%s'" %pic_name)
        
        #upload image to firebase storage
        storage.child("antti/%s.jpg" %pic_name).put("/home/pi/group_20/pics/%s.jpg" %pic_name)
        
        camera.stop_preview()
        
    else:
        print("no name given, give a name.")
#method to close the window
def exitProgram():
    win.destroy()

#button for taking a picture:
take_pic_button=tk.Button(win, text='Take a picture', font=myFont, command=capture, bg='bisque2',
                          height=1, width=24)
take_pic_button.grid(row=0, column=0, sticky=tk.NSEW)

#create label for naming the picture:
pic_name_label=tk.Label(win, text='name your picture', font=myFont,bg='bisque',
                        height=1, width=24)
pic_name_label.grid(row=1, column=0, sticky=tk.W)

#create entry field for picture name:
pic_name_entry=tk.Entry(win, bd=5,width=12)
pic_name_entry.grid(row=1, column=1, sticky=tk.E)

#button for exiting the program:
exit_button=tk.Button(win, text='Exit', font=myFont, command=exitProgram, bg='bisque2',
                      height=1, width=6)
exit_button.grid(row=2, sticky=tk.NSEW)

tk.mainloop()
                          
