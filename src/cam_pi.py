# python 2
from picamera import PiCamera
from time import sleep
import os
import sender

class Camera:
    def __init__(self):
        # start PiCamera
        self.camera = PiCamera()
    
    def capture(self, path = './face_testing/unknown_pictures/', pic_name = 'image_', pic_delay = 3):
        path, dirs, files = next(os.walk(path))
        
        #count files in directory
        img_counter = len(files)
    
        # show PiCamera preview
        self.camera.start_preview()
        # wait for pic_delay and take the photo
        sleep(pic_delay)
        # take the photo and save it with the name "image_[img_counter+1].png"
        self.camera.capture(path+pic_name+"{}.png".format(img_counter+1))
        # close PiCamera
        self.camera.stop_preview()
        
        return (img_counter+1)
                

