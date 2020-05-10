import shelve
from random import randint
import PySimpleGUI as gui

# TODO Show random word from list of exact topic or from all lists
# TODO Another class for window
# TODO Use Dictionary class's data by Window class


def define_layout():
    layout = [
        [gui.Output(size=(50, 25), key="-Output-", font="12px")],
        [gui.Button("Add new word"), gui.Input(key="-InputNewWord-")],
        [gui.Button("Random word"), gui.Button("All words"), gui.Button("Exit")]
    ]
    return layout


class Dictionary:
    FILE_PATH = "./data/dict"

    def __init__(self, key):
        self.window = gui.Window("Memorize words", define_layout())
        self.key = key
        self.words = []
        self.check_key_existence()
        self.menu()

    def print_random_word(self):
        print("\n Random word: {}".format(self.words[(randint(0, len(self.words) - 1))]))

    def add_new_word(self, new_word):
        self.words.append(new_word)
        self.window["-InputNewWord-"]("")
        print("\nAdded new word in dictionary:\n\t{}".format(new_word))

    def list_words(self):
        self.window["-Output-"]("")
        for i in range(len(self.words)):
            print("{}: {}".format(i + 1, self.words[i]))

    def menu(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Random word"):
                self.print_random_word()
            elif event in (None, "Add new word"):
                self.add_new_word(values["-InputNewWord-"])
            elif event in (None, "All words"):
                self.list_words()
            elif event in (None, "Exit"):
                with shelve.open(Dictionary.FILE_PATH) as file:
                    file[self.key] = self.words
                break

        self.window.close()

    def check_key_existence(self):
        with shelve.open(Dictionary.FILE_PATH) as file:
            if self.key in file:
                self.words = file[self.key]
            else:
                self.words.append(input("Enter your first word to store in dictionary: "))


# TODO Make chose between topics and add them to different keys
# TODO Key is topic
if __name__ == "__main__":
    main_dictionary = Dictionary("dict_1")
