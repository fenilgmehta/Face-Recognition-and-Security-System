# python 2 and 3

from socket import *
import sys
import select
from face_recognition_module import faceRecognition
from text2speech import text_to_speech
import netifaces as ni

message = "Image saved !"

def get_wifi_ip():
    '''
    Returns a tuple of (IPv4 and IPv6) WiFi address
    '''
    for i in netifaces.interfaces():
        if i.startswith('wlp'):
            if netifaces.ifaddresses(i).__contains__(netifaces.AF_INET):
                return (netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr'], netifaces.ifaddresses(i)[netifaces.AF_INET6][0]['addr'].split("%")[0])


host = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
port = 9999
while True:
    print("\n\nServer is running ...\n")
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind((host,port))

    #addr = (host,port)
    buf=1024

    data,addr = s.recvfrom(buf)
    #print "Received File: "+data.strip()+"\nFrom: "+addr

    data = str(data)
    mode = data[:data.rfind("@")][2:]
    print(mode)
    if mode == "face_training":                         # check the mode in which image is received and set path appropriatly
        path = "./trained_faces/"   
    else:
        path = "./unknown_faces/"   

    f = open(path+data[data.rfind('/')+1:],'wb')        # create a file in specified directory

    imgFile,addr = s.recvfrom(buf)                      # store file in buffer
    try:
        while(imgFile):
            f.write(imgFile)                            # write file
            s.settimeout(2)
            imgFile,addr = s.recvfrom(buf)
    except timeout:
        f.close()
        print("File Downloaded")

    if mode == "face_training":
        message = 'Image saved !'        
    else:
        message = faceRecognition()    
        #message = "Image saved !"

    text_to_speech(message)
    s.sendto(message.encode(), addr)
    
    print(message)
    message = ''
    s.close()
