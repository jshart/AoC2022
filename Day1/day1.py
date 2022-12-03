
import math

def calculateFuel(fuel):
    r=math.floor(fuel/3)
    f=r-2
    if(f<0):
        f=0

    if (f>0):
        f=f+calculateFuel(f)
    return f

# Using readlines()
file1 = open('Day1/data/input.txt', 'r')
Lines = file1.readlines()
  
count = 0
runningTotal=0
totals = []
# Strips the newline character
for line in Lines:
    count += 1

    if len(line.strip())==0:
        print("\tNEW GROUP, last group total:"+str(runningTotal))
        totals.append(runningTotal)
        runningTotal=0
    else:
        print("Line{}: {}".format(count, line.strip()))
        print("\tGROUP, running total:"+str(runningTotal))
        runningTotal=runningTotal+int(line.strip())

for t in totals:
    print("T:{}".format(t))

totals.sort()
print("SORTING")
for t in totals:
    print("T:{}".format(t))

print("Max:{}".format(totals[-1]))

max3=totals[-1]+totals[-2]+totals[-3]
print("Max3:{}".format(max3))

