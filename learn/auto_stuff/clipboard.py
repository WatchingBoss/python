# Sample of using module pyperclip

import pyperclip


def outFromBuffer():
    buffer = pyperclip.paste()
    print("This is in current buffer: {}".format(buffer))


def makeBufferUppercase():
    buffer = pyperclip.paste()
    newBuffer = buffer.upper()
    pyperclip.copy(newBuffer)


makeBufferUppercase()
