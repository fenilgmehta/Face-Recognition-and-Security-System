# Face-Recognition-and-Security-System

This project is intended for IoT systems so that the home door opens automatically for the family members.


-----------------------
## Steps for execution

Using client server model:
1. run the "server.py" file on your server device. Note down the IP address and the port number printed
2. "client_RPi_face_training.py" should be used on the client to add known/authorized people to the dataset
3. "client_RPi_face_detection.py" to be used for face detection on the client side

Note: use python 3 for the program execution to avoid any difficuly and errors

-----------------------
### How to run:

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

