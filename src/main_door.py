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

from face_recognizer import FaceRecognizer

print("=== import complete (main_door) ===\n")


def authorize_guests():
    fr = FaceRecognizer("./z_face_testing/pictures_of_people_i_know/")
    fr.train_on_folder_tree(True)
    fr.save_to_file()

    print("\nWaiting for a guest (press \"ENTER\" to take a photo of the guest and \"exit\" to stop)")
    while(True):
        if input()=="exit": return

        # capture image for training
        images_path_tuple = Camera.capture_single_image("./z_face_testing/unknown_pictures/")

        # do face recognition and return the results
        # here is have directly accessed the element at 0th index as each time only one photo is taken
        results = fr.face_detection(images_path_tuple[0])
        print(results)


if __name__ == '__main__':
    authorize_guests()
