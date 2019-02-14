# this is the main file which integrates two modules (cam and face_recognition_module)

import sys
import argparse
from cam import capture
from face_recognition_module import faceRecognition


def main(arguments):
    mode = arguments.mode

    if(mode == "camera"):
        print("Capturing image for recognition")
        capture("./face_testing/unknown_pictures/","Face Recognition")        # capture image for recognition
        faceRecognition()                            # Recognize face

    elif mode == "input":
        print("Training the system")
        capture("./face_testing/pictures_of_people_i_know/","System Training")    # capture image for training

    elif mode == "recognition":                            # for testing pupose only
        print("Mode = Face Recognition")
        faceRecognition()                            # Recognize face
    else:
        raise ValueError("Unimplemented mode")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="camera")        # defualt mode is for capturing and recognizing face
    arguments = parser.parse_args(sys.argv[1:]);
    main(arguments)
