# this python program is used to add new faces to known peoples list

import sys
import argparse
from cam import capture
from face_recognition_module import faceRecognition
print("\n### import complete ###\n")

def main():
    print("Training the system\n\nWhat's your name: ")
    name = raw_input();
    
    # capture image for training
    capture(name, "./face_testing/pictures_of_people_i_know/","System Training")

if __name__ == '__main__':
    main()
