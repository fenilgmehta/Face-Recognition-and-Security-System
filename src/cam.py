import cv2
import os

def capture(path, mode):                        # path for storing image; mode to give title to capture window 

    camera = cv2.VideoCapture(0)                            # select defualt camera i.e 0

    path, dirs, files = next(os.walk(path))
    img_counter = len(files)                            #count files in directory

    while True:
        ret, frame = camera.read()
        cv2.imshow(mode, frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:                             # ESC pressed
            print("Escape, closing capture...")
            break

        elif k%256 == 13:                               # Enter pressed (for spacebar event '32')
            img_name = path+"image_{}.png".format(img_counter)      #location to store image
            cv2.imwrite(img_name, frame)
            print("{} saved!".format(img_name))
            img_counter += 1

    camera.release()
    cv2.destroyAllWindows()
