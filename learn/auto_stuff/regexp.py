#!/usr/bin/env python3
"""
Sample of using regular expressions

So, what I want to parse?
For example, I wish to get all dates
which format (DAY MONTH YEAR)
from text in data buffer.
This format used in 'References' on wikipedia.org
"""

import re
import sys
import pyperclip


class parseText:
    def __init__(self, text=""):
        if not len(text):
            self.text = self.storeBuffer()
        else:
            self.text = text
        self.printDates()

    def storeBuffer(self):
        return str(pyperclip.paste())

    def getFormat(self, name):
        names = ["date"]
        if name == names[0]:
            return re.compile(r"""(
            (\d{1,2})        # Day
            (\s|\.|\/|\\|\,) # Separator
            ([a-zA-Z]+)      # Month
            (\s|\.|\/|\\|\,) # Separator
            (\d{4})          # Year
            )""", re.X)
        return 0

    def findDates(self):
        day, month, year = [], [], []
        dateFormat = self.getFormat("date")
        matches = dateFormat.findall(self.text)
        for m in matches:
            day.append(m[1])
            month.append(m[3])
            year.append(m[5])
        return [day, month, year]

    def printDates(self):
        dates = self.findDates()
        if not len(dates):
            print("No dates of format (DAY MONTH YEAR) in clipboarded text")
            sys.exit()
        print("All dates of format (DAY MONTH YEAR) in clipboearded text")
        for d in range(len(dates[0])):
            print("{:3}: {:3} {:9} {}".
                  format(d + 1, dates[0][d], dates[1][d], dates[2][d]))


if __name__ == "__main__":
    printDate = parseText()
