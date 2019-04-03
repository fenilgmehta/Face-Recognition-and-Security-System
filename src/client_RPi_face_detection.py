# python 3
# Description: client module for face training

print("=== import started (client_RPi_face_detection) ===")

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

print("=== import complete (client_RPi_face_detection) ===")

#####################################################################################################################


path_initializer.initialize_client_paths()

print("\n")
ip_address = input("Please enter the server IP address: ")
port = input("Please enter the server Port Number: ")
sender= udp_transfer.UdpTransfer(ip_address,port)

print("\n\n### Press \"ENTER\" to take new photo, write \"exit\" to stop.")
msg = input()

while msg != "exit":
    img_path = Camera.capture_single_image(path_initializer.CLIENT_UNKNOWN_FACES_FOLDER)[0]
    sender.send_data("face_detection",img_path)
    response=sender.recieve_data()
    print("\n"+str(response))
    msg = input()

