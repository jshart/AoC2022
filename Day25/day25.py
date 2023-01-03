from jshSNAFU import SNAFU
from jshSNAFU import *

# read file input.txt into an array of strings
file1 = open('Day25/data/input.txt', 'r')
lines = file1.readlines()


print("### PARSING PROGRAM ###")
snafu = []
grandTotal = 0
# parse each line
for c, line in enumerate(lines):
    line = line.strip()
    # print(line)

    snafu.append(SNAFU(line))
    snafu[c].convertToDec()
    print("{} == {}".format(line, snafu[c].total))

    grandTotal += snafu[c].total

print("Grand total in decimal:{}".format(grandTotal))
v = grandTotal  
print("SNAFU: {}".format(convertToBase5(v)))
print("SNAFU: {}".format(convertToSNAFU(v)))