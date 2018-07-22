#!/usr/bin/env python3
"""
Advent of Code 2015 day 4
"""

import hashlib

def part_1(secret_key):
    """ Part 1 of day 4 """
    for i in range(5000000):
        number = hashlib.md5((secret_key + str(i)).encode('utf-8'))
        if str(number.hexdigest())[:5] == "00000":
            print(secret_key + str(i))
            break
    print(number.hexdigest())

def part_2(secret_key):
    """ Part 2 of day 4 """
    for i in range(10000000):
        number = hashlib.md5((secret_key + str(i)).encode('utf-8'))
        if str(number.hexdigest())[:6] == "000000":
            print(secret_key + str(i))
            break
    print(number.hexdigest())

part_1("iwrupvqb")
part_2("iwrupvqb")
