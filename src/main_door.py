# this python program is to be used at the enterance
# of the home where this IoT system is implemented.

import sys
import argparse
from cam import capture
from face_recognition_module import faceRecognition
print("\n### import complete ###\n")

def main():
    print("Capturing image for recognition (Hit Enter to take a snap and Ecs to stop.)")
    while(True):
        if raw_input()=="exit": return
        capture("image", "./face_testing/unknown_pictures/","Face Recognition")     # capture image for recognition
        faceRecognition()                           # Recognize face


if __name__ == '__main__':
    main()
