""" Advent to code day 6 """

import re

SANTA_INST = open("./day_6.txt", 'r')

def part_1(instructions):
    """ Part 1 of day 6 """

    lit = 0
    lights = [[0 for i in range(1000)] for j in range(1000)]

    for inst in instructions:
        commands = re.search(r'turn on|turn off|toggle', inst)
        command = commands[0]
        numbers = [int(s) for s in re.findall(r'\b\d+\b', inst)]

        if command == "turn on":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] = 1
        elif command == "turn off":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] = 0
        elif command == "toggle":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] ^= 1

    lit = (sum(sum(l) for l in lights))

    print("{} lights are lit".format(lit))

def part_2(instructions):
    """ Part 2 of 6 day """

    brightness = 0
    lights = [[0 for i in range(1000)] for j in range(1000)]

    for inst in instructions:
        commands = re.search(r'turn on|turn off|toggle', inst)
        command = commands[0]
        numbers = [int(s) for s in re.findall(r'\b\d+\b', inst)]

        if command == "turn on":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] += 1
        if command == "turn off":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    if lights[i][j]:
                        lights[i][j] -= 1
                    else:
                        continue
        if command == "toggle":
            for i in range(numbers[1], numbers[3] + 1):
                for j in range(numbers[0], numbers[2] + 1):
                    lights[i][j] += 2

    brightness = (sum(sum(b) for b in lights))

    print("Sum of brights of light equal {}".format(brightness))

part_1(SANTA_INST)
part_2(SANTA_INST)
