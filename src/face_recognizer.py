print("=== import started (face_recognizer) ===")
import face_recognition
import os
import numpy
import pickle
print("=== import complete (face_recognizer) ===")

def mydebug(msg):
    print("DEBUG: "+str(msg))

class FaceRecognizer:
    '''
        self.is_valid               : bool tells whether the object is valid or not, whether it will work as required or not
        self.path_to_training_data  : will store the directory path where the training pictures are stored
        self.known_faces_encoded    : this is a list of tuple (name, list of encoded faces)
    '''


    def __init__(self, path_to_training_data):
        '''
        self.path_to_training_data will store the directory path where the training pictures are stored
        '''
        path_to_training_data = os.path.abspath(path_to_training_data)
        if os.path.exists(path_to_training_data) and os.path.isdir(path_to_training_data):
            self.is_valid = True
            self.path_to_training_data = path_to_training_data
        else:
            self.is_valid = False
            self.path_to_training_data = ''


    def train_on_folder_tree(self, delete_image_without_faces = False):
        '''
        The directory structure should be like this:
            path_to_training_data/name1/name1_1.png
                                    .../name1_2.png
                                    .../name1_3.png
            path_to_training_data/name2/name2_1.png
                                    .../name2_2.png
                                    .../name2_3.png
            path_to_training_data/name3/name3_1.png
                                    .../name3_2.png
                                    .../name3_3.png
        Due to this, we can compare unknown face with multiple pictures of the same person.
        Example: face with beard, without beard, with makeup, without makeup, with hair cut, without hair cut, and many more cases
        '''

        folder_path = self.path_to_training_data
        folder_path = os.path.abspath(folder_path)
        if not os.path.exists(folder_path): return

        known_faces = []
        self.known_faces_encoded = []
        for i in os.listdir(folder_path):
            res = self.__train_on_folder(folder_path + "/" + i, delete_image_without_faces)
            if len(res[1]) == 0: continue
            self.known_faces_encoded.append(res)


    def __train_on_folder(self, folder_path, delete_image_without_faces = False):
        '''
        This function will return a tuple of (person name, list of encoded faces)
        If the "folder_path" does not exists, then we return no name and empty list
        person_name: it will be same as the name of the folder being scanned for images
        '''
        folder_path = os.path.abspath(folder_path)
        folder_path_exists = os.path.isdir(folder_path)
        pic_list = []
        pic_list_encoded = []

        if folder_path_exists:
            pic_list = os.listdir(folder_path)

        if (not folder_path_exists) or (len(pic_list) == 0):
            return ('',[])

        # person_name = pic_list[0]
        # person_name = person_name[:person_name.rfind("_")]
        person_name = folder_path[folder_path.rfind("/")+1:]
        for i in range(len(pic_list)):
            file_path = folder_path + "/" + pic_list[i]
            # mydebug("loading image: "+ str(file_path))
            known_picture = face_recognition.load_image_file(file_path)
            known_picture_encoded = face_recognition.face_encodings(known_picture)
            if len(known_picture_encoded) == 0:
                # no face found
                print("WARNING: unable to add the file \"" + file_path + "\"")
                if delete_image_without_faces:
                    os.remove(file_path)
                    print("WARNING: file deleted \"" + file_path + "\"")
            else:
                # the following line will append all the items of "known_picture_encoded" to "pic_list_encoded"
                print("message: added new image file \"" + file_path + "\"")
                pic_list_encoded.extend(known_picture_encoded)
        return (person_name, pic_list_encoded)


    def face_detection(self, picture_path, verify_all_faces = True, success_percentage = 0.6, distance_tolerance = 0.6):
        '''
        picture_path        : Path to the image to test for authentication
        verify_all_faces    : Decide whether to return the first matched result of all matched faces
        success_percentage  : Percentage of images to match to consider the face as known
        distance_tolerance  : How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
        returns a list of tuple (bool is_a_known_face, String name, Float success_fraction, int pictures_matched, int total_pictures)
        '''
        if success_percentage > 1: success_percentage = 1
        if (not os.path.exists(picture_path)) or (not os.path.isfile(picture_path)):
            return [(False, 'file does not exists')]

        unknown_picture = face_recognition.load_image_file(picture_path)
        unknown_picture_encoded = face_recognition.face_encodings(unknown_picture)
        if len(unknown_picture_encoded) == 0:
            # no face found
            return [(False, 'no face found')]

        return_value = []
        for i in self.known_faces_encoded:
            for j in unknown_picture_encoded:
                # NOTE: i -> (name, face encodings)
                # results: list of boolean values
                results = face_recognition.compare_faces(i[1], j, distance_tolerance)
                results = numpy.array(results)
                if results.sum() > (len(i) * success_percentage):
                    # (bool is_a_known_face, String name, Float success_fraction, int pictures_matched, int total_pictures)
                    # print(True, i[0], results.sum() / len(i[1]), results.sum(), len(i[1]))
                    if verify_all_faces:
                        return_value.append((True, i[0], results.sum() / len(i[1]), results.sum(), len(i[1])))
                    else:
                        return [(True, i[0], results.sum() / len(i[1]), results.sum(), len(i[1]))]

        if len(return_value) == 0:
            return [(False, 'unauthorized person')]
        else:
            return return_value


    def single_face_detection(self, picture_path, success_percentage = 0.6, distance_tolerance = 0.6):
        return self.face_detection(picture_path, False, success_percentage, distance_tolerance)


    def save_to_file(self, file_name = "trained_faces.pkl"):
        # open the file for writing
        file_object = open(file_name,'wb') 
        # this writes the object to the file named stored in the variable file_name
        pickle.dump((self.is_valid, self.path_to_training_data, self.known_faces_encoded), file_object)
        # here we close the file object
        file_object.close()


    def load_from_file(self, saved_file_name = "trained_faces.pkl"):
        # Check if file exists and it contains data or not. If file not found or file is empty, then return False. Else read the content and load the object
        if os.path.isfile("./" + saved_file_name) and os.path.getsize(saved_file_name) != 0:
            # open the file in read mode
            file_object = open(saved_file_name, 'rb')  
            # load the object from the file into class data members
            (self.is_valid, self.path_to_training_data, self.known_faces_encoded) = pickle.load(file_object)  
            return True
        return False


if __name__ == "__main__":
    # from face_recognition_module_new import *
    a = FaceRecognizer('./z_face_testing/pictures_of_people_i_know')

    print("\n=== Training started ===")
    if not a.load_from_file():
        a.train_on_folder_tree()
        a.save_to_file()
    print("=== Training complete ===")
    # a.save_to_file()

    print("\n=== Face detection started ===")
    path_to_new_pics = os.path.abspath('./z_face_testing/unknown_pictures/')
    for i in os.listdir(path_to_new_pics):
        print("face recognition:", i, a.face_detection(path_to_new_pics + '/' + str(i), True, 0.0, 0.4))
        print("face recognition:", i, a.single_face_detection(path_to_new_pics + '/' + str(i), 0.0, 0.4))
        # print("face recognition:", i, a.face_detection(path_to_new_pics + '/' + str(i), False, 0.5, 0.4))
    print("=== Face detection complete ===")

    # print(a.face_detection('./z_face_testing/unknown_pictures/unknown.jpg', True, 0.6, 0.5))
