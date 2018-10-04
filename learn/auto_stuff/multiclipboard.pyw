#!/usr/bin/env python3

"""
Save text associated with key to binary file,
show return all used keys and
content stored as value to key.
"""

import shelve
import pyperclip
import sys
import os


dbDir = os.path.join(os.getcwd(), "multicb_files")


def app():
    db = shelve.open(os.path.join(dbDir, "mdb"))

    if len(sys.argv) == 3:
        option = sys.argv[1].lower()
        keyWord = sys.argv[2].lower()

        if option == "save":
            db[keyWord] = pyperclip.paste()
        elif option == "delete":
            if keyWord == "all":
                for k in db.keys():
                    del db[k]
            else:
                del db[keyWord]

    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == "list":
            pyperclip.copy(str(list(db.keys())))
        elif sys.argv[1] in db:
            pyperclip.copy(db[sys.argv[1]])

    db.close()


if __name__ == "__main__":
    app()
