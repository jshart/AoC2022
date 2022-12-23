
# Importing the library
from enum import IntEnum
import pygame
from pygame.locals import *


class Moves(IntEnum):
    BOTTOM=0
    IGNORE=1
    ALLOWED=2
    COLLISION=3

class Directions(IntEnum):
    DOWN=0
    RIGHT=1
    LEFT=2

# note board is laid out board[Y][X]
class Board:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.left = 0
        self.top = 0
        self.scale = scale

    def moveAllowed(self, newx, newy):
        if newy>=self.height:
            return Moves.BOTTOM
        if newx<0 or newx >=self.width:
            return Moves.IGNORE
        if self.board[newy][newx]>0:
            return Moves.COLLISION

        return Moves.ALLOWED

    def asciiBoard(self):
        # print the board out
        for row in self.board:
            for cell in row:
                if cell == 0:
                    print('.', end='')
                elif cell == 1:
                    print('#', end='')
                elif cell == 2:
                    print('Z', end='')
            print()

    def draw(self, surface):
        cellFilled = (255, 0, 0)
        cellBorder = (125, 125, 125)

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == 0:
                    cellContent = (0, 0, 0)
                elif cell == 1:
                    cellContent = cellFilled
                elif cell == 2:
                    cellContent = cellFilled

                pygame.draw.rect(surface, cellContent, pygame.Rect(
                    x*self.scale, y*self.scale, self.scale, self.scale))
                pygame.draw.rect(surface, cellBorder, pygame.Rect(
                    x*self.scale, y*self.scale, self.scale, self.scale), width=1)

    def addRow(self):
        self.board.insert(0, [0 for x in range(self.width)])


class JetPattern:
    def __init__(self, instructions):
        self.ins = instructions
        self.index = 0
        print("JetPattern initiatlised with length:{}".format(len(self.ins)))

    def getIns(self):
        i = self.ins[self.index]
        print("Ins [{}] at index:{}".format(i, self.index))

        self.index += 1
        if self.index >= len(self.ins):
            print("--> Instructions wrapping")
            self.index = 0

        return i


class TType(IntEnum):
    HLINE = 0
    CROSS = 1
    BL = 2
    VLINE = 3
    BOX = 4


class Tetromino:

    # hLine = [1, 1, 1, 1]
    # cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    # bL = [[0, 0, 1], [0, 0, 1], [1, 1, 1]]
    # vLine = [[1], [1], [1], [1]]
    # box = [[1, 1], [1, 1]]

    def __init__(self, type):
        self.type = type

    def getShape(self):
        match self.type:
            case TType.HLINE:
                return [[1, 1, 1, 1]]
            case TType.CROSS:
                return [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
            case TType.BL:
                return [[0, 0, 1], [0, 0, 1], [1, 1, 1]]
            case TType.VLINE:
                return [[1], [1], [1], [1]]
            case TType.BOX:
                return [[1, 1], [1, 1]]

    def printShape(self):
        print(self.getShape())

    def printAsciiShape(self):
        s = self.getShape()
        y = len(s)
        x = len(s[0])
        for i in range(y):
            for j in range(x):
                if (s[i][j] == 1):
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def draw(self, surface, scale, xoffset, yoffset):
        cellFilled = (0, 255, 0)
        cellBorder = (125, 125, 125)

        s = self.getShape()

        for y, row in enumerate(s):
            for x, cell in enumerate(row):
                if cell == 0:
                    cellContent = (0, 0, 0)
                elif cell == 1:
                    cellContent = cellFilled
                elif cell == 2:
                    cellContent = cellFilled

                tx = x+xoffset
                ty = y+yoffset
                pygame.draw.rect(surface, cellContent, pygame.Rect(
                    tx*scale, ty*scale, scale, scale))
                pygame.draw.rect(surface, cellBorder, pygame.Rect(
                    tx*scale, ty*scale, scale, scale), width=1)

    def checkMove(self,cx,cy,board,direction):
        s = self.getShape()

        for y, row in enumerate(s):
            for x, cell in enumerate(row):
                # check each element in the Tetromino to see if
                # hits anything
                match direction:
                    case Directions.DOWN:
                        result=board.moveAllowed(cx+x,cy+y+1)
                        if result==Moves.BOTTOM or result==Moves.COLLISION:
                            return Moves.COLLISION
                    case Directions.RIGHT:
                        result=board.moveAllowed(cx+x+1,cy+y)
                        if result==Moves.IGNORE or result==Moves.COLLISION:
                            return Moves.IGNORE
                    case Directions.LEFT:
                        result=board.moveAllowed(cx+x-1,cy+y)
                        if result==Moves.IGNORE or result==Moves.COLLISION:
                            return Moves.IGNORE

        return Moves.ALLOWED

nextTetromino = TType.HLINE


def getNextTetromino():
    global nextTetromino
    t = nextTetromino

    nextTetromino += 1
    if nextTetromino > TType.BOX:
        nextTetromino = TType.HLINE

    return t


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
file1 = open('Day17/data/input_test.txt', 'r')

# read file input.txt into an array of strings
lines = file1.readlines()

# loop through each line
for line in lines:
    line = line.strip()
    print(line)


ins = JetPattern(lines[0])

for c in range(len(lines[0])*2):
    i = ins.getIns()


x = 7
y = 25
# setup the display, now we know how big we need it
scale = 20

board = Board(x, y, scale)

# test code
board.addRow()
board.asciiBoard()
# end test code

surface = pygame.display.set_mode((scale*x, scale*y))


surface.fill((0, 0, 0))

board.draw(surface)

for c in range(5):
    shape = Tetromino(getNextTetromino())
    shape.draw(surface, board.scale, 2, c*5)

pygame.display.flip()

for c in range(5):
    shape = Tetromino(getNextTetromino())
    cycles = 0

    while cycles < y:

        if shape.checkMove(2,cycles,board,Directions.DOWN)==Moves.COLLISION:
            print("bottom hit at cycles={}".format(cycles))
            break

        cycles += 1

        surface.fill((0, 0, 0))
        board.draw(surface)
        shape.draw(surface, board.scale, 2, cycles)
        pygame.display.flip()

        pygame.time.wait(200)

print("done")


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
