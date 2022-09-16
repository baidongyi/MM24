from src.lib_share import *
import threading
import urllib.parse

base_url = "https://www.xrmn5.com"


def download_all_image_in_page(img_url: str, folder: str, num: int):
    wl("download_all_image_in_page:  url=" + img_url, 2)

    try:
        soup = get_soup_by_url(img_url)
        title = soup.find('h1').string
        wl("title = " + title, 2)
    except:
        return num

    save_folder = os.path.join(folder, title)
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    links = soup.find_all('img')

    for link in links:
        url_link = str(link.attrs['src'])
        if url_link.find("upload") > 0:
            img_url = base_url + url_link
            num = num + 1
            file_name = save_folder + "\\" + str(num) + ".jpg"
            save_image_by_url_to_file(file_name, img_url)
    return num


def download_pages(the_url: str, folder: str):
    wl("download_pages url=" + the_url, 2)
    num = 0
    num = download_all_image_in_page(the_url, folder, num)

    for i in range(1, 99):
        my_link = the_url.replace(".html", "_" + str(i) + ".html")
        new_num = download_all_image_in_page(my_link, folder, num)
        if new_num == num:
            return
        else:
            num = new_num


def get_links_in_page1(main_url: str):
    try:
        soup = get_soup_by_url(main_url)
        links = soup.find_all("div", class_="sousuo")
    except:
        return []

    result = []

    for link in links:
        href = str(link.div.h2.a.attrs['href'])
        if href.find(".html") > 0 and len(href) > 10:
            my_link = base_url + href
            print("find my_link 1 = " + my_link)
            result.append(my_link)
    return result


def get_links_in_page2(url: str):
    soup = get_soup_by_url(url)
    links = soup.find_all('a')
    result = []

    for link in links:
        href: str = str(link.attrs['href'])
        if href.find(".html") > 0 and len(href) > 10 and link.has_attr('alt'):
            my_link: str = base_url + href
            print("find my_link 2 = " + my_link)
            result.append(my_link)
    return result


def get_links_in_page(my_view_url: str):
    if my_view_url.find("keyword") > 0:
        return get_links_in_page1(my_view_url)
    else:
        return get_links_in_page2(my_view_url)


def download_image_in_web(my_base_url: str, my_base_folder: str):
    pages: [] = get_links_in_page(my_base_url)
    for page in pages:
        download_pages(page, my_base_folder)


def download_image_in_web_thread(base_url_link: str, my_base_save_folder: str):
    t_list = []
    pages = get_links_in_page(base_url_link)
    for page in pages:
        t = threading.Thread(target=download_pages, args=(page, my_base_save_folder))
        t.start()
        t_list.append(t)

    for t in t_list:
        t.join()


def loop_web(first_url: str, my_base_save_folder: str):
    if first_url.find("keyword") > 0:
        for i in range(0, 10):
            new_url: str = first_url + "&p=" + str(i)
            download_image_in_web_thread(new_url, my_base_save_folder)
    else:
        download_image_in_web_thread(first_url, my_base_save_folder)


def download_by_keyword(keyword: str):
    print("download_by_keyword: = " + keyword)
    new_url = base_url + "/plus/search/index.asp?keyword=" + urllib.parse.quote(keyword)
    print(new_url)
    loop_web(new_url, base_folder)


def download_by_url(down_url: str):
    loop_web(down_url, base_folder)


if __name__ == '__main__':
    base_folder = os.path.join(get_base_folder(), 'mn')

    download_by_url("https://www.xrmn5.com/rm.html")
    download_by_url("https://www.xrmn5.com/tj.html")
    # download_by_keyword("Fish")
    # download_by_keyword("Booty")
    # download_by_keyword("杨晨晨")
    # download_by_keyword("林星阑")
    # download_by_keyword("唐安琪")





