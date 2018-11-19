#!/usr/bin/env python3
"""
Sample of downloading images from site
"""

import os
import threading as thr
import requests
from bs4 import BeautifulSoup as bs


def get_req(address):
    req = requests.get(address)
    req.raise_for_status()
    return req


def make_soup(address):
    print("Downloading page: {}".format(address))
    return bs(get_req(address).text, 'lxml')


def down_img(address, folder):
    req = get_req(address)
    print("Downloading image: {}".format(address))
    with open(os.path.join(folder, os.path.basename(address)), 'wb') as img:
        for chunk in req.iter_content(100000):
            img.write(chunk)


def img_from_soup(folder, soup, num):
    img = soup.select("#comic img")
    if img:
        down_img("http:" + img[0].get("src"), folder)
        print("Downloaded image #{}".format(num))
    else:
        print("Cannot get image #{}".format(num))


def load_comics(folder, start, end):
    url = "https://xkcd.com/"
    num = start
    for url_num in range(start, end):
        url = "https://xkcd.com/" + url_num
        soup = make_soup(url)
        img_from_soup(folder, soup, num)
        num += 1


def load_comics_multy_threading():
    folder = os.path.join(os.getcwd(), "xkcd")
    os.makedirs(folder, exist_ok=True)

    all_threads = []
    end_image = 1500
    for num in range(0, end_image, 100):
        thread = thr.Thread(target=load_comics, args=(folder, num, num + 99))
        all_threads.append(thread)
        thread.start()

    for thread in all_threads:
        thread.join()

    print("{} have been downloded".format(end_image))


if __name__ == "__main__":
    load_comics_multy_threading()
