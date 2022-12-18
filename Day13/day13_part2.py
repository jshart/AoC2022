# read file input.txt into an array of strings
from functools import cmp_to_key
#file1 = open('Day13/data/input_test.txt', 'r')
file1 = open('Day13/data/input.txt', 'r')

Lines = file1.readlines()

packets = []

print("### PARSING PROGRAM ###")
# parse each line
for line in Lines:
    line = line.strip()
    if (len(line) > 0):
        packets.append(eval(line))
print("### PARSING COMPLETE ###")
packets.append([[2]])
packets.append([[6]])


# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/13.py
def compare(p1, p2):
    #print("Comparing {} with {} ".format(p1, p2), end='')
    if isinstance(p1, int) and isinstance(p2, int):
        print("Both ints")
        if p1 < p2:
            return -1
        elif p1 == p2:
            return 0
        else:
            return 1
    elif isinstance(p1, list) and isinstance(p2, list):
        print("Both lists")
        i = 0
        while i < len(p1) and i < len(p2):
            c = compare(p1[i], p2[i])
            if c == -1:
                return -1
            if c == 1:
                return 1
            i += 1
        if i == len(p1) and i < len(p2):
            return -1
        elif i == len(p2) and i < len(p1):
            return 1
        else:
            return 0
    elif isinstance(p1, int) and isinstance(p2, list):
        print("int/list")

        return compare([p1], p2)
    else:
        print("list/int {} {}".format(type(p1), type(p2)))

        return compare(p1, [p2])


p1 = []
p2 = []
# from the example code; https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/13.py
packets = sorted(packets, key=cmp_to_key(lambda p1, p2: compare(p1, p2)))

for i, p in enumerate(packets):
    print(p)

part2 = 1
for i,p in enumerate(packets):
    if p==[[2]] or p==[[6]]:
        part2 *= i+1
print(part2)