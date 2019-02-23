# USE anaconda / miniconda distribution for easy installation and usage of python and other libraries
# https://github.com/ageitgey/face_recognition
# pip install face_recognition

import face_recognition
import os
import datetime


def faceRecognition():
    messageToClient = "\n\nUnauthorized person"
    base_path = "."
    folder_known_faces = '/trained_faces'
    folder_unknown_faces = '/unknown_faces'


    known_people_names_map = os.listdir(base_path+folder_known_faces)
    known_people_names_map.sort()
    known_people_names_to_remove = []
    known_people_images = list(known_people_names_map)
    known_people_images_encoded = []


    unknown_people_images = os.listdir(base_path+folder_unknown_faces+"/")
    unknown_people_images.sort()
    unknown_people_images_encoded = []


    # known_people_images_encoded now contains a universal 'encoding' of all facial features that can be compared to any other picture of a face!
    for i in range(len(known_people_images)):
        known_picture = face_recognition.load_image_file(base_path+folder_known_faces+"/"+str(known_people_images[i]))
        known_face_encoding = face_recognition.face_encodings(known_picture)
        if len(known_face_encoding) > 0:
            known_people_images_encoded.append(known_face_encoding[0])
            # print("'" + known_people_images[i] + "' images added to known peoples list")
        else:
            known_people_names_to_remove.append(i)
            print("ERROR: adding '" + known_people_images[i] + "'")
    

    # now remove the names of images which could not be loaded
    for i in known_people_names_to_remove:
        known_people_names_map.remove(known_people_names_map[i])


    # make the names proper
    for i in range(len(known_people_names_map)):
        known_people_names_map[i] = known_people_names_map[i][:known_people_names_map[i].rfind('_')]


    # Encode all the unknown faces
    images_to_delete = []
    for i in unknown_people_images:
        unknown_picture = face_recognition.load_image_file(base_path+folder_unknown_faces+"/"+str(i))
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)
        if len(unknown_face_encoding) == 0:
            print('Unable to find face. Please take a picture in a well lit location.')
            messageToClient = 'Unable to find face. Please take a picture in a well lit location.'
            images_to_delete.append(True)               
            os.remove(base_path+folder_unknown_faces+"/"+str(i));
            unknown_people_images_encoded.append(None)
        else:
            images_to_delete.append(False)
            unknown_people_images_encoded.append(unknown_face_encoding[0])


    # Now we can see the two face encodings are of the same person with `compare_faces`!
    for i in range(len(unknown_people_images_encoded)):
        if images_to_delete[i]: continue
        results = face_recognition.compare_faces(known_people_images_encoded, unknown_people_images_encoded[i])
        # print(results)
        a_known_face = False
        for j in range(len(results)):
            if results[j] == True:
                #print("'" + str(unknown_people_images[i]) + "' is a known face : " + str(known_people_names_map[j]))
                #print("\n\nHello " + str(known_people_names_map[j])+"!")
                messageToClient = "\n\nHello " + str(known_people_names_map[j])+"!"
                a_known_face = True
                break
        if not a_known_face: 
            #print("Unauthorized person.")
            messageToClient = "Unauthorized person."
        os.remove(base_path+folder_unknown_faces+"/"+unknown_people_images[i]);

    return messageToClient
