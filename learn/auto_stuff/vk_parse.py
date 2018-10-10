#!/usr/bin/env python3
"""
Using modules requests and beautiful soup 4 to get info from
vk.com profiles
"""

import re
from bs4 import BeautifulSoup as bs
import requests


def pageSoup(address):
    with requests.get(address) as req:
        return bs(req.text, 'lxml')


def getInfo(address):
    soup = pageSoup(address)

    for name in soup.find_all("h2", class_="op_header"):
        print("Name: {}".format(name.getText()))
    for town in soup.find_all("div", class_="pp_info"):
        print("Town: {}".format(town.getText()))
    for pinfo in soup.find_all(class_=re.compile("pinfo")):
        try:
            print("{} {}".format(pinfo.dt.getText(), pinfo.dd.getText()))
        except AttributeError:
            print("Problem with: {}".format(str(pinfo)))


if __name__ == "__main__":
    for i in range(1, 20):
        print("\nInfo of page with ID #{}".format(i))
        address = "https://vk.com/id" + str(i)
        getInfo(address)
