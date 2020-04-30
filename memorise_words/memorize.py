import shelve
from random import randint

# TODO Add GUI

# TODO Show random word from list of exact topic or from all lists


class Dictionary:
    FILE_PATH = "./data/dict"

    def __init__(self, key):
        self.key = key
        self.words = []
        self.check_key_existence()
        self.menu()

    def print_random_word(self):
        print(self.words[(randint(0, len(self.words) - 1))])

    def add_new_word(self):
        self.words.append(input("Enter new word: "))

    def list_words(self):
        for i in range(len(self.words)):
            print("{}: {}".format(i + 1, self.words[i]))

    def menu(self):
        while True:
            print("""Choose next option:
            1. Show random word from dictionary
            2. Add new word to dictionary
            3. List all word in dictionary
            4. Exit""")
            option = int(input("Enter chose: "))
            if option == 1:
                self.print_random_word()
            elif option == 2:
                self.add_new_word()
            elif option == 3:
                self.list_words()
            elif option == 4:
                with shelve.open(Dictionary.FILE_PATH) as file:
                    file[self.key] = self.words
                break
            else:
                continue

    def check_key_existence(self):
        with shelve.open(Dictionary.FILE_PATH) as file:
            if self.key in file:
                words = file[self.key]
            else:
                self.words.append(input("Enter your first word to store in dictionary: "))


# TODO Make chose between topics and add them to different keys
# TODO Key is topic
if __name__ == "__main__":
    main_dictionary = Dictionary("dict_1")
