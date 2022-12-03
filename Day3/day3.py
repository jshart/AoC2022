
import math


def calculateFuel(fuel):
    r = math.floor(fuel/3)
    f = r-2
    if (f < 0):
        f = 0

    if (f > 0):
        f = f+calculateFuel(f)
    return f


# Using readlines()
file1 = open('Day3/data/input.txt', 'r')
Lines = file1.readlines()


# lower case 'a' = 97, uppercase 'A' = 65
def priorityValue(pv):
    if pv >= 97:
        return pv-96
    else:
        return pv-64+26


runningTotal = 0
for line in Lines:
    line = line.strip()
    print(line)

    # break line into two halves
    first_half = line[:int(len(line)//2)]
    second_half = line[int(len(line)//2):]

    # A = 65 a=97
    # check if a letter is in both the first_half and second_half
    for i in range(len(first_half)):
        if first_half[i] in second_half:
            print(first_half[i])
            print("ORD:{} PV:{}".format(ord(first_half[i]),priorityValue(ord(first_half[i]))))
            runningTotal += priorityValue(ord(first_half[i]))
            print(runningTotal)
            break
