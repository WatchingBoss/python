#!/usr/bin/env python3
"""
Playing to 2048 on site
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import random

score = 0


def play_game(browser):
    global score
    html = browser.find_element_by_tag_name("html")
    scoreElem = browser.find_element_by_class_name("best-container")
    while True:
        choose = random.randrange(1, 4)
        if choose == 1:
            html.send_keys(Keys.UP)
        elif choose == 2:
            html.send_keys(Keys.DOWN)
        elif choose == 3:
            html.send_keys(Keys.RIGHT)
        elif choose == 4:
            html.send_keys(Keys.LEFT)
        try:
            if browser.find_element_by_class_name("game-over"):
                break
        except exceptions.NoSuchElementException:
            continue

    localScore = int(scoreElem.text)
    if localScore > score:
        score = localScore
        print("Best score: {}".format(score))

    Again = browser.find_element_by_class_name("retry-button")
    Again.click()
    play_game(browser)


def load_browser():
    browser = webdriver.Firefox()
    browser.get("http://2048game.com/")
    play_game(browser)


if __name__ == "__main__":
    load_browser()
