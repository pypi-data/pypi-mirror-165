import pickle
import os


def getData(file_name):
    # print(os.path.abspath(__file__))

    data_file_path = os.path.abspath(__file__).replace("__init__.py", file_name)
    with open(data_file_path, "rb") as f:
        return pickle.load(f)


def getFiles():
    data_dir_path = os.path.abspath(__file__).replace("__init__.py", '')
    return os.listdir(data_dir_path)
