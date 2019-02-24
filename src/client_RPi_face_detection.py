# python 2
from time import sleep
import os
import sender

import cam_pi

path = './face_testing/unknown_pictures/'
camera_obj = cam_pi.Camera()

print("### Press enter to take new photo, write 'exit' to stop.")
ip_address = raw_input("Please enter the server IP address: ")
msg = raw_input()

while msg != "exit":
    img_counter = camera_obj.capture(path)				#count files in directory
    sender.call1("face_detection",ip_address,path+"image_{}.png".format(img_counter))
    msg = raw_input()
