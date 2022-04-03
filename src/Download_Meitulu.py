from src.lib_share import *
import threading


def get_img_url_from_web_url(img_page_url: str):
    soup = get_soup_by_url(img_page_url)
    aList = soup.find_all('img', class_="content_img")
    wl(aList[0]['src'], 3)
    return aList[0]['src']


def get_img_url(my_id: str, img_num: int) -> str:
    web = 'http://meitulu.cn/'
    web_url = web + 'item/'
    if img_num == 1:
        img_page_url = web_url + my_id + '.html'
    else:
        img_page_url = web_url + my_id + '_' + str(img_num) + '.html'

    wl('img_page_url = ' + img_page_url, 3)

    return img_page_url


def get_img_ref_url(my_id, img_num) -> str:
    return 'https://mtl.gzhuibei.com/images/img/' + str(my_id) + '//' + str(img_num) + '.jpg'


def save_image_by_id_num(img_id, img_num, bottom_folder) -> int:
    url_ref = get_img_url(img_id, img_num)

    img_url = get_img_url_from_web_url(url_ref)

    file_path = os.path.join(bottom_folder, str(img_id) + '_' + str(img_num) + '.jpg')

    result = save_image_by_url_to_file(file_path, img_url, url_ref)

    # 0 for downloaded successfully , 1 for already exists, 2 for error 404 not found
    if result == 2:
        return 1
    elif result == 0:
        return 0
    else:
        return 0


def remove_char(title: str) -> str:
    my_list = '~!@#$%^&*()-+=\|;:/<>[]{}'
    for char in my_list:
        title = title.replace(char, '_')
    return title


def get_url_title(url) -> str:
    try:
        soup = get_soup_by_url(url)
    except:
        return '404'
    else:
        title = soup.find('h1').string
        wl('Get title: ' + str(title), 2)
        return remove_char(title)


def is_img_id_exist(img_id: str, save_folder: str) -> bool:
    list_folder = os.listdir(save_folder)
    for one_folder in list_folder:
        if one_folder[0:len(img_id)] == img_id and one_folder[-7:] != 'working':
            return True
    return False


def save_image_by_id(img_id, save_folder):
    url = get_img_url(img_id, 1)
    title = get_url_title(url)
    if title == '404':
        wl('ID: ' + str(img_id) + ' => invalid', 1)
        return

    wl(url, 3)

    bottom_folder = os.path.join(save_folder, str(img_id) + '_' + title)

    if not os.path.exists(bottom_folder):
        os.mkdir(bottom_folder)

    for img_num in range(1, 99):
        if save_image_by_id_num(img_id, img_num, bottom_folder) > 0:
            wl('reach Max =' + str(img_num), 1)
            break


def get_link_in_page(url: str) -> list:
    soup = get_soup_by_url(url)
    links = soup.find_all('a', attrs={"target": "_blank"})
    my_links = []
    for link in links:
        url_link = str(link.attrs['href'])
        if url_link.find('item') > 0:
            item = url_link.split('/')[2].replace('.html', '')
            my_links.append(item)
            wl('Get Item => ' + str(item), 3)
    return my_links


def get_link_by_name(name: str, page: int) -> list:
    web = 'http://meitulu.cn/'

    if page > 1:
        url = web + 't/' + name + '/index_' + str(page) + '.html'
    else:
        url = web + 't/' + name

    wl('url => ' + url, 2)

    if get_url_title(url) == '404':
        wl('reach web limit count ', 1)
        return []
    else:
        return get_link_in_page(url)


def save_by_name(name: str, save_folder: str):
    for page in range(1, 1999):
        my_links = get_link_by_name(name, page)

        try:
            if len(my_links) > 0:
                wl('Page ' + str(page) + ' have links count => ' + str(len(my_links)), 1)
                t_list = []
                for img_id in my_links:
                    t = threading.Thread(target=save_image_by_id, args=(img_id, save_folder))
                    t.start()
                    t_list.append(t)

                for t in t_list:
                    t.join()
            else:
                return
        except:
            return


def main():
    base_folder = os.path.join(get_base_folder(), 'meitulu')

    name_list = [ 'xinggan']

    for name in name_list:
        save_by_name(name, base_folder)


if __name__ == '__main__':
    main()
