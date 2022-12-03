
import math


# Using readlines()
file1 = open('Day3/data/input.txt', 'r')
Lines = file1.readlines()


# lower case 'a' = 97, uppercase 'A' = 65
def priorityValue(pv):
    if pv >= 97:
        return pv-96
    else:
        return pv-64+26

# read file 3 lines at a time


testLines = []
testCount = 0
runningTotal = 0
for line in Lines:
    line = line.strip()

    if testCount < 3:
        testLines.append(line)
        print("Adding {} to group".format(line))

        testCount += 1
    else:
        print("Group found, testing or common character")
        # we have 3 lines, now check which character is common to all 3
        # loop through each character in the first line
        for i in range(0, len(testLines[0])):
            # get character i from from string testLines
            c = testLines[0][i]

            if (c in testLines[1] and c in testLines[2]):
                # found common character, print it
                print("CC:{}".format(c))

                print("ORD:{} PV:{}".format(ord(c), priorityValue(ord(c))))
                runningTotal += priorityValue(ord(c))
                print("Total:{}".format(runningTotal))
                break

        # reset testCount
        testCount=1

        # clear testLines array
        testLines.clear()
        print("Adding {} to group".format(line))
        testLines.append(line)
