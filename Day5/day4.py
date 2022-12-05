
import math


# Using readlines()
file1 = open('Day4/data/input.txt', 'r')
Lines = file1.readlines()

# This function checks for overlapping ranges between 2 pairs of numbers


def totalOverLap(s1, e1, s2, e2):

    # is range 1 (s1-e1) inside range 2 (s2-e2)
    # start in range
    if s1 >= s2 and s1 <= e2:
        # end in range
        if e1 >= s2 and e1 <= e2:
            print("R1 in R2 {},{}-{},{} OL:{}".format(s1, e1, s2, e2, 1))
            return 1

    # is range 2 (s2-e2) inside range 1 (s1-e1)
    # start in range
    if s2 >= s1 and s2 <= e1:
        # end in range
        if e2 >= s1 and e2 <= e1:
            print("R2 in R1 {},{}-{},{} OL:{}".format(s1, e1, s2, e2, 1))
            return 1

    print("No overlap {},{}-{},{} OL:{}".format(s1, e1, s2, e2, 0))
    return 0


runningTotal = 0
overLapCount = 0
result = 0
for line in Lines:
    line = line.strip()

    # split line into an array by commas
    sl = line.split(',')

    # check the individual ranges to see if they completely overlap
    result = totalOverLap(int(sl[0]), int(sl[1]), int(sl[2]), int(sl[3]))
    # print("{},{}-{},{} OL:{}".format(sl[0], sl[1], sl[2], sl[3], result))
    overLapCount += result

print("Answer:{}".format(overLapCount))

print(totalOverLap(9, 79, 10, 79))
print(totalOverLap(81, 95, 96, 99))

# 9,79-10,79 OL:0
# 9,79-10,79 OL:1
