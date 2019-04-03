# python 3
# Description: class to handle face training and recognition requests from the server

print("=== import started (face_recognizer) ===")
import face_recognition
import os
import numpy
import pickle

# the following two lines are used to solve truncated file problem
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
print("=== import complete (face_recognizer) ===")

def mydebug(msg):
    print("DEBUG: "+str(msg))

class FaceRecognizer:
    """
        self.is_valid               : bool tells whether the object is valid or not, whether it will work as required or not
        self.path_to_training_data  : will store the directory path where the training pictures are stored
        self.known_faces_encoded    : this is a list of tuple (name, list of encoded faces)
    """


    def __init__(self, path_to_training_data):
        """
        Parameters:
        path_to_training_data (str): will store the directory path where the training pictures are stored
        """

        path_to_training_data = os.path.abspath(path_to_training_data)
        if os.path.exists(path_to_training_data) and os.path.isdir(path_to_training_data):
            self.is_valid = True
            self.path_to_training_data = path_to_training_data
        else:
            self.is_valid = False
            self.path_to_training_data = ''


    def get_person_index(self, person_name):
        """
        Parameters:
        person_name (str): name of the person whose tuple index is to be returned

        Returns:
        int: index to the tuple with person_name in self.known_faces_encoded
        """

        for i in range(len(self.known_faces_encoded)):
            if self.known_faces_encoded[i][0] == person_name:
                return i
        self.known_faces_encoded.append(tuple([person_name, []]))
        return len(self.known_faces_encoded)


    def train_on_folder_tree(self, delete_image_without_faces = True):
        """
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

        Parameters:
        delete_image_without_faces : boolean value to decide whether to delete the image if no face is found
        """

        folder_path = self.path_to_training_data
        if not os.path.exists(folder_path): return

        known_faces = []
        self.known_faces_encoded = []
        for i in os.listdir(folder_path):
            res = self.__train_on_folder(folder_path + "/" + i, delete_image_without_faces)
            if len(res[1]) == 0: continue
            self.known_faces_encoded.append(res)


    def retrain_on_folder(self, person_name, delete_image_without_faces = True):
        """
        Retrain the object on a particular person_name

        Parameters:
        person_name (str): name of the person to which the image should be added
        delete_image_without_faces (bool): boolean value to decide whether to delete the image if no face is found
        """

        # person_name = folder_path[folder_path.rfind("/")+1:]
        folder_path = self.path_to_training_data + "/" + person_name

        index_to_remove = self.get_person_index(person_name)
        self.known_faces_encoded.pop(index_to_remove)

        res = self.__train_on_folder(folder_path, delete_image_without_faces)
        if len(res[1]) != 0: self.known_faces_encoded.append(res)


    def __train_on_folder(self, folder_path, delete_image_without_faces = True):
        """
        This function will return a tuple of (person name, list of encoded faces)
        If the "folder_path" does not exists, then we return no name and empty list
        person_name: it will be same as the name of the folder being scanned for images

        Parameters:
        folder_path (str): path to the folder which contains multiple images of a person on which the object should be trained
        delete_image_without_faces (bool): boolean value to decide whether to delete the image if no face is found

        Returns:
        tuple: (person name, [multiple encoded faces])
        """

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
            # convert to 128 floating point representation
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


    def train_on_image(self, person_name, image_path, delete_image_without_faces = True):
        """
        Train the object on a single image

        Parameters:
        person_name (str): name of the person to which the image should be added
        image_path  (str): path to the image
        delete_image_without_faces (bool): boolean value to decide whether to delete the image if no face is found

        Returns:
        bool: status denoting if the image was added to self.known_faces_encoded or not.
        """

        index_to_insert = self.get_person_index(person_name)

        known_picture = face_recognition.load_image_file(image_path)
        known_picture_encoded = face_recognition.face_encodings(known_picture)
        if len(known_picture_encoded) == 0:
            # no face found
            print("WARNING: unable to add the file \"" + image_path + "\"")
            if delete_image_without_faces:
                os.remove(image_path)
                print("WARNING: file deleted \"" + image_path + "\"")
            return False
        else:
            # the following line will append all the items of "known_picture_encoded" to "pic_list_encoded"
            print("message: added new image file \"" + image_path + "\"")
            self.known_faces_encoded[index_to_insert][1].extend(known_picture_encoded)
            return True


    def remove_person(self, person_name, delete_all_images = False):
        """
        Used to remove a person from the known faces list

        Parameters:
        person_name       (str): name of the person who is to be removed from the known faces list
        delete_all_images (bool): boolean value to decide whether to delete the folder of person_name or not
        """

        index_to_remove = self.get_person_index(person_name)
        self.known_faces_encoded.pop(index_to_remove)
        if delete_all_images:
            os.system("rm -r " + self.path_to_training_data + "/" + str(person_name))


    def face_detection(self, picture_path, verify_all_faces = True, success_percentage = 0.6, distance_tolerance = 0.6):
        """
        Parameters:
        picture_path        (str): Path to the image to test for authentication
        verify_all_faces    (bool): Decide whether to return the first matched result of all matched faces
        success_percentage  (float): Percentage of images to match to consider the face as known
        distance_tolerance  (float): How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.

        Returns:
        list: a list of tuple (bool is_a_known_face, String name, Float success_fraction, int pictures_matched, int total_pictures)
        """

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
                if results.sum() > (len(i[1]) * success_percentage):
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
        """
        If the image has a face, then the first known face would be returned.
        If no known face found, then [(False, "Unauthorized")] is returned
        If no face found, then [(False, "No face found")] is returned

        Parameters:
        picture_path        (str): Path to the image to test for authentication
        success_percentage  (float): Percentage of images to match to consider the face as known
        distance_tolerance  (float): How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.

        Returns:
        list: list of a single tuple (bool is_a_known_face, String name, Float success_fraction,
                                            int pictures_matched, int total_pictures)
        """
        
        return self.face_detection(picture_path, False, success_percentage, distance_tolerance)


    def save_to_file(self, file_path = "trained_faces.pkl"):
        """
        Save a pickle file at "file_path"

        Parameters:
        file_path (str): path to the file where the class is to be saved
        """

        # open the file for writing
        file_object = open(file_path,'wb') 
        # this writes the object to the file named stored in the variable file_path
        pickle.dump((self.is_valid, self.path_to_training_data, self.known_faces_encoded), file_object)
        # here we close the file object
        file_object.close()


    def load_from_file(self, file_path = "trained_faces.pkl"):
        """
        Load the pickle file located at "file_path"

        Parameters:
        file_path (str): path to the file where the class is to be saved

        Returns:
        bool: denoting the status of the file loading
        """

        # Check if file exists and it contains data or not. If file not found or file is empty, then return False. Else read the content and load the object
        if os.path.isfile("./" + file_path) and os.path.getsize(file_path) != 0:
            # open the file in read mode
            file_object = open(file_path, 'rb')  
            # load the object from the file into class data members
            (self.is_valid, self.path_to_training_data, self.known_faces_encoded) = pickle.load(file_object)  
            return True
        return False


if __name__ == "__main__":
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

# DESCRIPTION: program to reload a particular part of the data-set
# f = FaceRecognizer("./z_face_testing/pictures_of_people_i_know")
# if not a.load_from_file("./z_face_testing/trained_faces.pkl"):
#     a.train_on_folder_tree()
#     a.save_to_file()
# f.retrain_on_folder("person_name")
# f.save_to_file("./z_face_testing/trained_faces.pkl")