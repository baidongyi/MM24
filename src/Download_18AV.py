from src.lib_share import *
import random
import time
import threading


def get_img_url_prefix(img_id: int):
    pre1 = 'http://wbhost3.kk9984.pw/03wpcg/'
    pre2 = 'http://wbhost3.imgscloud.com/03wpcg/'

    if random.randint(1, 9) >= 5:
        pre = pre1
    else:
        pre = pre2

    # wl('Using Web => ' + pre)
    return pre + str(img_id) + '/' + str(img_id) + '_'


def thread_it(f):
    global t_max

    def wrapper(img_id: int, top_folder: str):
        print('start')
        t_list = []
        for i in range(0, t_max):
            t = threading.Thread(target=f, args=(img_id + i, top_folder))
            t.start()
            t_list.append(t)

        for t in t_list:
            t.join()

    return wrapper


@thread_it
def save_image_by_id(img_id: int, folder: str):
    img_url_prefix = get_img_url_prefix(img_id)
    img_url = img_url_prefix + '001.jpg'

    my_folder = os.path.join(folder, str(img_id))

    if is_img_url_valid(img_url):
        if not os.path.exists(my_folder):
            os.mkdir(my_folder)
    else:
        wl('Series ' + str(img_id) + ' => Invalid', 1)
        return

    count_min = 1
    count_max = 199

    for i in range(count_min, count_max):
        if i >= 10:
            file = '0' + str(i) + '.jpg'
        else:
            file = '00' + str(i) + '.jpg'

        img_url = img_url_prefix + file
        save_path = os.path.join(my_folder, str(img_id) + '_' + file)

        result = save_image_by_url_to_file(save_path, img_url)
        if result == 0:
            time.sleep(0.01)
        elif result == 2:
            wl('Not Exists =>' + str(img_id) + '_' + str(i), 1)
            break


def main():
    global t_max
    t_max = 120
    start_index = 32200 # 23570   #24501
    end_index = start_index + 9900
    base_folder = os.path.join(get_base_folder(), '18av')

    for img_id in range(start_index, end_index, t_max):
        save_image_by_id(img_id, base_folder)


if __name__ == '__main__':
    main()
