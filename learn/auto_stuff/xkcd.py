#!/usr/bin/env python3
"""
Sample of downloading images from site
"""

import os
import requests
from bs4 import BeautifulSoup as bs


def getReq(address):
    req = requests.get(address)
    req.raise_for_status()
    return req


def makeSoup(address):
    print("Downloading page: {}".format(address))
    return bs(getReq(address).text, 'lxml')


def down_img(address, folder):
    req = getReq(address)
    print("Downloading image: {}".format(address))
    with open(os.path.join(folder, os.path.basename(address)), 'wb') as f:
        for chunk in req.iter_content(100000):
            f.write(chunk)


def load_comics():
    folder = os.path.join(os.getcwd(), "xkcd")
    os.makedirs(folder, exist_ok=True)
    url = "https://xkcd.com/"
    num = 1
    while not url.endswith('#'):
        soup = makeSoup(url)
        img = soup.select("#comic img")
        if img:
            down_img("http:" + img[0].get("src"), folder)
        else:
            print("Cannot get image #{}".format(num))
        print("Downloaded image #{}".format(num))
        num += 1
        prevLink = soup.select("a[rel='prev']")[0]
        url = "https://xkcd.com/" + prevLink.get("href")


if __name__ == "__main__":
    load_comics()
