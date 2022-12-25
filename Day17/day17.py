# Init shape no# 2022
# *** Need to add lines: 1
# bottom hit at yOffset=3/3071 Y Watermark set:3 ANS:3068

# Importing the library
from enum import IntEnum
import pygame
from pygame.locals import *

# Overall dimensioning and limits - dial these based on display size etc
maxYDraw=50
x = 7
y = 40
scale = 20

#working numbers for part 1
# maxYDraw=200
# x = 7
# y = 180
# scale = 5

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
        #print("C:{},{}".format(newx,newy),end='')
        if newy>=self.height:
            #print(" Y out of range:{}".format(newy))
            return Moves.BOTTOM
        if newx<0 or newx >=self.width:
            #print(" X out of range:{}".format(newx))
            return Moves.IGNORE
        if self.board[newy][newx]>0:
            #print(" collision")
            return Moves.COLLISION

        #print(" in range")
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

        yLen=len(self.board)
        xLen=len(self.board[0])

        if yLen>maxYDraw:
            #print("Max Y Draw limited reached - clipping")
            yLen=maxYDraw

        for y in range(yLen):
            row=self.board[y]

            for x in range(xLen):
                cell=row[x]
                cellContent=tColors[cell]

                pygame.draw.rect(surface, cellContent, pygame.Rect(
                    x*self.scale, y*self.scale, self.scale, self.scale))
                pygame.draw.rect(surface, cellBorder, pygame.Rect(
                    x*self.scale, y*self.scale, self.scale, self.scale), width=1)
            
            # You can use `render` and then blit the text surface ...
            h=abs(y-len(self.board))-1
            text_surface = myFont.render(str(h), False, (255,255,255))
            surface.blit(text_surface,(0, y*self.scale))

    def addRow(self):
        self.board.insert(0, [0 for x in range(self.width)])

    def addRows(self,n):
        for i in range(n):
            self.board.insert(0, [0 for x in range(self.width)])

    def lockToBoard(self,xoffset,yoffset,shape):
        s=shape.getShape()

        for y, row in enumerate(s):
            for x, cell in enumerate(row):
                if cell!=0:
                    self.board[y+yoffset][x+xoffset]=int(shape.type)

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
    HLINE = 1
    CROSS = 2
    BL = 3
    VLINE = 4
    BOX = 5

tColors=[(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255)]

class Tetromino:

    # hLine = [1, 1, 1, 1] height == 1
    # cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]] height == 3
    # bL = [[0, 0, 1], [0, 0, 1], [1, 1, 1]] height == 3
    # vLine = [[1], [1], [1], [1]] height == 4
    # box = [[1, 1], [1, 1]] height == 2

    def __init__(self, type):
        self.type = type
        print("Creating shape:{} Height is:{}".format(type.name,self.getHeight()))

    def getHeight(self):
        return len(self.getShape())

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
        s = self.getShape()

        cellFilled = tColors[self.type]
        cellBorder = (125, 125, 125)

        for y, row in enumerate(s):
            for x, cell in enumerate(row):
                if cell == 0:
                    cellContent = (0, 0, 0)
                elif cell == 1:
                    cellContent = cellFilled
                # elif cell == 2:
                #     cellContent = cellFilled

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
                
                if cell!=0:
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

    return TType(t)


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
file1 = open('Day17/data/input.txt', 'r')

# read file input.txt into an array of strings
lines = file1.readlines()

# Create a list of the Jet stream directions, which we can
# retreive one at a time, and that resets to the beginning
# if we run out of items
ins = JetPattern(lines[0])

board = Board(x, y, scale)

# test code
board.addRow()
board.asciiBoard()
# end test code

# setup the display, now we know how big we need it
surface = pygame.display.set_mode((scale*x, scale*y))
surface.fill((0, 0, 0))
board.draw(surface)
pygame.display.flip()



# Start Y co-ord for first block will be maxY-3
# Subsequent startY will be highest_current_Y - 3
# highest_current_Y == top of new block unless that is < highest_current_Y
# if highest_current_Y + block_height is too high we need to add rows to the matrix
# NOTE - Y is lower the "higher" up the display we are - so much of the maths above
# is actually inverted in the real code.

yWatermark=y
maxShapes=0

while maxShapes<2022:
    for c in range(5):
        shape = Tetromino(getNextTetromino())
        maxShapes+=1
        print("Init shape no# {}".format(maxShapes))

        # work out the start position for the new shape, which is 3 above the
        # watermark (plus we need to leave space for the actual shape)
        yOffset = yWatermark-3-shape.getHeight()

        # if this puts us off-screen, we need to increase the size of the screen
        if (yOffset<0):
            linesToAdd=abs(yOffset)
            print("*** Need to add lines: {}".format(linesToAdd))
            board.addRows(linesToAdd)
            y=len(board.board)
            yOffset=0
            yWatermark+=linesToAdd

        xOffset = 2
        directionToggle = True

        while True:

            if directionToggle==True:
                # grab the next direction instruction from the input stream
                directionInstruction = ins.getIns()
                if directionInstruction == '>':
                    if shape.checkMove(xOffset,yOffset,board,Directions.RIGHT)!=Moves.IGNORE:
                        xOffset+=1
                else:
                    if shape.checkMove(xOffset,yOffset,board,Directions.LEFT)!=Moves.IGNORE:
                        xOffset-=1

                directionToggle=False
            else:
                if shape.checkMove(xOffset,yOffset,board,Directions.DOWN)==Moves.COLLISION:
                    print("bottom hit at yOffset={}/{}".format(yOffset,y-1), end='')
                    board.lockToBoard(xOffset,yOffset,shape)

                    if (yOffset<yWatermark):
                        yWatermark = yOffset
                    print(" Y Watermark set:{} ANS:{}".format(yWatermark,y-1-yWatermark))
                    break
                yOffset += 1
                directionToggle=True


            surface.fill((0, 0, 0))
            board.draw(surface)
            shape.draw(surface, board.scale, xOffset, yOffset)
            pygame.display.flip()

            #pygame.time.wait(200)

        if (maxShapes==2022):
            print("### MAX SHAPES == 2022 ###")
            break

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
