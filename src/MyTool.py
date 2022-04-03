import os
import shutil


def is_folder_empty(folder: str):
    my_folder_list = os.listdir(folder)
    return len(my_folder_list) == 0


def delete_empty_folder(base_folder: str):
    my_list = os.listdir(base_folder)
    i = 0
    max_del = 99999
    for one_folder in my_list:

        one_folder_path = os.path.join(base_folder, one_folder)
        if is_folder_empty(one_folder_path):
            print(one_folder_path + " is Empty, delete")
            shutil.rmtree(one_folder_path)
            i = i + 1

        if i > max_del:
            break


if __name__ == '__main__':
    my_base_folder = r"E:\Pic18\18av"
    delete_empty_folder(my_base_folder)
