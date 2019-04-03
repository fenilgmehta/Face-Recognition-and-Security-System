# python 3
# Description: server program to accept and respond to client requests

print("=== import started (server) ===")

from socket import *
import sys
import os
import select
import netifaces

import path_initializer
from face_recognizer import FaceRecognizer
from text2speech import text_to_speech

print("=== import complete (server) ===\n")

#####################################################################################################################


def get_wifi_ip():
    '''
    WiFi interface IPv4 and IPv6 addresses if available, else empty tuple

    Returns:
    tuple: tuple of (IPv4 and IPv6) for WiFi address
    '''
    for i in netifaces.interfaces():
        if i.startswith('wlp'):
            if netifaces.ifaddresses(i).__contains__(netifaces.AF_INET):
                return (netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr'], netifaces.ifaddresses(i)[netifaces.AF_INET6][0]['addr'].split("%")[0])
    return tuple()


ip_addresses = get_wifi_ip()
if len(ip_addresses) == 0:
    print("Unable to fetch the IP address. Hence running the server on localhost - 127.0.0.1")
    ip_addresses = tuple(["127.0.0.1"])

host = ip_addresses[0]
port = 9999

print("\n")
print("host = " + str(host))
print("port = " + str(port))

path_initializer.initialize_server_paths()
fr = FaceRecognizer(path_initializer.SERVER_KNOWN_FACES_FOLDER)
loaded_dataset_path = path_initializer.SERVER_MAIN_DATA_FOLDER + "/" + "trained_faces.pkl"
if not fr.load_from_file(loaded_dataset_path):
    print("\n\nPlease wait while the server is getting initialized ...\n")
    fr.train_on_folder_tree()
    fr.save_to_file(loaded_dataset_path)

print("\nPress \"ctrl+c\" to stop the server")

while True:
    print("\n")
    print("=====================")
    print("Server is running ...\n")
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind((host,port))

    #addr = (host,port)
    buf=1024

    try:
        data, addr = s.recvfrom(buf)
    except KeyboardInterrupt:
        print("\nStopping the server ...")
        s.close()
        exit(0)

    corrupted_data_error = False
    try:
        data = str(data.decode()).split("@")
        # data = str(data.decode())
    except:
        print("ERROR: corrupted data received")
        corrupted_data_error = True
        # the following lines will receive all the data sent and then send the reply
        try:
            imgFile,addr = s.recvfrom(buf)
            while(imgFile):
                s.settimeout(1)
                imgFile,addr = s.recvfrom(buf)
        except timeout:
            s.sendto("Network error, try again".encode(), addr)
        continue

    mode = data[0]
    image_name = data[1]
    if len(data) == 3:
        person_name = data[2]
        print("person_name : " + person_name)

    # check the mode in which image is received and set image_path appropriatly
    if mode == "face_training":
        image_path = path_initializer.SERVER_KNOWN_FACES_FOLDER + "/" + person_name
    else:
        image_path = path_initializer.SERVER_UNKNOWN_FACES_FOLDER

    if not os.path.exists(image_path): os.makedirs(image_path) # create the directory with the new persons name if it does not exist

    image_save_path = image_path+"/"+image_name
    image_save_path = image_save_path[:image_save_path.rfind(".")] + "_" + str(len(os.listdir(image_path))) + ".png"
    print("mode : " + mode)
    print("image_name : " + image_name)
    print("image_path : " + image_path)
    print("image_save_path : " + str(image_save_path))

    # create a file in specified directory
    f = open(image_save_path,'wb')

    # store file in buffer and write to file
    imgFile,addr = s.recvfrom(buf)
    try:
        while(imgFile):
            f.write(imgFile)                            # write file
            s.settimeout(1)
            imgFile,addr = s.recvfrom(buf)
    except timeout:
        f.close()
        print("File Downloaded")
    except:
        print("Unknown error")
        mode = "error"

    if mode == "error":
        message = "Error downloading the image."
        text_to_speech(message)
    elif mode == "face_training":
        if fr.train_on_image(str(person_name), str(image_save_path), True):
            message = "Image saved !"        
            fr.save_to_file(loaded_dataset_path)
        else:
            message = "No face found :("        
        text_to_speech(message)
    else:
        try:
            res = fr.face_detection(image_save_path, True, 0.2, 0.4)
            message = res[0][1]
            print("result : " + str(res))
            for i in res:
                if i[0]: text_to_speech("Welcome " + str(i[1]))
            if len(res) == 1 and res[0][0] == False:
                text_to_speech(message)
        except:
            message = "Error, image corrupted"
            text_to_speech(message)
            print(message)
    
    s.sendto(message.encode(), addr)
    
    print(message)
    s.close()

