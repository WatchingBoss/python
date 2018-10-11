#!/usr/bin/env python3
"""
Sample of using selenium module
"""

from selenium import webdriver


if __name__ == "__main__":
    b = webdriver.Firefox()
    url = "http://vk.com/id"
    for i in range(10, 50):
        b.get(url + str(i))
