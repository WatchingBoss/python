#!/usr/bin/env python3

"""
Rename file names of directory from american style dates to
Europe style or reverse.
I don't have such files, hence I'll first create them
"""

import os
import re
import shutil
import random


def getDir():
    dirName = input("Enter directory name (ENTER if current): ")
    if not dirName:
        dirName = os.getcwd()
    else:
        dirName = os.path.abspath(dirName)
    return dirName


class createFiles():
    def __init__(self):
        os.chdir(getDir())
        number = int(input("Enter number of files: "))
        self.fillDir(number)

    def fillDir(self, number):
        for i in range(number):
            self.addFile()

    def addFile(self):
        month, day, year = self.getDate()
        name = "text_befor_" + month + '-' + day \
               + '-' + year + "_text_after"
        self.createFile(name)

    def createFile(self, name):
        f = open(name, 'w')
        f.write("This is just testing file")
        f.close()

    def addZero(self, num):
        if num < 10:
            return '0' + str(num)
        else:
            return str(num)

    def getDate(self):
        month = self.addZero(random.randrange(1, 12))
        day = self.addZero(random.randrange(1, 31))
        year = str(random.randrange(1900, 2017))
        return month, day, year


class renameFiles:
    def __init__(self):
        os.chdir(getDir())
        self.regex = self.getRegex()
        self.renameAll()

    def renameAll(self):
        for f in os.listdir():
            self.renameThisFile(f)

    def renameThisFile(self, f):
        match = self.regex.search(f)
        if not match:
            return
        newName = self.rename(match)
        self.renameFile(f, newName)

    def getRegex(self):
        # (1 - string)(2 - day)(5 - month)(8 - year)(10 - string)
        regex = re.compile(r"""(.*?)
        ((0|1)?\d)            # day
        (_|-|\.|\,)           # separator
        ((0|1|2|3)?\d)        # month
        (_|-|\.|\,)           # separator
        ((19|20)\d\d)         # year
        (.*?)$""", re.X)
        return regex

    def rename(self, old):
        newName = old.group(1) + old.group(5) + '-' + old.group(2) + '-'\
                  + old.group(8) + old.group(10)
        return newName

    def renameFile(self, oldName, newName):
        shutil.move(oldName, newName)


def userInput():
    print("What do you want to do?\n\
    1. Rename with changing style (American to Europe or otherwise)\n\
    2. Create files with American style dates in names\n")
    choise = int(input("Choose (enter number): "))
    if choise == 1:
        renameFiles()
    elif choise == 2:
        createFiles()
    else:
        print("Invalid input! What are you looking for?")


if __name__ == "__main__":
    userInput()
