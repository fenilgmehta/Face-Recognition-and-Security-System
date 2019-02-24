# Face-Recognition-and-Security-System

This project is intended for IoT systems so that the home door opens automatically for the family members.


-----------------------
## Steps for execution

On one device:
1.  "main.py" is the starter module for project (alternatives: "main_door.py" and "main_add_new_face.py")
2.  "cam_laptop.py" and "cam_pi.py" are used for capturing images for face training and face recognition.
3.  "face_recognition_module.py" is used for final face recognition.

Using client server model:
1. run the "server.py" file on your server device. Note down the IP address of the server on the LAN
2. "client_RPi_face_trainning.py" should be used on the client to add know/authorized people to the dataset
2. "client_RPi_face_detection.py" to be used for face detection on the client


-----------------------
### How to run:

1. For training the system with authorized faces
```sh
   $ python main.py --mode input
   # Press 'Enter' to capture and 'Esc' to stop and exit
```


2. For unknown face recognition

```sh
   $ python main.py
   # Press 'Enter' to capture and 'Esc' to stop and exit
```


3. For testing the programs with existing images
```sh
   $ python main.py --mode recognition
```
