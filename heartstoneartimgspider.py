from bs4 import BeautifulSoup
import requests
import re
from bs4 import SoupStrainer
import time
import os
import socket

socket.setdefaulttimeout(25)
def get_links(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    only_li = SoupStrainer(class_=re.compile("toclevel-1"))
    lis = BeautifulSoup(r.text, "html.parser", parse_only=only_li)
    links = []
    for li in lis:
        link = li.a["href"]
        links.append(link)

    return links


def get_real_links(basic_url, keywords):
    real_links = []
    for keyword in keywords:
        keyword = keyword[1:]
        real_links.append(basic_url+"/"+keyword)
    print(real_links)
    return real_links


# def get_img_links(real_links):
#     all_img_link = []
#     for link in real_links:
#         img_link = []
#         r = requests.get(link)
#         r.encoding = "utf-8"
#         ss = SoupStrainer(class_="image")
#         only_img_a = BeautifulSoup(r.text, "html.parser", parse_only=ss)
#         for img_a in only_img_a:
#             img_link.append(link+img_a["href"])
#         all_img_link.append(img_link)
#         print(all_img_link)
#         break

def get_img_page_links(basic_url, real_link):
    all_img_page_link = []
    r = requests.get(real_link)
    r.encoding = "utf-8"
    ss = SoupStrainer(class_="image")
    only_img_a = BeautifulSoup(r.text, "html.parser", parse_only=ss)
    for img_a in only_img_a:
        all_img_page_link.append(basic_url+img_a["href"])
    print(all_img_page_link)
    return all_img_page_link


def get_all_img_link(all_img_page_link):
    all_img_link = []
    for link in all_img_page_link:
        img_name = link[link.index("File:") + len("File:"):]
        path = "D://python/heartstoneimg/Knights_of_the_Frozen_Throne_full_art/"+img_name
        if os.path.exists(path):
            print(img_name+" exists")
            continue
        else:
            print("requesting:%s"%(link))
            r = requests.get(link)
            r.encoding = "utf-8"
            ss = SoupStrainer(class_="internal")
            img_a = BeautifulSoup(r.text, "html.parser", parse_only=ss)
            print("imag_a:%s" % (img_a))
            print(img_a.a["href"])
            img_link = img_a.a["href"]
            all_img_link.append((img_link, img_name))
            time.sleep(10)
            if len(all_img_link) > 20:
                break
    print(all_img_link)
    return all_img_link


def do_get_img(all_image_link):

    for img_link in all_image_link:
        path = "D://python/heartstoneimg/Knights_of_the_Frozen_Throne_full_art/"+img_link[1];
        if os.path.exists(path):
            print(img_link[1]+" exists.")
            continue
        else:
            print("downloading:%s" % (img_link[0]))
            try:
                pic = requests.get(img_link[0], timeout=60)
            except requests.exceptions.ConnectionError:
                print("fail or timeout!!")
                continue
            # path = "D://python/heartstoneimg/basic_full_art/"+img_link[1]
            print("writing:%s" % (path))
            file = open(path, 'wb')
            file.write(pic.content)
            file.close()
            time.sleep(10)


def start_get_img():
    url = "http://hearthstone.gamepedia.com/Full_art"
    keywords = get_links(url)
    basic_url = "http://hearthstone.gamepedia.com"
    real_links = get_real_links(basic_url, keywords)
    all_img_page_link = get_img_page_links(basic_url, real_links[11])
    all_img_link = get_all_img_link(all_img_page_link)
    do_get_img(all_img_link)

if __name__ == "__main__":
    start_get_img()
