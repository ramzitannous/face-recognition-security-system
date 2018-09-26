# from train import *
# x,y=loadEncodings()
import time

import face_recognition

path = "/home/pi/Desktop/Face Recognition/dataset/images/ramzi tannous/obama.jpg"
img = face_recognition.load_image_file(path)
t = time.time()
rr = face_recognition.face_encodings(img)
print(rr)
print(time.time() - t)
