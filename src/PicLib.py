import time

from PIL import Image
from PIL import ImageTk
import tkinter as tk
import random
from src.lib_share import *


class PicLib:
    folder_list = []
    file_list = []
    folder_count: int = 0
    isEmpty: bool = False
    text: str
    days: float
    max: int
    file_index: int
    folder_index:int

    def __init__(self, base_folder: str, my_keyword: str, days: float = 999, max: int = 299):
        self.base_folder = base_folder
        self.keyword = my_keyword
        self.folder_list = []
        self.days = days
        self.file_index = 0
        self.file_list = []
        self.folder_index = 0

        if len(self.keyword) > 0 and self.days <= 9:
            self.days = 9

        for one_folder in os.listdir(self.base_folder):
            full_folder_path = os.path.join(self.base_folder, one_folder)

            folder_mod_time = os.path.getmtime(full_folder_path)
            now_time = float(time.time())
            diff = (now_time - folder_mod_time) / 3600 / 24

            if diff <= self.days:
                if len(self.keyword) > 0:
                    if one_folder.find(self.keyword) >= 0:
                        self.folder_list.append(full_folder_path)
                else:
                    self.folder_list.append(full_folder_path)

            if len(self.folder_list) >= max:
                break

        self.folder_count = len(self.folder_list)
        self.isEmpty = (self.folder_count == 0)
        if self.isEmpty:
            print('PicLib isEmpty = True')
            return

        self.folder_index = random.randint(0, self.folder_count)
        self.curr_folder = self.folder_list[self.folder_index]
        self.file_list = os.listdir(self.curr_folder)
        self.file_index = 0

    def get_next_folder(self) -> str:
        if not self.isEmpty:
            self.folder_index = (self.folder_index + 1) % self.folder_count
            self.curr_folder = self.folder_list[self.folder_index]
            return self.curr_folder

    def get_next_image(self, folder_offset: int, file_offset: int):
        if folder_offset > 0:
            self.folder_index = (self.folder_index + folder_offset) % self.folder_count
            self.curr_folder = self.folder_list[self.folder_index]
            self.file_list = os.listdir(self.curr_folder)
            self.file_index = 0
            if len(self.file_list) == 0:
                return self.get_next_image(1, 0)

        self.file_index = (self.file_index + file_offset) % max(len(self.file_list), 1)

        file_path = os.path.join(self.folder_list[self.folder_index], self.file_list[self. file_index - 1])
        try:
            my_image = Image.open(file_path)
        except:
            os.remove(file_path)
            wl('delete file => ' + file_path)
            my_image = self.get_next_image(0, 1)

        image_num: str = "图片(" + str(self.file_index + 1) + "/" + str(len(self.file_list)) + ") "
        fold_num: str = "图集[" + str(self.folder_index + 1) + "/" + str(len(self.folder_list)) + "] "
        self.text = image_num + fold_num + self.curr_folder

        return my_image

    def get_photo_image(self, folder_offset: int, file_offset: int) -> tk.PhotoImage:
        img = self.get_next_image(folder_offset, file_offset)
        fix_height = 900

        [width, height] = img.size
        if height != fix_height:
            width = int(fix_height / height * width)
            height = fix_height
            img = img.resize((width, height))
        return ImageTk.PhotoImage(img)
