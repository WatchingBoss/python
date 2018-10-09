#!/usr/bin/env python3
"""
Using zipfile package to backup folder
"""

import os
import zipfile


def initZipName(dirName):
    number = 1
    while True:
        zipFile = os.path.basename(dirName) + '_' + str(number) + ".zip"
        if not os.path.exists(zipFile):
            return zipFile
        number += 1


def addToZip(zipFile, dirName):
    for mainFolder, subFolder, fileName in os.walk(dirName):
        print("Add files in {}".format(mainFolder))
        zipFile.write(mainFolder)

        for each in fileName:
            base = os.path.basename(mainFolder) + '_'
            if not (each.startswith(base) and each.endswith(".zip")):
                zipFile.write(os.path.join(mainFolder, each))


def backUp(dirName):
    dirName = os.path.abspath(dirName)
    zipFile = initZipName(dirName)

    print("Create zip file: {}".format(zipFile))
    backUpZip = zipfile.ZipFile(zipFile, 'w')

    addToZip(backUpZip, dirName)

    backUpZip.close()
    print("Complete")


if __name__ == "__main__":
    backUpPath = input("Enter directory path (ENTER for current)")
    backUp(backUpPath)
