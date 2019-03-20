# python 2/3

print("=== import started (client_RPi_face_training) ===")

from time import sleep
import os

try:
    from cam_pi import Camera
    is_raspberry_pi = True
except ImportError:
    from cam_laptop import Camera
    is_raspberry_pi = False

try:
    input = raw_input
except NameError:
    pass

import path_initializer
import udp_transfer

print("=== import complete (client_RPi_face_training) ===")

#####################################################################################################################


path_initializer.initialize_client_paths()
camera_obj = Camera()

print("\n")
ip_address = input("Please enter the server IP address: ")
port = input("Please enter the server Port Number: ")
sender= udp_transfer.UdpTransfer(ip_address,port)

print("\n\n### Press \"ENTER\" to take new photo, write \"exit\" to stop.")
name = input("\n\nWhat's your name: ")
msg=""

while msg != "exit":
    img_path = camera_obj.capture_single_image(path_initializer.CLIENT_KNOWN_FACES_FOLDER, name+'_')[0]
    sender.send_data("face_training", img_path, name)
    response=sender.recieve_data()
    print(response)
    msg = input()

