
# Importing the library
import pygame
from pygame.locals import *


def draw(scale, x, y, raw):

    s = set()

    # loop through each cell
    for colPos in range(y):
        for rowPos in range(x):
            # map the height to a green colour scale, unless its a negative number, which represent the start/end locations
            # which we map to red
            if raw[colPos][rowPos] < 0:
                color = (255, 0, 0)
            else:
                color = (0, (255/26)*(raw[colPos][rowPos]), 0)

            # just for debug purposes capture which Green values we generate
            s.add(255/raw[colPos][rowPos])
            # print(color)

            # draw the map
            pygame.draw.rect(surface, color, pygame.Rect(
                rowPos*scale, colPos*scale, scale, scale))

            # draw a rect to highlight the cells and make it a bit easier to see when there are blocks of same height
            pygame.draw.rect(surface, (10, 10, 10), pygame.Rect(
                rowPos*scale, colPos*scale, scale, scale), width=1)

            # Render the temporary surface, and then blit that onto the main surface
            text_surface = myFont.render(
                str(raw[colPos][rowPos]), False, (255, 0, 0))
            surface.blit(text_surface, (rowPos*scale, (colPos*scale)))

    # dump the green values, so we can check the heights look sane
    print(s)


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
for row in raw:
    print(row)

for colPos in range(y):
    print("L:[{}]  ".format(colPos), end='')
    for rowPos in range(x):
        print("{}|".format(raw[colPos][rowPos]), end='')
    print()

print("Grid is {},{}".format(x, y))



# setup the display, now we know how big we need it
scale = 10
surface = pygame.display.set_mode((scale*x, scale*y))

# draw the map in its current state
draw(scale, x, y, raw)

# flip the display for double buffering
pygame.display.flip()


# hold the screen open waiting on a user interaction so we can actually see it
pygame.event.clear()
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")
