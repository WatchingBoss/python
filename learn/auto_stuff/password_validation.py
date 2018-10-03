#!/usr/bin/env python3
"""
Password validation programm
Check if password has:
at least 8 symbols,
uppercase and lowercase letters,
at least one digit
"""
import re


class Validation:
    def __init__(self, ui):
        self.PW = ui
        self.VALID = {"count": False, "digit": False,
                      "lower": False, "upper": False}
        self.FINAL = True
        self.checkValidation()

    def checkValidation(self):
        self.checkCount()
        self.checkDigit()
        self.checkUppercase()
        self.checkLowercase()
        self.isValid()
        self.output()

    def output(self):
        if self.FINAL:
            print("\n'{}' is valid password".format(self.PW))
        else:
            print("\n'{}' is invalid".format(self.PW))

    def isValid(self):
        for i in self.VALID.values():
            if not i:
                self.FINAL = False
                break

    def checkCount(self):
        if len(self.PW) < 8:
            print(" - Less then 8 digits")
        else:
            self.VALID["count"] = True

    def checkDigit(self):
        match = re.findall(r"\d", self.PW)
        if match:
            self.VALID["digit"] = True
        else:
            print(" - No digit")

    def checkUppercase(self):
        match = re.findall(r"[A-Z]", self.PW)
        if match:
            self.VALID["upper"] = True
        else:
            print(" - No uppercase")

    def checkLowercase(self):
        match = re.findall(r"[a-z]", self.PW)
        if match:
            self.VALID["lower"] = True
        else:
            print(" - No lowercase")


def checkUserPassword():
    while True:
        userInput = input("Enter password: ")
        v = Validation(userInput)
        if v.FINAL:
            break
        else:
            print("Try agen")


if __name__ == "__main__":
    checkUserPassword()
