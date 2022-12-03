
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
# 1 for Rock, 2 for Paper, and 3 for Scissors
scores = {"A":1, "B":2, "C":3}

# rules
# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.
whatToPlay={}
# need too lose
whatToPlay[('X','A')]='C'
whatToPlay[('X','B')]='A'
whatToPlay[('X','C')]='B'

# need to draw
whatToPlay[('Y','A')]='A'
whatToPlay[('Y','B')]='B'
whatToPlay[('Y','C')]='C'

# need to win
whatToPlay[('Z','A')]='B'
whatToPlay[('Z','B')]='C'
whatToPlay[('Z','C')]='A'

winScore={}
winScore['X']=[6,0]
winScore['Y']=[3,3]
winScore['Z']=[0,6]

p1TotalScore=0
p2TotalScore=0
symbolToPlay=' '
p1WinScore=0
p2WinScore=0

# Strips the newline character
for line in Lines:
    count += 1
    line=line.strip()
    p1,p2 = line.split(" ")
    print("P1 {} v P2 {}".format(p1,p2))

    # What symobol should we play based on the strategy
    symbolToPlay=whatToPlay[p2,p1]
    
    # Based on the strategy we can immediately determine the win/loose/draw bonus
    p1WinScore,p2WinScore = winScore[p2]

    # Now add up the totals
    p1TotalScore=p1TotalScore+(scores[p1]+p1WinScore)
    p2TotalScore=p2TotalScore+(scores[symbolToPlay]+p2WinScore)


    print("Scores:{} v {}".format(p1TotalScore,p2TotalScore))
        
