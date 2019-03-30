# python 2/3
import os

SERVER_MAIN_DATA_FOLDER = "./z_face_testing"
SERVER_KNOWN_FACES_FOLDER = SERVER_MAIN_DATA_FOLDER + "/" + "pictures_of_people_i_know"
SERVER_UNKNOWN_FACES_FOLDER = SERVER_MAIN_DATA_FOLDER + "/" + "unknown_pictures"
SERVER_LOADED_DATASET_PATH = SERVER_MAIN_DATA_FOLDER + "/" + "trained_faces.pkl"
SERVER_PATHS = (SERVER_MAIN_DATA_FOLDER, SERVER_KNOWN_FACES_FOLDER, SERVER_UNKNOWN_FACES_FOLDER)

CLIENT_MAIN_DATA_FOLDER = "./face_testing"
CLIENT_KNOWN_FACES_FOLDER = CLIENT_MAIN_DATA_FOLDER + "/" + "pictures_of_people_i_know"
CLIENT_UNKNOWN_FACES_FOLDER = CLIENT_MAIN_DATA_FOLDER + "/" + "unknown_pictures"
CLIENT_PATHS = (CLIENT_MAIN_DATA_FOLDER, CLIENT_KNOWN_FACES_FOLDER, CLIENT_UNKNOWN_FACES_FOLDER)

def initialize_server_paths():
    for i in SERVER_PATHS:
        if not os.path.exists(i):
            os.makedirs(i)

def initialize_client_paths():
    for i in CLIENT_PATHS:
        if not os.path.exists(i):
            os.makedirs(i)
