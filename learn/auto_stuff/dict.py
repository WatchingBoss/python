"""
Sample of using dictionaries
"""


def countChars(string):
    chars = {}
    for c in string:
        if c == ' ' or c == '\n':
            continue
        chars.setdefault(c, 0)
        chars[c] += 1
    return chars


def sortDict(dictionary):
    keys = list(dictionary.keys())[:]
    keys.sort(key=str.lower)
    sortDict = {}
    for k in keys:
        sortDict[k] = dictionary[k]
    return sortDict


def firstSample():
    anyString = ""
    with open("text.txt", 'r') as f:
        for line in f:
            anyString += line

    chars = sortDict(countChars(anyString))
    for key in chars.keys():
        print("Char {0:2} repeats {1:2d} times".format(key, chars[key]))
