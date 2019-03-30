# python 2/3
# Description: this is the main file which does face detection and face training without the server

print("=== import started (main) ===")

import sys
import argparse

# basic requirement
import path_initializer

# for method "authorize_guests"
from face_recognizer import FaceRecognizer

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

print("=== import complete (main) ===\n")

#####################################################################################################################


def authorize_guests():
    print("\nWaiting for a guest (press \"ENTER\" to take a photo of the guest and \"exit\" to stop)")
    while(True):
        if input()=="exit": return

        # capture image for training
        images_path_tuple = Camera.capture_single_image(path_initializer.SERVER_UNKNOWN_FACES_FOLDER)

        # do face recognition and return the results
        # here is have directly accessed the element at 0th index as each time only one photo is taken
        results = fr.face_detection(images_path_tuple[0], True, 0.2, 0.4)
        print(results)


def add_new_faces():
    print("Training the system\n")

    choice = 2
    while True:
        if choice == 1: pass
        elif choice == 2: name = input("Please enter the name: ");
        elif choice == 3: return
        else: print("ERROR: please enter a valid choice")

        # capture image for training
        image_path = path_initializer.SERVER_KNOWN_FACES_FOLDER + "/" + str(name)
        image_path = Camera.capture_single_image(image_path)[0]
        if fr.train_on_image(name, image_path, True):
            message = "Image saved !"        
            fr.save_to_file(path_initializer.SERVER_LOADED_DATASET_PATH)
        else:
            message = "No face found :("        


        print("\n--------------------------------------")
        print("Menu")
        print("1. add images of the same person")
        print("2. add images of a new person")
        print("3. exit")
        choice = input("\nPlease enter your choice: ")
        while choice == "":
            choice = input()
        choice = int(choice)


def main(arguments):
    mode = arguments.mode

    if not fr.load_from_file(path_initializer.SERVER_LOADED_DATASET_PATH):
        print("\n\nPlease wait while the images are being loaded ...\n")
        fr.train_on_folder_tree(True)
        fr.save_to_file(path_initializer.SERVER_LOADED_DATASET_PATH)

    if(mode == "detection"):
        print("Face detection")
        authorize_guests()
    elif mode == "training":
        print("Face training")
        add_new_faces()
    else:
        raise ValueError("Unimplemented mode")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # defualt mode is for face detection
    parser.add_argument("--mode", type=str, default="detection")
    arguments = parser.parse_args(sys.argv[1:]);

    print("\n\n=======================\n")
    path_initializer.initialize_server_paths()
    fr = FaceRecognizer(path_initializer.SERVER_KNOWN_FACES_FOLDER)

    main(arguments)
