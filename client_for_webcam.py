import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import subprocess
import time
from firebase import firebase

firebase = firebase.FirebaseApplication('https://cognitrack-c16c7.firebaseio.com', None)
result = firebase.get('/users', None)
cap=cv2.VideoCapture(0)

ip = firebase.get('/server/ip', None)
print(ip)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((ip,8089))

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

firebase.patch('/camera/' + get_ip_address().replace(".", ""), {'location': ' 31.257786,75.708119'})
firebase.patch('/camera/' + get_ip_address().replace(".", ""), {'location_name': 'Room 1'})
firebase.patch('/camera/' + get_ip_address().replace(".", "") + "/blackout", {'status': '0'})
bo = 1

while True:
    time.sleep(0.1)
    ret,frame=cap.read()
    print(np.median(frame))
    if np.median(frame) < 15:
        if bo:
            firebase.patch('/camera/' + get_ip_address().replace(".", "") + "/blackout", {'status': '1'})
            bo = 0
    else:
        if not bo:
            firebase.patch('/camera/' + get_ip_address().replace(".", "") + "/blackout", {'status': '0'})
            bo = 1

    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data))+data)