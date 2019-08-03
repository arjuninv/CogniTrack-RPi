from time import sleep
import picamera
import picamera.array
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import subprocess
from firebase import firebase


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

firebase = firebase.FirebaseApplication('https://cognitrack-c16c7.firebaseio.com', None)
result = firebase.get('/users', None)
ip = firebase.get('/server/ip', None)
firebase.patch('/camera/' + get_ip_address().replace(".", ""), {'location': ' 31.257786,75.708119'})
firebase.patch('/camera/' + get_ip_address().replace(".", ""), {'location_name': 'Room 1'})
firebase.patch('/camera/' + get_ip_address().replace(".", "") + "/blackout", {'status': '0'})
bo = 1

print(ip)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((ip,8089))


print(get_ip_address())
firebase.patch('/camera/' + get_ip_address().replace(".", ""), {'location': ' 31.257786,75.708119'})

while True:
    try:
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as stream:
                camera.shutter_speed = 6000000
                camera.iso = 800
                camera.capture(stream, format='bgr')
                image = stream.array
                data = pickle.dumps(image)
                print(np.median(image))
                if np.median(image) < 15:
                    if bo:
                        firebase.patch('/camera/' + get_ip_address().replace(".", "") + "/blackout", {'status': '1'})
                        bo = 0
                else:
                    if not bo:
                        firebase.patch('/camera/' + get_ip_address().replace(".", "") + "/blackout", {'status': '0'})
                        bo = 1
                clientsocket.sendall(struct.pack("L", len(data))+data)
                #time.sleep(0.)
    except socket.error:
        print( "re-connection successful" )
        sleep(2)  
        sleep(2)  