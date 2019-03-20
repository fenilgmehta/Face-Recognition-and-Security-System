# python 2/3
# Description: this python program is to be used at the enterance of the home where this Internet of Things(IoT) system is implemented

print("=== import started (main_door) ===")

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
from face_recognizer import FaceRecognizer

print("=== import complete (main_door) ===\n")

#####################################################################################################################


def authorize_guests():
    fr = FaceRecognizer(path_initializer.SERVER_KNOWN_FACES_FOLDER)
    if not fr.load_from_file(path_initializer.SERVER_MAIN_DATA_FOLDER + "/" + "trained_faces.pkl"):
        fr.train_on_folder_tree(True)
        fr.save_to_file(path_initializer.SERVER_MAIN_DATA_FOLDER + "/" + "trained_faces.pkl")

    print("\nWaiting for a guest (press \"ENTER\" to take a photo of the guest and \"exit\" to stop)")
    while(True):
        if input()=="exit": return

        # capture image for training
        images_path_tuple = custom_camera.capture_single_image(path_initializer.SERVER_UNKNOWN_FACES_FOLDER)

        # do face recognition and return the results
        # here is have directly accessed the element at 0th index as each time only one photo is taken
        results = fr.face_detection(images_path_tuple[0], True, 0.2, 0.4)
        print(results)


if __name__ == '__main__':
    path_initializer.initialize_server_paths()
    custom_camera = Camera()
    authorize_guests()
