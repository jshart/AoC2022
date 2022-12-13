
# Importing the library
import pygame
from pygame.locals import *



def draw(scale, x, y, raw):
    count = 0
    total = 0

    s=set()

    # loop through each cell
    for colPos in range(y):
        for rowPos in range(x):
            # map the height to a green colour scale - we add one as some squares have a tree height of "zero" which would result in a divide by zero error
            if raw[colPos][rowPos] <0:
                color = (255,0,0)
            else:
                color = (0, (255/26)*(raw[colPos][rowPos]), 0)

            s.add(255/raw[colPos][rowPos])
            #print(color)

            # draw the tree
            pygame.draw.rect(surface, color, pygame.Rect(
                rowPos*scale, colPos*scale, scale, scale))

            pygame.draw.rect(surface, (10, 10, 10), pygame.Rect(rowPos*scale, colPos*scale, scale, scale), width=1)

            # You can use `render` and then blit the text surface ...
            text_surface = myFont.render(str(raw[colPos][rowPos]), False, (255,0,0))
            surface.blit(text_surface,(rowPos*scale,(colPos*scale)))


    print(s)


# Initializing Pygame
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

for row in raw:
    print(row)

for colPos in range(y):
    print("L:[{}]  ".format(colPos), end='')
    for rowPos in range(x):
        print("{}|".format(raw[colPos][rowPos]), end='')
    print()

print("Grid is {},{}".format(x, y))


# setup the display
scale = 10
surface = pygame.display.set_mode((scale*x, scale*y))

draw(scale,x,y,raw)

# flip the display for double buffering
pygame.display.flip()


pygame.event.clear()
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")
