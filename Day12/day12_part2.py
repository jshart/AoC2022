
# Importing the library
import pygame
from pygame.locals import *


def drawCameFrom(scale, cameFrom, x, y):
    color = (200, 200, 200)
    offset = scale/4

    # loop through each cell
    for colPos in range(y):
        for rowPos in range(x):
            if (rowPos, colPos) in cameFrom:
                # pygame.draw.rect(surface, color, pygame.Rect((colPos*scale)+offset, (rowPos*scale)+offset, scale-offset, scale-offset))

                f = cameFrom.get((rowPos, colPos))

                if f != None:
                    pygame.draw.circle(
                        surface, color, ((f[0]*scale), (f[1]*scale)+scale/2), scale/4)
                    pygame.draw.line(surface, color, ((
                        rowPos*scale)+scale/2, (colPos*scale)+scale/2), ((f[0]*scale)+scale/2, (f[1]*scale)+scale/2))


def drawReached(scale, reached):
    color = (125, 125, 125)
    for r in reached:
        pygame.draw.rect(
            surface, color, (r[0]*scale, r[1]*scale, scale, scale))


def drawFrontier(scale, frontier):
    color = (255, 255, 0)
    for f in frontier:
        pygame.draw.rect(
            surface, color, (f[0]*scale, f[1]*scale, scale, scale))


def drawStart(scale, x, y):
    color = (255, 0, 0)
    pygame.draw.rect(surface, color, pygame.Rect(
        x*scale, y*scale, scale, scale))


def drawEnd(scale, x, y):
    color = (0, 0, 255)
    pygame.draw.rect(surface, color, pygame.Rect(
        x*scale, y*scale, scale, scale))


def drawMap(scale, x, y, raw):
    s = set()

    # loop through each cell
    for colPos in range(y):
        for rowPos in range(x):
            # map the height to a green colour scale,

            color = (0, (255/26)*(raw[colPos][rowPos]), 0)

            # just for debug purposes capture which Green values we generate
            s.add(255/raw[colPos][rowPos])

            # draw the map
            pygame.draw.rect(surface, color, pygame.Rect(
                rowPos*scale, colPos*scale, scale, scale))

            # draw a rect to highlight the cells and make it a bit easier to see when there are blocks of same height
            pygame.draw.rect(surface, (10, 10, 10), pygame.Rect(
                rowPos*scale, colPos*scale, scale, scale), width=1)

            # Render the temporary surface, and then blit that onto the main surface
            text_surface = myFont.render(
                str(raw[colPos][rowPos]), False, (255, 255, 255))
            surface.blit(text_surface, (rowPos*scale, (colPos*scale)))


def validHeightChange(h1, h2):
    # print("h1:h2 {}:{}".format(h1, h2))
    if h1 - h2 > 1:
        return False

    return True


def getValidNeighbours(raw, x, y):
    # get the neighbours of a cell
    # print("Checking Neighbours for {},{}".format(x, y))
    neighbours = []
    h1 = raw[y][x]
    # check the cell above
    if y > 0:
        h2 = raw[y-1][x]
        if validHeightChange(h1, h2):
            neighbours.append([x, y-1])
    # check the cell below
    if y < len(raw)-1:
        h2 = raw[y+1][x]
        if validHeightChange(h1, h2):
            neighbours.append([x, y+1])
    # check the cell to the left
    if x > 0:
        h2 = raw[y][x-1]
        if validHeightChange(h1, h2):
            neighbours.append([x-1, y])
    # check the cell to the right
    if x < len(raw[y])-1:
        h2 = raw[y][x+1]
        if validHeightChange(h1, h2):
            neighbours.append([x+1, y])

    return neighbours


def sortKey(e):
    #print(raw[e[0]][e[1]])
    return (raw[e[1]][e[0]])


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
file1 = open('Day12/data/input.txt', 'r')

# read file input.txt into an array of strings
Lines = file1.readlines()

raw = []

temp = []
# loop through each line
for line in Lines:
    temp.clear()
    line = line.strip()
    # break up each line into an array of characters
    for c in line:
        # makes 'a' == 1 - note S/E will go negative - but this is intentional as allows us an easy way to spot them
        temp.append(ord(c)-96)
    raw.append(temp.copy())


x = len(raw[0])
y = len(raw)

print("Matrix size:{}/{}".format(x, y))

#### END OF DATA LOADING ####


# just dump the data we loaded, so we get a chance to visually check it looks ok
# also use this pass to capture the co-ords for the start/end points
for row in raw:
    print(row)

for colPos in range(y):
    print("L:[{}]  ".format(colPos), end='')
    for rowPos in range(x):
        print("{}|".format(raw[colPos][rowPos]), end='')

        if (raw[colPos][rowPos] == -13):
            start_x = rowPos
            start_y = colPos

            # now we know the start, we can reset the height
            raw[colPos][rowPos] = 1

        if (raw[colPos][rowPos] == -27):
            print("E", end='')
            end_x = rowPos
            end_y = colPos

            # now we know the start, we can reset the height
            raw[colPos][rowPos] = 26

    print()

print("Grid is {},{}".format(x, y))
print("S={},{}".format(start_x, start_y))
print(getValidNeighbours(raw, start_x, start_y))
print("E={},{}".format(end_x, end_y))
print(getValidNeighbours(raw, end_x, end_y))
# 83 69
print("{} {}".format(ord('S')-96, ord('E')-96))

# setup the display, now we know how big we need it
scale = 12
surface = pygame.display.set_mode((scale*x, scale*y))


frontier = []
frontier.append([end_x, end_y])

reached = set()
reached.add((end_x, end_y))

came_from = dict()
came_from[(end_x, end_y)] = None

found = False

loop = 0
while len(frontier) > 0 and found == False and loop < 10000:

    loop += 1
    current = frontier.pop(0)

    if raw[current[1]][current[0]]==1:
        print("'a' Found")
        found = True
    else:
        print(raw[current[1]][current[0]])

    for e in getValidNeighbours(raw, current[0], current[1]):
        if (e[0], e[1]) not in came_from:
            frontier.append(e)
            came_from[(e[0], e[1])] = current
            reached.add((e[0], e[1]))

    # draw the map in its current state
    drawMap(scale, x, y, raw)
    drawStart(scale, start_x, start_y)
    drawEnd(scale, end_x, end_y)
    drawReached(scale, reached)
    drawFrontier(scale, frontier)
    drawCameFrom(scale, came_from, x, y)

    # flip the display for double buffering
    pygame.display.flip()

    #frontier.sort(key=sortKey)
    #print(frontier)

    #a=input()


# for c in came_from:
#     print(c)

drawMap(scale, x, y, raw)

#current=came_from.get((end_x, end_y))
color=(0, 255, 255)
count=0
while (current != None):
    pygame.draw.rect(
        surface, color, (current[0]*scale, current[1]*scale, scale, scale))
    print(current)

    # Render the temporary surface, and then blit that onto the main surface
    text_surface = myFont.render(
        str(raw[current[1]][current[0]]), False, (255, 0, 0))
    surface.blit(text_surface, (current[0]*scale, (current[1]*scale)))


    current=came_from.get((current[0], current[1]))
    count += 1

print("Count:{}".format(count))

# flip the display for double buffering
pygame.display.flip()

pygame.event.clear()
while True:
    event=pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")
