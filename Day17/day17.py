
# Importing the library
from enum import Enum
import pygame
from pygame.locals import *


class JetPattern:
    def __init__(self, instructions):
        self.ins = instructions
        self.index = 0
        print("JetPattern initiatlised with length:{}".format(len(self.ins)))

    def getIns(self):
        i=self.ins[self.index]
        print("Ins [{}] at index:{}".format(i, self.index))
        
        self.index += 1
        if self.index >= len(self.ins):
            print("--> Instructions wrapping")
            self.index=0

        return i


class Tetromino:
    class TType(Enum):
        HLINE=0
        CROSS=1
        BL=2
        VLINE=3
        BOX=4

    # hLine = [1, 1, 1, 1]
    # cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    # bL = [[0, 0, 1], [0, 0, 1], [1, 1, 1]]
    # vLine = [[1], [1], [1], [1]]
    # box = [[1, 1], [1, 1]]

    def __init__(self, type):
        self.type=type

    def getShape(self):
        match self.type:
            case Tetromino.TType.HLINE:
                return [[1, 1, 1, 1]]
            case Tetromino.TType.CROSS:
                return [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
            case Tetromino.TType.BL:
                return [[0, 0, 1], [0, 0, 1], [1, 1, 1]]
            case Tetromino.TType.VLINE:
                return [[1], [1], [1], [1]]
            case Tetromino.TType.BOX:
                return [[1, 1], [1, 1]]

    def printShape(self):
        print(self.getShape())

    def printAsciiShape(self):
        s=self.getShape()
        y=len(s)
        x=len(s[0])
        for i in range(y):
            for j in range(x):
                if (s[i][j] == 1):
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def draw(self, scale):
        c=(255, 255, 0)
        # draw the sand
        pygame.draw.rect(surface, c, pygame.Rect(
            self.x*scale, self.y*scale, scale, scale))


def drawMap(scale, xmax, ymax, m):

    rockColor=(125, 125, 125)
    sandColor=(255, 255, 0)

    for x in range(xmax):
        for y in range(ymax):
            if (m[x][y] == 1):
                # draw the rock
                pygame.draw.rect(surface, rockColor, pygame.Rect(
                    x*scale, y*scale, scale, scale))
                pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(
                    x*scale, y*scale, scale, scale), width=1)
            elif (m[x][y] == 2):
                pygame.draw.rect(surface, sandColor, pygame.Rect(
                    x*scale, y*scale, scale, scale))


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont=pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
file1=open('Day17/data/input_test.txt', 'r')

# read file input.txt into an array of strings
lines=file1.readlines()

# loop through each line
for line in lines:
    line=line.strip()
    print(line)


x=600
y=200
map=[]

shape=Tetromino(Tetromino.TType.HLINE)
shape.printAsciiShape()
shape=Tetromino(Tetromino.TType.CROSS)
shape.printAsciiShape()
shape=Tetromino(Tetromino.TType.BL)
shape.printAsciiShape()
shape=Tetromino(Tetromino.TType.VLINE)
shape.printAsciiShape()
shape=Tetromino(Tetromino.TType.BOX)
shape.printAsciiShape()

ins=JetPattern(lines[0])

for c in range(len(lines[0])*2):
    i=ins.getIns()


# setup the display, now we know how big we need it
scale=3
surface=pygame.display.set_mode((scale*x, scale*y))


# surface.fill((0, 0, 0))

# drawMap(scale, x, y, map)
# pygame.display.flip()


pygame.event.clear()
while True:
    event=pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")
