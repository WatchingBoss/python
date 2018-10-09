#!/usr/bin/env python3
"""
Using webbrowser module
"""

import sys
import webbrowser
import pyperclip


def getAddress():
    if len(sys.argv) == 1:
        return pyperclip.paste()
    return ' '.join(sys.argv[1:])


def showMap(address):
    webbrowser.open(address)


if __name__ == "__main__":
    base = "https://www.google.com/maps/place/"
    address = base + getAddress()
    showMap(address)
