# python 2
from picamera import PiCamera
from time import sleep
from os import walk

class Camera:
    def __init__(self):
        # start PiCamera
        self.camera = PiCamera()
    
    def capture(self, path = './face_testing/unknown_pictures/', pic_name_prefix = 'image_', pic_delay = 3):
        path, dirs, files = next(walk(path))
        
        #count files in directory
        img_counter = len(files)
    
        # show PiCamera preview
        self.camera.start_preview()
        # wait for pic_delay and take the photo
        sleep(pic_delay)
        # take the photo and save it with the name "image_[img_counter+1].png"
        self.camera.capture(path+pic_name_prefix+"{}.png".format(img_counter+1))
        # close PiCamera
        self.camera.stop_preview()
        
        return (img_counter+1)
                

