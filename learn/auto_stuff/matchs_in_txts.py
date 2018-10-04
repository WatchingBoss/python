#!/usr/bin/env python3

"""
Search keyword in all text files of
current or given directory
"""

import re
import sys
import os


def searching(textList, key, f):
    for line in textList:
        match = re.search(key, line)
        if not match:
            continue
        print("[{} : {}] -> {}".
              format(f, textList.index(line) + 1, line))


def searchMatch(wDir, key):
    files = os.listdir(wDir)
    for f in files:
        path = os.path.join(wDir, f)
        stream = open(path)
        textList = stream.readlines()
        searching(textList, key, f)
        stream.close()


def userInput():
    wDir = ""
    key = ""
    if len(sys.argv) == 2:
        wDir = str(os.getcwd())
        key = sys.argv[1]
    elif len(sys.argv) == 3:
        wDir = str(sys.argv[1])
        key = sys.argv[2]

    searchMatch(wDir, key)


if __name__ == "__main__":
    userInput()
