# 177202 is too low?

# answer;
# 182   (row)
# 42    (col)
# 2     (dir)
# 182170

# # my results;
# *** Instructions completed
# \-- Final location:50,177 - Direction:2
# \-- Row P:177000 Col P:200
# \--- Final RESULT:177202

# error delta is 5*1000 - 4*8 == 4968

import sys
from pygame.locals import *
import pygame
from enum import IntEnum


class Portals:
    def __init__(self):

        # Portal name, start range, end range, exit, entrance
        self.edges = [['A',  [101, 50],  [150, 50], 'v', '^'],
                      ['B',  [150, 1],   [150, 50], '>', '<'],
                      ['C',  [101, 1],   [150, 1], '^', 'v'],
                      ['D',  [51, 1],    [100, 1], '^', 'v'],
                      ['E',  [51, 1],    [51, 50], '<', '>'],
                      ['F',  [51, 51],   [51, 100], '<', '>'],
                      ['F2', [1, 101],   [50, 101], '^', 'v'],
                      ['E2', [1, 101],   [1, 150], '<', '>'],
                      ['D2', [1, 151],   [1, 200], '<', '>'],
                      ['C2', [1, 200],   [50, 200], 'v', '^'],
                      ['G2', [50, 151],  [50, 200], '>', '<'],
                      ['G',  [51, 150],  [100, 150], 'v', '^'],
                      ['B2', [100, 101], [100, 150], '>', '<'],
                      ['A2', [100, 51],  [100, 100], '>', '<']]

    def getPartnerPortal(self, portalName):
        if len(portalName) == 1:
            partnerName = portalName + '2'
        else:
            partnerName = portalName[:-1]

        for edge in self.edges:
            if edge[0] == partnerName:
                return edge
        return None

    def testInPortal(self, x, y):
        for edge in self.edges:
            if x >= edge[1][0] and x <= edge[2][0] and y >= edge[1][1] and y <= edge[2][1]:
                return edge
        return None

    def posInPortal(self, e, x, y):
        # is this portal horizontal or vertical?
        if e[1][1] == e[2][1]:
            # horizontal
            pos = x-min(e[1][0], e[2][0])
        else:
            # vertical
            pos = y-min(e[1][1], e[2][1])
        return (pos)

    def jumpToPartner(self, partnerEdge, offset):
        e=partnerEdge
        if e[1][1] == e[2][1]:
            # horizontal
            pos = min(e[1][0], e[2][0]) + offset
            return [pos, e[1][1]]
        else:
            # vertical
            pos = min(e[1][1], e[2][1]) + offset
            return [e[1][0], pos]

    def draw(self, surface, scale):
        for edge in self.edges:
            x = edge[1][0]*scale
            y = edge[1][1]*scale
            w = abs(edge[2][0]-edge[1][0])*scale
            h = abs(edge[2][1]-edge[1][1])*scale

            w = w if w > 0 else scale
            h = h if h > 0 else scale

            if len(edge[0]) == 1:
                pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(x, y, w, h))
            else:
                pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x, y, w, h))

    def drawLabels(self, surface, scale):
        for edge in self.edges:

            # You can use `render` and then blit the text surface ...
            text_surface = myFont.render(
                edge[0]+" "+edge[3], False, (0, 0, 0), (255, 255, 255))
            x = (edge[1][0] + edge[2][0])/2
            y = (edge[1][1] + edge[2][1])/2
            x *= scale
            y *= scale
            surface.blit(text_surface, (x, y))


# Overall dimensioning and limits - dial these based on display size etc
scale = 5

# these get reset by the file load, so these are just defaults
maxX = 7
maxY = 40


class Directions(IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3

    @ staticmethod
    def portalToDirection(p):
        if p == '^':
            return Directions.North
        elif p == '>':
            return Directions.East
        elif p == 'v':
            return Directions.South
        elif p == '<':
            return Directions.West

    @ staticmethod
    def directionToPortal(d):
        if d == Directions.North:
            return '^'
        elif d == Directions.East:
            return '>'
        elif d == Directions.South:
            return 'v'
        elif d == Directions.West:
            return '<'


class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.outstandingMoves = 0

    def turnRight(self):
        self.direction = Directions((self.direction + 1) % 4)

    def turnLeft(self):
        self.direction = Directions((self.direction - 1) % 4)

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

    def testMove(self,board,portals):
        delta = self.proposedMoveDelta()

        # work out the proposed co-ordinates and direction, this gets
        # over-ridden by the portal transformation if we are traversing
        # a portal
        pX = self.x+delta[0]
        pY = self.y+delta[1]
        newDirection = self.direction

        # are we already inside a portal zone?
        e = portals.testInPortal(player.x, player.y)
        if e != None:
            # we're in a portal - test to see if the direction
            # of travel would move us through the portal?
            if Directions.portalToDirection(e[3]) == self.direction:
                # we are travelling in the direction that the portal
                # faces, so we should move through the portal and reset
                # the direction to the new location

                print("Direction: {} Entering portal:{} pos:{}".format(Directions.directionToPortal(player.direction), e, [player.x, player.y]))
   
                # work out our relative position inside the portal
                pos=portals.posInPortal(e, player.x, player.y)
                print("|- Pos in Portal: {}".format(pos))
                # work out what the partner portal is
                partnerEdge=portals.getPartnerPortal(e[0])
                print("|- Partner portal:{}".format(partnerEdge))
                # given the portal offset and the partner portal lets wrok out the new location
                newLocation= portals.jumpToPartner(partnerEdge,pos)
                print("|- proposed new position:{}".format(newLocation))
                pX = newLocation[0]
                pY = newLocation[1]

                newDirection = Directions.portalToDirection(partnerEdge[4])

        # we've calculated the proposed move. Now we need to check if that destination position
        # is a blocker - if so we ignore and end the move, otherwise we lock in the proposed
        # new position
        if board.board[pY][pX] == ' ':
            print("*-- ERROR - trying to move into open space at:{}".format([pX,pY]))
        elif board.board[pY][pX] == '#':
            #print("*-- Stopping because of block, proposed position was {} direction {}".format([pX,pY],newDirection))
            return False
        
        # if we didnt return above, then we're ok to continue moving
        self.x=pX
        self.y=pY
        self.direction=newDirection
        return True



    def move(self, board, portals):

        # Only attempt to move if we've any oustanding steps to take
        if self.outstandingMoves <= 0:
            return

        result = self.testMove(board, portals)
 
        # NOTE: we could do this directly inside testmove
        if result == False:
            # print("|-- Obstruction, stopping moves")
            # we've hit an obstruction, so we can't move any further - discard the rest of the movement
            self.outstandingMoves = 0
        else:
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
        if self.index >= len(self.ins):
            return True
        return False

    def getNextIns(self):
        if self.index >= len(self.ins):
            return None

        c = self.ins[self.index]
        ret = ''
        if c == 'R' or c == 'L':
            self.index += 1
            self.count += 1
            return c

        while c.isnumeric() == True:
            ret += c
            self.index += 1
            if self.index >= len(self.ins):
                break
            else:
                c = self.ins[self.index]

        self.count += 1
        return ret


class Heatmap:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(width)] for y in range(height)]
        self.scale = scale
        self.max = 0

    def update(self, x, y):
        self.map[y][x] += 1
        if self.map[y][x] > self.max:
            self.max = self.map[y][x]

    def draw(self, surface):

        yLen = len(self.map)
        xLen = len(self.map[0])

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):

                if cell > 0:
                    # print("{} ".format(cell),end='')
                    g = 223/self.max
                    g *= cell
                    g += 32
                    # print("{} ".format(r),end='')
                    cellContent = (0, g, 0)
                    # print(cellContent)
                    pygame.draw.rect(surface, cellContent, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale))


class Board:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.board = [[' ' for x in range(width)] for y in range(height)]
        self.scale = scale
        self.startLocation = None
        self.heatMap = Heatmap(width, height, scale)

    def draw(self, surface):
        cellFilled = (255, 0, 0)
        cellBorder = (125, 125, 125)

        yLen = len(self.board)
        xLen = len(self.board[0])

        cellContent = (255, 255, 0)
        blankCell = (50, 50, 50)

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
                    # pygame.draw.rect(surface, cellBorder, pygame.Rect(
                    #     x*self.scale, y*self.scale, self.scale, self.scale), width=1)
                    pass
                else:
                    pygame.draw.rect(surface, blankCell, pygame.Rect(x*self.scale, y*self.scale, self.scale, self.scale))

            # You can use `render` and then blit the text surface ...
            # text_surface = myFont.render(str(y), False, (255, 255, 255))
            # surface.blit(text_surface, (0, y*self.scale))

        self.heatMap.draw(surface)


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
test = False
if (test == True):
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

# add a one wide border around the whole map so that we dont have any part
# of the shape directly touching a surface edge
maxX += 2
maxY += 2

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
        # by adding +1 here it'll off set the whole data load
        # and leave the first col/row empty - ensuring we have
        # a blank border all the way around
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

portals = Portals()

passes = 0
surface.fill((0, 0, 0))
map.draw(surface)
player.draw(surface, map.scale)
pygame.display.flip()
maxMoves = 100

# while passes <= maxMoves and instructions.finished()==False:
while instructions.finished() == False or player.outstandingMoves > 0:
    #pygame.time.wait(100)

    # We only want to fetch another instruction and process it - *if*
    # we've got no move steps to execute.
    if player.outstandingMoves == 0:

        # fetch the next instruction, if there are none we're done
        currentInstruction = instructions.getNextIns()
        # if currentInstruction==None:
        #     break

        # print("Execute Instruction:{} count:{}".format(currentInstruction,instructions.count))
        if currentInstruction == 'R':
            # print("|-- Right turn")
            player.turnRight()
        elif currentInstruction == 'L':
            # print("|-- Left turn")
            player.turnLeft()
        else:
            player.outstandingMoves = int(currentInstruction)

    player.move(map, portals)

    if passes % 100 == 0:
        print("\== PASS {} complate".format(passes))

    surface.fill((0, 0, 0))
    portals.draw(surface, scale)
    map.draw(surface)
    player.draw(surface, map.scale)
    portals.drawLabels(surface, scale)

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
print("\-- Final location:{},{} - Direction:{}".format(col, row, dirValue))
rowp=row*1000
colp=col*4
print("\-- Row P:{} Col P:{}".format(rowp, colp))

# The final password is the sum of 1000 times the row, 4 times the column, and the facing.
password=(row*1000)+(4*col)+dirValue
print("\--- Final RESULT:{}".format(password))

# pygame.event.get() is what I need to do an "instant" poll;
# https://www.pygame.org/docs/ref/event.html
# https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
# the below code is what we "fall into" if the main logic completes
# this just holds the program into a final state until we're sure we've
# got any screen shots or info we need
pygame.event.clear()
while True:
    event=pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")
        if event.key == K_ESCAPE:
            pygame.quit()
            exit()
