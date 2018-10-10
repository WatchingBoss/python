#!/usr/bin/env python3
"""
Using requests module
"""

import requests


def getFileInfo(fileAddress):
    dFile = requests.get(fileAddress)
    try:
        dFile.raise_for_status()
    except Exception as ex:
        print("Problem: ".format(ex))
    print("Info about {}:\n\
    length: {}".format(dFile, len(dFile.text)))


if __name__ == "__main__":
    getFileInfo("https://github.com/30-seconds/30-seconds-of-code/blob/master/README.md")
