# python 2
from time import sleep
import os
import sender

import cam_pi

path = './face_testing/pictures_of_people_i_know/'
camera_obj = cam_pi.Camera()

print("### Press enter to take new photo, write 'done' to stop.")
ip_address = raw_input("Please enter the server IP address: ")
name = raw_input("What's your name: ")
msg = raw_input()

while msg != "done":
    img_counter = camera_obj.capture(path, name+'_')
    sender.call1("face_training",ip_address,path+name+"_{}.png".format(img_counter))
    msg = raw_input()
