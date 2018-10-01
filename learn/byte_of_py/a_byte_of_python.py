#!python3
import os


def print_format():
    print("{:.3f}".format(1.0/3.0))
    print("{:-^10}".format("String"))
    print("1: {first} 2: {second}".format(second="Apple", first="Orange"))
    print(r"Without escape sequences \n")


def number_system(num):
    for i in range(num):
        print("Binary: {0:8b} Octal: {0:3o} Decimal: {0:3d} \
        Hex:{0:3x}".format(i))


def data_structures():
    # List
    someList = ["first", "second", "third"]
    # Tuple
    someTuple = ("first", "second", "third")
    # Dictionary
    someDictionary = {"first": "Apple", "second": "Orange", "third": "Potato"}
    # Set
    someSet = set(["first", "second", "third"])

    # Make reference to list
    refToList = someList
    # Make copy of list
    copyOfList = someList[:]

    print(someTuple[0])
    print(someDictionary["second"])
    print(someSet)

    someList[0] = "Not first HOHO"
    print(refToList)
    print(copyOfList)


class shape:
    shapeCount = 0

    def __init__(self, height, width):
        self.height = height
        self.width = width
        shape.shapeCount += 1
        print("Height: {} Width: {}".format(self.height, self.width))

    def showDimantion(self):
        print("Height: {}\tWidth: {}".format(self.height, self.width))

    def newSize(self, height=0, width=0):
        if height:
            self.height = height
        if width:
            self.width = width

    @classmethod
    def showShapeCount():
        print("Total count of shapes: {}".format(shape.shapeCount))


def useShapeClass():
    rect = shape(15, 20)
    rect.newSize(45, 53)
    rect.showDimantion()
    secondRect = shape(10, 23)
    secondRect.showDimantion()
    shape.showShapeCount()


class shape3D:
    """Here we are using inheritance"""

    def __init__(self,  height, width, length):
        shape.__init__(self, height, width)
        self.length = length
        print("Length of cube: {}".format(self.length))

    def showDimantion(self):
        print("Height: {}\tWidth: {}\tLength: {}"\
              .format(self.height, self.width, self.length))


def use3Dshape():
    cube = shape3D(10, 15, 25)
    cube.showDimantion()


def writeToFile(fName):
    f = open(fName, "w")
    try:
        for line in range(3):
            string = input()
            f.write(string + '\n')
    except EOFError:
        f.close()


def readFromFile(fName):
    with open(fName, "r") as f:
        for line in f:
            print(line)


def usingFile(fName):
    writeToFile(fName)
    readFromFile(fName)


def deleteFile(fName):
    try:
        os.remove(fName)
    except FileNotFoundError:
        print("No such file: {}".format(fName))
    finally:
        print("File '{}' removed".format(fName))


def jobWithList():
    newList = [i for i in range(20) if not i % 2]
    for i in newList:
        print(i, end=" ")
    print()
