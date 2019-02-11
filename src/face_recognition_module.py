# USE anaconda / miniconda distribution for easy installation and usage of python and other libraries
# REFER https://github.com/ageitgey/face_recognition
# pip install face_recognition

import face_recognition
import os

base_path = "./face_testing"
folder_known_faces = '/pictures_of_people_i_know'
folder_unknown_faces = '/unknown_pictures'


known_people_names_map = os.listdir(base_path+folder_known_faces)
known_people_names_map.sort()
known_people_names_to_remove = []
known_people_images = known_people_names_map.copy()
known_people_images_encoded = []


unknown_people_images = os.listdir(base_path+folder_unknown_faces)
unknown_people_images.sort()
unknown_people_images_encoded = []


# known_people_images_encoded now contains a universal 'encoding' of all facial features that can be compared to any other picture of a face!
for i in range(len(known_people_images)):
    known_picture = face_recognition.load_image_file(base_path+folder_known_faces+"/"+str(known_people_images[i]))
    known_face_encoding = face_recognition.face_encodings(known_picture)
    if len(known_face_encoding) > 0:
        known_people_images_encoded.append(known_face_encoding[0])
        print("'" + known_people_images[i] + "' images added to known peoples list")
    else:
        known_people_names_to_remove.append(i)
        print("ERROR: adding '" + known_people_images[i] + "'")


# now remove the names of images which could not be loaded
for i in known_people_names_to_remove:
    known_people_names_map.remove(known_people_names_map[i])


# make the names proper
for i in range(len(known_people_names_map)):
    known_people_names_map[i] = known_people_names_map[i][:-7]


# Encode all the unknown faces
for i in unknown_people_images:
    unknown_picture = face_recognition.load_image_file(base_path+folder_unknown_faces+"/"+str(i))
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    unknown_people_images_encoded.append(unknown_face_encoding)


# Now we can see the two face encodings are of the same person with `compare_faces`!
for i in range(len(unknown_people_images_encoded)):
    results = face_recognition.compare_faces(known_people_images_encoded, unknown_people_images_encoded[i])
    print(results)
    a_known_face = False
    for j in range(len(results)):
        if results[j] == True:
            print("'" + str(unknown_people_images[i]) + "' is a known face : " + str(known_people_names_map[j]))
            a_known_face = True
            break
    if not a_known_face: print("'"+"'' is an unknown face.")

