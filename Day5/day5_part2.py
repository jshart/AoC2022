
import math

# open and read the header file
file1 = open('Day5/data/input_header.txt', 'r')
lines = file1.readlines()

# open and read the instructions file

file2 = open('Day5/data/input_instructions.txt', 'r')
instructions = file2.readlines()

# starting from the end and working backwards loop through lines and print each one out

# create a list of lists
allCrates = [[] for _ in range(9)]

for line in reversed(lines):
    # loop through each character in line
    index = 0
    for c in line.strip():
        print("[{}]".format(c), end="")
        if c != "#":
            allCrates[index].append(c)
        index += 1
    print("_")


# print all elements in allCrates

for crate in allCrates:
    print(crate)

# loop through all the instructions

for instruction in instructions:
    # strip the new character from instruction
    instruction = instruction.strip('\n')

    # split instruction at each comma
    num, src, dest = instruction.split(",")
    print("Move {} from {} to {}".format(num, src, dest))

    n = int(num)
    # reduce by one so we can index from 0
    s = int(src)
    s -= 1
    d = int(dest)
    d -= 1

    cutlist = allCrates[s].copy()
    l = len(cutlist)
    allCrates[s] = cutlist[0:l-n]
    allCrates[d].extend(cutlist[l-n:])


    # loop through allCrates and print each one
    for crate in allCrates:
        print(crate)

for crate in allCrates:
    # if the crate list is not empty print last element
    if len(crate) != 0:
        print(crate[-1])
