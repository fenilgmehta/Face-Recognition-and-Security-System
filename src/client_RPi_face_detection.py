# python 2
from time import sleep
import os

import udp_transfer
import cam_pi

path = './face_testing/unknown_pictures/'
camera_obj = cam_pi.Camera()

print("### Press enter to take new photo, write 'exit' to stop.")
ip_address = raw_input("Please enter the server IP address: ") #192.168.43.124
port = raw_input("Please enter the server Port Number: ")
sender= udp_transfer.UdpTransfer(ip_address,port)

msg = raw_input()
while msg != "exit":
    img_counter = camera_obj.capture(path)				#count files in directory
    sender.send_data("face_detection",path+"image_{}.png".format(img_counter))
    response=sender.recieve_data()
    print("\n"+str(response))
    msg = raw_input()
