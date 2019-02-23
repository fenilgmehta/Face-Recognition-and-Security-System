#!/usr/bin/env python
# python 2

from socket import *
import sys

def call1(mode,ip,file1):
    s = socket(AF_INET,SOCK_DGRAM)
    #host =sys.argv[1]
    host=ip
    port = 9999
    buf =1024
    file_name=file1
    addr = (host,port)
    
    #file_name=sys.argv[2]

    s.sendto(mode+"@"+file_name,addr)

    f=open(file_name,"rb")
    data = f.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            # print "sending ..."
            data = f.read(buf)
            
    message, ip = s.recvfrom(buf)
    print("\n"+message.decode())
    s.close()
    f.close()
