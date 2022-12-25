# Importing the library
from enum import IntEnum
import pygame
from pygame.locals import *

# Overall dimensioning and limits - dial these based on display size etc
maxYDraw = 5
maxX = 7
maxY = 40
scale = 3
bs = 60  # Border Size
maxMoves = 9


# working numbers for part 1
# maxYDraw=200
# x = 7
# y = 180
# scale = 5

# note board is laid out board[Y][X]

# 4245 is too high

class minMaxTracker:
    def __init__(self):
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

        self.firstSetDone = False

    def update(self, x, y):
        if self.firstSetDone:
            if x < self.minX:
                self.minX = x
            if x > self.maxX:
                self.maxX = x
            if y < self.minY:
                self.minY = y
            if y > self.maxY:
                self.maxY = y
        else:
            self.minX = x
            self.maxX = x
            self.minY = y
            self.maxY = y
            self.firstSetDone = True

    def print(self):
        print("{},{}-{},{}".format(self.minX, self.minY, self.maxX, self.maxY))

    def drawBox(self):
        pygame.draw.rect(surface, (255, 0, 0), (self.minX * scale, self.minY * scale, (self.maxX - self.minX+1) * scale,
                                                (self.maxY - self.minY+1) * scale), width=2)

    def countEmpty(self,board):
        xRange = self.maxX+1
        yRange = self.maxY+1

        count=0
        print("x in {} range {}".format(self.minX,xRange))
        for x in range(self.minX, xRange):
            for y in range(self.minY, yRange):
                if board.board[y][x] == '.':
                    count+=1
                    pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(x*board.scale, y*board.scale, board.scale, board.scale))

        return count

class Directions(IntEnum):
    North = 0
    South = 1
    West = 2
    East = 3


class OrderTracker:
    s = []

    def __init__(self):
        for e, d in enumerate(Directions):
            self.s.append(e)

    def rotateState(self):
        # rotate the state
        self.s.append(self.s.pop(0))

    def getState(self):
        return self.s


class Board:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.board = [['.' for x in range(width)] for y in range(height)]
        self.pMoves = [[[] for k in range(width)] for j in range(height)]
        self.resetpMoves()
        self.left = 0
        self.top = 0
        self.scale = scale
        self.ot = OrderTracker()
        self.mmTracker = minMaxTracker()

    def updateTracker(self):
        for k in range(self.width):
            for j in range(self.height):

                if self.board[j][k] == '#':
                    self.mmTracker.update(k, j)

    def resetpMoves(self):
        for k in range(self.width):
            for j in range(self.height):
                self.pMoves[j][k].clear()


    # During the first half of each round, each Elf considers the eight positions adjacent to themself.
    # If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
    # Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:
    # If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    # If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    # If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    # If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.

    # *NORMALLY* we'd want to check screen boundaries, but in this case, we the screen to be so large that we never
    # hit the edge. So we're purposely not going to check the boundaries, so that if we ever do go over the edges
    # it forces a crash - and gives us a prompt to fix the sizes.
    def checkCardinalDirections(self, myX, myY):
        #print("Checking moves for ", myX, myY)

        # pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(
        #     myX*self.scale, myY*self.scale, self.scale, self.scale))

        viableMoves = []
        canMoveNorth = tuple()
        canMoveSouth = tuple()
        canMoveEast = tuple()
        canMoveWest = tuple()

        # Check North
        for x in range(myX-1, myX+2):
            # pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(
            #     x*self.scale, (myY-1)*self.scale, self.scale, self.scale), width=2)
            if self.board[myY-1][x] == '.':
                viableMoves.append([x, myY-1])
                # return viableMoves
        #print("North Viable moves: ", viableMoves)
        if len(viableMoves) == 3:
            canMoveNorth = viableMoves[1]
        viableMoves.clear()

        # Check South
        for x in range(myX-1, myX+2):
            # pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(
            #     x*self.scale, (myY+1)*self.scale, self.scale, self.scale), width=2)
            if self.board[myY+1][x] == '.':
                viableMoves.append([x, myY+1])
                # return viableMoves
        #print("South Viable moves: ", viableMoves)
        if len(viableMoves) == 3:
            canMoveSouth = viableMoves[1]
        viableMoves.clear()

        # Check West
        for y in range(myY-1, myY+2):
            # pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(
            #     (myX-1)*self.scale, y*self.scale, self.scale, self.scale), width=2)
            if self.board[y][myX-1] == '.':
                viableMoves.append([myX-1, y])
                # return viableMoves
        #print("West Viable moves: ", viableMoves)
        if len(viableMoves) == 3:
            canMoveWest = viableMoves[1]
        viableMoves.clear()

        # Check East
        for y in range(myY-1, myY+2):
            # pygame.draw.rect(surface, (255, 0, 255), pygame.Rect(
            #     (myX+1)*self.scale, y*self.scale, self.scale, self.scale), width=2)
            if self.board[y][myX+1] == '.':
                viableMoves.append([myX+1, y])
                # return viableMoves
        #print("East Viable moves: ", viableMoves)
        if len(viableMoves) == 3:
            canMoveEast = viableMoves[1]
        viableMoves.clear()

        if len(canMoveNorth) > 0 and len(canMoveSouth) > 0 and len(canMoveWest) > 0 and len(canMoveEast) > 0:
            #print("All directions viable, so do not need to move, standing down")

            me = (myX, myY)
            return me

        #print("N:{} S:{} W:{} E:{}".format(canMoveNorth,canMoveSouth, canMoveWest, canMoveEast))

        for s in self.ot.getState():
            d = Directions(s)
            if d == Directions.North and len(canMoveNorth) > 0:
                return canMoveNorth
            if d == Directions.South and len(canMoveSouth) > 0:
                return canMoveSouth
            if d == Directions.West and len(canMoveWest) > 0:
                return canMoveWest
            if d == Directions.East and len(canMoveEast) > 0:
                return canMoveEast

        me = (myX, myY)
        return me

    def checkViableMoves(self, myX, myY):
        #print("Checking moves for ", myX, myY)

        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(
            myX*self.scale, myY*self.scale, self.scale, self.scale))

        viableMoves = []
        startX = myX
        endX = myX
        startY = myY
        endY = myY
        if myX > 0:
            startX = myX-1
        if myX < self.width - 1:
            endX = myX+1
        if myY > 0:
            startY = myY-1
        if myY < self.height - 1:
            endY = myY+1

        for x in range(startX, endX+1):
            for y in range(startY, endY+1):
                pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(
                    x*self.scale, y*self.scale, self.scale, self.scale), width=1)

                if self.board[y][x] == '.':
                    viableMoves.append([x, y])

        #print(viableMoves)

    def asciiBoard(self):
        print("BL:{}".format(len(self.board)))
        print("RL:{}".format(len(self.board[0])))
        # print the board out
        for row in self.board:
            for cell in row:
                print(cell, end="")
            print()

    def checkCellsForMoves(self):
        me = tuple()

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if (cell == '#'):
                    me = (x, y)
                    #print("Cell Found at {},{}".format(x, y))
                    result = self.checkCardinalDirections(x, y)
                    if (result != me):
                        board.pMoves[result[1]][result[0]].append(me)

    def executeValidMoves(self):
        #print("Executing valid moves")
        count=0
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                l = len(self.pMoves[y][x])

                # whenever we have *exactly* one proposed move, then its valid
                # any other combo is ignored.
                if l == 1:
                    #print("Cell {} has  {} moves".format((x, y), len(self.pMoves[y][x])), end='')
                    #print(" consisting of:{}".format(self.pMoves[y][x]))

                    # this cell is now populated
                    self.board[y][x] = '#'
                    # old cell is now unpopulated
                    temp = self.pMoves[y][x][0]
                    self.board[temp[1]][temp[0]] = '.'

                    count+=1

        self.ot.rotateState()
        #print("#### Next direction checks would be:{}".format(self.ot.getState()))
        return count

    def draw(self, surface):
        cellFilled = (255, 0, 0)
        cellBorder = (125, 125, 125)

        yLen = len(self.board)
        xLen = len(self.board[0])

        cellContent = (255, 255, 255)
        blankCell = (0, 0, 0)

        #print("BL:{}".format(len(self.board)))
        #print("RL:{}".format(len(self.board[0])))
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):

                if (cell == '#'):
                    pygame.draw.rect(surface, cellContent, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale))
                    pygame.draw.rect(surface, cellBorder, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale), width=1)
                else:
                    pygame.draw.rect(surface, blankCell, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale))
                    pygame.draw.rect(surface, cellBorder, pygame.Rect(
                        x*self.scale, y*self.scale, self.scale, self.scale), width=1)

            # You can use `render` and then blit the text surface ...
            # text_surface = myFont.render(str(y), False, (255, 255, 255))
            # surface.blit(text_surface, (0, y*self.scale))

    def addRow(self):
        self.board.insert(0, [0 for x in range(self.width)])

    def addRows(self, n):
        for i in range(n):
            self.board.insert(0, [0 for x in range(self.width)])


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
file1 = open('Day23/data/input.txt', 'r')

# read file input.txt into an array of strings
lines = file1.readlines()
for y in range(len(lines)):
    lines[y] = lines[y].strip()


maxX = len(lines[0])
maxY = len(lines)

maxBoardX = maxX+(bs*2)
maxBoardY = maxY+(bs*2)
# Create an empty board, the size of the input data plus a border all around
board = Board(maxBoardX, maxBoardY, scale)


# Load the input into the centre of the board, offset
# by the bordersize (bs)
for lY in range(maxY):
    for lX in range(maxX):
        board.board[lY+bs][lX+bs] = lines[lY][lX]

# board.asciiBoard()

# setup the display, now we know how big we need it
surface = pygame.display.set_mode((scale*maxBoardX, scale*maxBoardY))

moves = 0
surface.fill((0, 0, 0))
board.draw(surface)
pygame.display.flip()

while True:
    #pygame.time.wait(500)
    # calculate and execute the moves
    # board.checkCardinalDirections(3, 2)
    board.checkCellsForMoves()
    result=board.executeValidMoves()

    moves += 1
    board.resetpMoves()
    print("*** PASS {} complate".format(moves))

    if result==0:
        break

    pygame.display.flip()
    board.draw(surface)


board.updateTracker()
print("Bounding box: ", end='')
board.mmTracker.print()
board.mmTracker.drawBox()
print("Empty Count:{}".format(board.mmTracker.countEmpty(board)))
pygame.display.flip()


# pygame.event.get() is what I need to do an "instant" poll;
# https://www.pygame.org/docs/ref/event.html
# https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
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
