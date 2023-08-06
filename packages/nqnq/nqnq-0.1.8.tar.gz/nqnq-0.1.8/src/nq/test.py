import pickle
import os


def add_some(number):
    return lambda x: x + number


def get_bjd_df():

    # 현재 파일 이름
    # print(__file__)

    # 현재 파일 실제 경로
    # print(os.path.realpath(__file__))

    # 현재 파일 절대 경로
    # print(os.path.abspath(__file__))

    data_path = os.path.abspath(__file__).replace("test.py", "data")
    with open(f"{data_path}/bjd_20220401.pkl", "rb") as f:
        return pickle.load(f)
