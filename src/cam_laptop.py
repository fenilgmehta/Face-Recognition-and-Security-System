# python 2/3
import cv2
import os


def mydebug(msg, debug_prefix = "DEBUG"):
    print(str(debug_prefix)+": "+str(msg))


class Camera:
    def capture_single_image(image_path = "./", image_name_prefix = "image_", display_message = "Face Recognition and Security System"):
        """
            Used to capture a single photo from Laptop camera

            Parameters:
            image_path (str): path to store the captured image
            image_name_prefix (str): prefix for the new image name
            display_message (str): title for the camera window, i.e. this message will be displayed when the camera window is open
        """
        Camera.capture_multiple_image(image_path, image_name_prefix, display_message, 1)

    def capture_multiple_image(image_path = "./", image_name_prefix = "image_", display_message = "Face Recognition and Security System", image_count = 0):
        """
            Used to capture multiple photos from Laptop camera
            Press "ENTER" to take a new photo
            Press "ESC" to stop capturing

            Parameters:
            image_path (str): path to store the captured image
            image_name_prefix (str): prefix for the new image name
            display_message (str): title for the camera window, i.e. this message will be displayed when the camera window is open
            image_count (int): maximum number of images to be captured. If this is less than equal to 0, then keep taking images untill "ESC" is pressed
        """

        image_path = os.path.abspath(image_path)
        if os.path.exists(image_path) == False: return

        # count files and folders in the directory
        image_name_suffix = len(os.listdir(image_path)) + 1

        # select defualt camera i.e 0
        camera = cv2.VideoCapture(0)

        i = 1
        while (image_count <= 0) or (i <= image_count):
            # capture a frame
            is_image_captured, frame = camera.read()
            # stop if image not captured
            if not is_image_captured: break
            # show the captured frame
            cv2.imshow(display_message, frame)

            k = cv2.waitKey(1) % 256
            if k == 27:     # ESC pressed
                mydebug("Escape pressed, capturing stopped ...")
                break
            elif k == 13:   # Enter pressed (for space-bar event '32')
                # location to store the image
                img_name = image_path+"/"+image_name_prefix+"{}.png".format(image_name_suffix)
                cv2.imwrite(img_name, frame)
                mydebug("{} saved!".format(img_name))
                image_name_suffix += 1
                i += 1

        camera.release()
        cv2.destroyAllWindows()


Camera.capture_single_image = staticmethod(Camera.capture_single_image)
Camera.capture_multiple_image = staticmethod(Camera.capture_multiple_image)


if __name__ == "__main__":
    print("Single capture start")
    Camera.capture_single_image()
    print("Multiple capture start")
    Camera.capture_multiple_image()
