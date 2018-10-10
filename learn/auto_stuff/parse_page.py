#!/usr/bin/env python3
"""
Using BeautifulSoup for parsign html page
"""

import sys
import webbrowser
from bs4 import BeautifulSoup as bs
import requests


def makeSoup(address):
    req = requests.get(address)
    req.raise_for_status()
    return bs(req.text, 'lxml')


def openTabs(search):
    address = "https://www.google.com/search?q=" + ' '.join(search)
    soup = makeSoup(address)
    links = soup.select("cite")
    for i in range(4):
        webbrowser.open(links[i].getText())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Using: [name] <Search request>")
        sys.exit()
    openTabs(sys.argv[1:])
