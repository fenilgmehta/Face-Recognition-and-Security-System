# python 2/3
# Description: this python program is used to add new faces to known peoples list

print("=== import started (main_add_new_faces) ===")

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

print("=== import complete (main_add_new_faces) ===\n")


def add_new_faces():
    print("Training the system\n")

    choice = 2
    while True:
        if choice == 1: pass
        elif choice == 2: name = input("Please enter the name: ");
        elif choice == 3: return
        else: print("ERROR: please enter a valid choice")

        # capture image for training
        Camera.capture_single_image("./z_face_testing/pictures_of_people_i_know/" + str(name))

        print("\n--------------------------------------")
        print("Menu")
        print("1. add images of the same person")
        print("2. add images of a new person")
        print("3. exit")
        choice = int(input("\nPlease enter your choice: "))


if __name__ == '__main__':
    add_new_faces()
