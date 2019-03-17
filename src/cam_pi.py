# python 2
from picamera import PiCamera
from os
from time import sleep

class Camera:
    def capture_single_image(image_path = "./", image_name_prefix = "image_", image_capture_delay = 3):
        """
            Used to capture a single photo from Laptop camera.

            Parameters:
            image_path (str): Path to store the captured image
            image_name_prefix (str): Prefix for the new image name
            image_capture_delay (int): Minimum number of seconds to wait before capturing the image

            Returns:
            tuple: Path to all captured images
        """
        image_path = os.path.abspath(image_path)
        if os.path.exists(image_path) == False: return


        # count files and folders in the directory
        image_name_suffix = len(os.listdir()) + 1
        complete_image_paths = (image_path+"/"+pic_name_prefix+"{}.png".format(image_name_suffix))
        
        # take access to PiCamera
        camera = PiCamera()
        # show PiCamera preview
        camera.start_preview()
        # wait for pic_delay
        sleep(pic_delay)
        # take the photo and save it
        camera.capture(complete_image_paths[0])
        # close PiCamera
        camera.stop_preview()

        return complete_image_paths

Camera.capture_single_image = staticmethod(Camera.capture_single_image)

if __name__ == "__main__":
    print("Single capture start")
    Camera.capture_single_image()
