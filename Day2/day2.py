
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
file1 = open('Day2/data/input.txt', 'r')
Lines = file1.readlines()
  
count = 0
runningTotal=0
totals = []

# A for Rock, B for Paper, and C for Scissors.
# X for Rock, Y for Paper, and Z for Scissors.
# 1 for Rock, 2 for Paper, and 3 for Scissors
scores = {"A":1, "B":2, "C":3, "X":1, "Y":2, "Z":3}

# rules
# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
win={}
win[('X','C')]=[6,0]
win[('Y','A')]=[6,0]
win[('Z','B')]=[6,0]

win[('X','A')]=[3,3]
win[('Y','B')]=[3,3]
win[('Z','C')]=[3,3]

win[('X','B')]=[0,6]
win[('Y','C')]=[0,6]
win[('Z','A')]=[0,6]

p1TotalScore=0;
p2TotalScore=0;
# Strips the newline character
for line in Lines:
    count += 1
    line=line.strip()
    p1,p2 = line.split(" ")
    print("P1 {} v P2 {}".format(p1,p2))
    print("P1 s {} v P2 s {}".format(scores[p1],scores[p2]))

    # Calculate the scores for the individual shapes selected
    s1 = scores[p1]
    s2 = scores[p2]
    p1TotalScore = p1TotalScore+scores[p1]
    p2TotalScore = p2TotalScore+scores[p2]

    # Calculate the win value
    p2RoundWin,p1RoundWin = win[p2,p1]
    p2TotalScore = p2TotalScore+p2RoundWin
    p1TotalScore = p1TotalScore+p1RoundWin


    print("Scores:{} v {}".format(p1TotalScore,p2TotalScore))
        
