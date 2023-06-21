
from PicLib import *
import os


def set_image(cv: tk.Canvas, my_label: tk.Label, my_pic_lib: PicLib, folder_offset: int, file_offset: int):
    photo = my_pic_lib.get_photo_image(folder_offset, file_offset)
    cv.create_image(0, 0, image=photo, anchor='nw')
    cv.image = photo
    text: str = my_pic_lib.text
    my_label.configure(text=text, justify='left')


def view_image(folder_series: str, search_keyword: str, days: float = 3, max_num: int = 299):
    base_path = os.path.join(get_base_folder(), folder_series)

    my_pic_lib = PicLib(base_path, search_keyword, days, max_num)

    root = tk.Tk()
    cv = tk.Canvas(root)
    my_label = tk.Label(root)

    frame = tk.Frame(root, width=100, height=100)

    set_image(cv, my_label, my_pic_lib, 0, 0)

    my_label.pack(side='top')

    cv.pack(side='top', fill='both', expand=1)

    cv.bind('<Double-1>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 10))

    cv.bind('<Button-1>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))
    cv.bind('<Button-2>', lambda event: set_image(cv, my_label, my_pic_lib, 1, 0))
    cv.bind('<Button-3>', lambda event: set_image(cv, my_label, my_pic_lib, 1, 0))

    cv.bind('<MouseWheel>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))

    cv.bind('<Button-4>', lambda event: set_image(cv, my_label, my_pic_lib, 0, -1))
    cv.bind('<Button-5>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))

    frame.bind('<Left>', lambda event: set_image(cv, my_label, my_pic_lib, 0, -1))
    frame.bind('<Right>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 1))
    frame.bind('<Down>', lambda event: set_image(cv, my_label, my_pic_lib, 1, 1))

    frame.bind('<Up>', lambda event: set_image(cv, my_label, my_pic_lib, 0, 10))

    frame.focus_set()
    frame.pack()

    root.mainloop()


if __name__ == '__main__':
    series = ['mn', '18av', 'meitulu', 'eclub']
    index = 0
    keyword = 'Fish'
    days = 21
    max_num = 99
    view_image(series[index % 4], keyword, days, max_num)
