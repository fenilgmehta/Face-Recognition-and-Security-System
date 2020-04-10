# Face-Recognition-and-Security-System

This project is intended for IoT systems so that the home door opens automatically for the family members.

**Note**: use python 3 and face-recognition==1.2.3 for the program execution to avoid any difficuly and errors

## Steps for execution

Using client server model:
1. run the "server.py" file on your server device. Note down the IP address and the port number printed
2. "client_RPi_face_training.py" should be used on the client to add known/authorized people to the known people dataset
3. "client_RPi_face_detection.py" to be used for face detection on the client side

## How to run

1. Start the server
```sh
   $ python3 server.py
   # note down the IP address and port number printed for client use
```


2. To save known faces
```sh
   $ python3 client_RPi_face_training.py
   # follow the messages on the screen to proceed
```


3. For unknown face recognition

```sh
   $ python3 client_RPi_face_detection.py
   # follow the messages on the screen to proceed
```

## Future work
1. Use REST API instead of using the networking library
2. Use [pynput](https://pypi.org/project/pynput/) to allow the user to take picture on key press.
   - In `cam_laptop.py` Replace cv2.waitKey
   - In `cam_pi.py` add key press support
3. Add option to delete previously saved faces
4. Add a feature to save user face from a small video where they will move their face in all directions for better recognition, inturn saving time of the user from taking multiple single images.
5. Improvise the architecture to support multiple customer using Email-ID and password authentication.
