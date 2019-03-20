# python 2
from time import sleep
import os

import cam_pi
import udp_transfer

path = './face_testing/pictures_of_people_i_know/'
camera_obj = cam_pi.Camera()

print("### Press enter to take new photo, write 'done' to stop.")
ip_address = raw_input("Please enter the server IP address: ")
port = raw_input("Please enter the server Port Number: ")
sender= udp_transfer.UdpTransfer(ip_address,port)

msg=""
name = raw_input("What's your name: ")
while msg != "done":
    img_counter = camera_obj.capture(path, name+'_')
    sender.send_data("face_training",path+name+"_{}.png".format(img_counter))
    response=sender.recieve_data()
    print(response)
    msg = raw_input()

