# too low:
# \-- Final location:84,75 - Direction:0
# \--- Final RESULT:75336

# row: 75
# col: 97
# dir: 0
# 75388

# 84300 is too high

# Importing the library
from enum import IntEnum
import pygame
from pygame.locals import *
import sys

# Overall dimensioning and limits - dial these based on display size etc
maxYDraw = 5
maxX = 7
maxY = 40
scale = 5


class Directions(IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3


class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.outstandingMoves = 0

    def turnRight(self):
        self.direction=Directions((self.direction + 1) % 4)

    def turnLeft(self):
        self.direction=Directions((self.direction - 1) % 4)

    def proposedMoveDelta(self):
        match self.direction:
            case Directions.North:
                return (0, -1)
            case Directions.South:
                return (0, 1)
            case Directions.East:
                return (1, 0)
            case Directions.West:
                return (-1, 0)

    # Facing is 0 for right (>), 1 for down (v)
    # 2 for left (<), and 3 for up (^)
    def getDirectionResult(self):
        match self.direction:
            case Directions.North:
                return 3
            case Directions.South:
                return 1
            case Directions.East:
                return 0
            case Directions.West:
                return 2

    def move(self,board):

        # Only attempt to move if we've any oustanding steps to take
        if self.outstandingMoves<=0:
            return

        # lets check to see what the proposed position would entail
        delta = self.proposedMoveDelta()
        pX = self.x+delta[0]
        pY = self.y+delta[1]

        loopX=False
        loopY=False
        stopMoving=False

        # if we're moving in the X direction and we'd either
        # go off screen or we'd move to space, then we should
        # look to loop instead
        if delta[0] !=0:
            # if pX < 0 or pX >= maxX-1:
            #     #print("*-- looping because of screen")
            #     loopX=True
            if board.board[pY][pX]==' ':
                #print("*-- looping because of space")
                loopX=True
            elif board.board[pY][pX]=='#':
                #print("*-- Stopping because of block")
                stopMoving=True
                
        # Run the same moves for the Y direction
        if delta[1] !=0:
            # if pY < 0 or pY >= maxY-1:
            #     loopY=True
            if board.board[pY][pX]==' ':
                loopY=True
            elif board.board[pY][pX]=='#':
                stopMoving=True

        if loopX==True:
            #print("|-- Looking to Loop X")
            if delta[0]>0: # trying to move right
                # search for a '.' spot starting from the left
                searchStart = [0,self.y]
                while (board.board[searchStart[1]][searchStart[0]]==' '):
                    searchStart[0]+=1
                if board.board[searchStart[1]][searchStart[0]]=='#':
                    stopMoving=True

            elif delta[0]<0: # trying to move left
                # search for a '.' spot starting from the right
                searchStart = [maxX-1,self.y]
                while (board.board[searchStart[1]][searchStart[0]]==' '):
                    searchStart[0]-=1
                if board.board[searchStart[1]][searchStart[0]]=='#':
                    stopMoving=True

        if loopY==True:
            #print("|-- Looking to Loop Y")
            if delta[1]>0: # trying to move down
                # search for a '.' spot starting from the top
                searchStart = [self.x,0]
                while (board.board[searchStart[1]][searchStart[0]]==' '):
                    searchStart[1]+=1
                if board.board[searchStart[1]][searchStart[0]]=='#':
                    stopMoving=True

            elif delta[1]<0: # trying to move up
                # search for a '.' spot starting from the bottom
                searchStart = [self.x,maxY-1]
                while (board.board[searchStart[1]][searchStart[0]]==' '):
                    searchStart[1]-=1
                if board.board[searchStart[1]][searchStart[0]]=='#':
                    stopMoving=True


        if stopMoving==True:
            #print("|-- Obstruction, stopping moves")
            # we've hit an obstruction, so we can't move any further - discard the rest of the movement
            self.outstandingMoves=0
        elif loopX==True or loopY==True:
            #print("|-- Looping to new location {}".format(searchStart))
            self.x = searchStart[0]
            self.y = searchStart[1]
            self.outstandingMoves-=1
            board.heatMap.update(self.x,self.y)
        else:
            #print("|-- Moving delta:{} outstanding:{}".format(delta,self.outstandingMoves))
            self.x+=delta[0]
            self.y+=delta[1]
            self.outstandingMoves-=1
            board.heatMap.update(self.x,self.y)


    def draw(self, surface, scale):
        playerBorder = (125, 125, 125)
        playerContent = (0, 255, 0)
        x = self.x
        y = self.y
        pygame.draw.rect(surface, playerContent, pygame.Rect(
            x*scale, y*scale, scale, scale))
        # pygame.draw.rect(surface, playerBorder, pygame.Rect(
        #     x*scale, y*scale, scale, scale), width=1)


class Instructions:
    def __init__(self, str):
        self.ins = str
        self.index = 0
        self.count = 0

    def finished(self):
        if self.index>=len(self.ins):
            return True
        return False

    def getNextIns(self):
        if self.index>=len(self.ins):
            return None
            
        c = self.ins[self.index]
        ret = ''
        if c == 'R' or c == 'L':
            self.index += 1
            self.count+=1
            return c

        while c.isnumeric() == True:
            ret += c
            self.index += 1
            if self.index>=len(self.ins):
                break
            else:
                c = self.ins[self.index]

        self.count+=1
        return ret

class Heatmap:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(width)] for y in range(height)]
        self.scale = scale
        self.max=0

    def update(self,x,y):
        self.map[y][x]+=1
        if self.map[y][x]>self.max:
            self.max=self.map[y][x]

    def draw(self, surface):

        yLen = len(self.map)
        xLen = len(self.map[0])

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):

                if cell>0:
                    #print("{} ".format(cell),end='')
                    r=223/self.max
                    r*=cell
                    r+=32
                    #print("{} ".format(r),end='')
                    cellContent=(r,0,0)
                    #print(cellContent)
                    pygame.draw.rect(surface, cellContent, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale))


class Board:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.board = [[' ' for x in range(width)] for y in range(height)]
        self.scale = scale
        self.startLocation = None
        self.heatMap = Heatmap(width,height,scale)

    def draw(self, surface):
        cellFilled = (255, 0, 0)
        cellBorder = (125, 125, 125)

        yLen = len(self.board)
        xLen = len(self.board[0])

        cellContent = (255, 255, 255)
        blankCell = (0, 0, 0)

        # print("BL:{}".format(len(self.board)))
        # print("RL:{}".format(len(self.board[0])))
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):

                if (cell == '#'):
                    pygame.draw.rect(surface, cellContent, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale))
                    # pygame.draw.rect(surface, cellBorder, pygame.Rect(
                    #     x*self.scale, y*self.scale, self.scale, self.scale), width=1)
                elif (cell == '.'):
                    pygame.draw.rect(surface, blankCell, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale))
                    # pygame.draw.rect(surface, cellBorder, pygame.Rect(
                    #     x*self.scale, y*self.scale, self.scale, self.scale), width=1)

            # You can use `render` and then blit the text surface ...
            # text_surface = myFont.render(str(y), False, (255, 255, 255))
            # surface.blit(text_surface, (0, y*self.scale))

        self.heatMap.draw(surface)


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
test=False
if (test==True):
    map = open('Day22/data/map_test.txt', 'r')
    ins = open('Day22/data/ins_test.txt', 'r')
else:
    map = open('Day22/data/map.txt', 'r')
    ins = open('Day22/data/ins.txt', 'r')

# read file input.txt into an array of strings
lines = map.readlines()
ins = ins.readlines()
instructions = Instructions(ins[0])

print("ins:{}".format(ins))
print("ins len:{}".format(len(ins[0])))

# #### SETUP THE MAP
# firstly parse the text data to work out dimensions and clean up return codes etc
maxX = 0
maxY = 0
for y in range(len(lines)):
    # remove the trailing whitespace (which is just the return code) from the line
    lines[y] = lines[y].rstrip()

    m = len(lines[y])
    if (m > maxX):
        maxX = m
        print("Reset max:{}".format(maxX))

maxY = len(lines)

maxX+=2
maxY+=2

# After the pre-processing above, we've ended up with the max dimensions of the board
# including dealing with undocumented areas due to the irregular shape
maxBoardX = maxX
maxBoardY = maxY
print("Board size:{}/{}".format(maxX, maxY))
# Create an empty board, the size of the input data plus a border all around
map = Board(maxBoardX, maxBoardY, scale)

#  Now we can fill the board with the data from the text file
for lY in range(len(lines)):  # Each line in the input file
    # we need to grab the len of each line in turn as each
    # line is different lens
    curLineMax = len(lines[lY])
    print("L: {} is Len: {} ".format(lY, curLineMax), end='')
    print("Processing: [{}]".format(lines[lY]))
    for lX in range(curLineMax):  # each cell in this line
        map.board[lY+1][lX+1] = lines[lY][lX]

        # Our start location is the first location with a '.'
        # on the first line. Lets check for this and capture
        # the co-ordinate pair as a tuple on the board class
        if lY == 0:
            if map.board[lY+1][lX+1] == '.':
                if map.startLocation is None:
                    # we store this as (x,y), need to remember this is opposite the
                    # way the grid is stored, due to the way we process the input file
                    map.startLocation = (lX+1, lY+1)

print("Start Location:{}".format(map.startLocation))
player = Player(map.startLocation[0],
                map.startLocation[1], Directions.East)

# setup the display, now we know how big we need it
surface = pygame.display.set_mode((scale*maxBoardX, scale*maxBoardY))

passes = 0
surface.fill((0, 0, 0))
map.draw(surface)
player.draw(surface, map.scale)
pygame.display.flip()
maxMoves = 100


#while passes <= maxMoves and instructions.finished()==False:
while instructions.finished()==False or player.outstandingMoves>0:
    #pygame.time.wait(1000)

    # We only want to fetch another instruction and process it - *if*
    # we've got no move steps to execute.
    if player.outstandingMoves==0:

        # fetch the next instruction, if there are none we're done
        currentInstruction = instructions.getNextIns()
        # if currentInstruction==None:
        #     break

        #print("Execute Instruction:{} count:{}".format(currentInstruction,instructions.count))
        if currentInstruction == 'R':
            #print("|-- Right turn")
            player.turnRight()
        elif currentInstruction == 'L':
            #print("|-- Left turn")
            player.turnLeft()
        else:
            player.outstandingMoves=int(currentInstruction)

    player.move(map)

    #print("|-- Latest Direction:{}".format(Directions(player.direction).name))
    if passes % 100 == 0:
        print("\== PASS {} complate".format(passes))

    map.draw(surface)
    player.draw(surface, map.scale)
    pygame.display.flip()

    passes += 1

    # This code allows us to quit the game by pressing the close
    # on the window etc. For each game loop once we've processed the
    # core logic, we just check for any queued up events to process
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("*** QUIT event called")
            pygame.quit()
            sys.exit()

print("*** Instructions completed")
col=player.x
row=player.y
dirValue=player.getDirectionResult()
print("\-- Final location:{},{} - Direction:{}".format(col,row,dirValue))
rowp=row*1000
colp=col*4
print("\-- Row P:{} Col P:{}".format(rowp,colp))

#The final password is the sum of 1000 times the row, 4 times the column, and the facing.
password = (row*1000)+(4*col)+dirValue
print("\--- Final RESULT:{}".format(password))

# pygame.event.get() is what I need to do an "instant" poll;
# https://www.pygame.org/docs/ref/event.html
# https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
# the below code is what we "fall into" if the main logic completes
# this just holds the program into a final state until we're sure we've
# got any screen shots or info we need
pygame.event.clear()
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")
        if event.key == K_ESCAPE:
            pygame.quit()
            exit()
