
# Importing the library
import pygame
import numpy


class VisTree:
    def __init__(self, height):
        self.h = height
        # until we know better assume the tree is visible from all directions
        self.n = True
        self.s = True
        self.e = True
        self.w = True


# Initializing Pygame
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 8)


#### START OF DATA LOADING ####

# read file input.txt into an array of strings
file1 = open('Day8/data/input.txt', 'r')
Lines = file1.readlines()

raw = []

# loop through each line
for line in Lines:
    # break up each line into an array of characters
    raw.append(list(map(int, line.strip())))


x = len(raw[0])
y = len(raw)

print("Grid is {},{}".format(x, y))

# replace the list content with a class object so we can also track the  tree visibility
for i in range(x):
    for j in range(y):
        raw[i][j] = VisTree(raw[i][j])


# just dump out the raw numbers so we can be sure the data loaded ok
for i in range(x):
    for j in range(y):
        print(raw[i][j].h, end='')
    print()

#### END OF DATA LOADING ####


def draw(scale, x, y, raw):
    count = 0

    # loop through each cell
    for i in range(x):
        for j in range(y):
            # map the height to a green colour scale - we add one as some squares have a tree height of "zero" which would result in a divide by zero error
            color = (0, 255/(raw[i][j].h+1), 0)

            # draw the tree
            pygame.draw.rect(surface, color, pygame.Rect(
                i*scale, j*scale, scale, scale))
            # border - maybe needed for debugging
            #pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(i*scale, j*scale, scale, scale), width=1)

            # if (raw[i][j].n==False):
            #     pygame.draw.line(surface, (255,0,0), pygame.Vector2(i*scale,j*scale), pygame.Vector2((i*scale)+scale,j*scale))
            #     pass

            # if (raw[i][j].s==False):
            #     pygame.draw.line(surface, (0,0,255), pygame.Vector2((i*scale),(j*scale)+scale-1), pygame.Vector2((i*scale)+scale-1,(j*scale)+scale-1))

            # if (raw[i][j].w==False):
            #     pygame.draw.line(surface, (255,0,0), pygame.Vector2(i*scale,j*scale), pygame.Vector2(i*scale,(j*scale)+scale))
            #     pass

            # if (raw[i][j].e==False):
            #     pygame.draw.line(surface, (0,0,255), pygame.Vector2((i*scale)+scale-1,j*scale), pygame.Vector2((i*scale)+scale-1,(j*scale)+scale-1))

            if (raw[i][j].n==False and raw[i][j].s==False and raw[i][j].w==False and raw[i][j].e==False):
                pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(i*scale, j*scale, scale, scale), width=1)
                #print(raw[i][j].h)
                count+=1

            # You can use `render` and then blit the text surface ...
            text_surface = myFont.render(str(raw[i][j].h), False, (255,255,255))
            surface.blit(text_surface,(i*scale,(j*scale)))

    return count



# setup the display
scale = 10
surface = pygame.display.set_mode((scale*x, scale*y))

# Check each directon in turn, N, S, W, E
# Create a mask to track the first occurance of a tree of a given height
#      0  1  2  3  4  5  6  7  8  9
mask = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
# Once we find a tree of a given height, we can mark it in the mask, any tree lower than
# that height we can then mark as no longer visible

# Check from the North (i.e. top)
# Loop across each column
for i in range(x):

    # reset the mask
    for m in range(len(mask)):
        mask[m]=-1

    # go down each row of this column
    for j in range(y):
        for m in range(raw[i][j].h, 10):
            # if any tree has already been found at this height or higher then we know this tree is invisible
            if mask[m]>=0:
                # a tree of this height or higher has been found, so we know we can now mark this tree as invisible
                # in this direction
                raw[i][j].n=False

        # check to see if this is the first time we found a tree if this height
        if mask[raw[i][j].h]==-1:
            mask[raw[i][j].h]=j

# Check from the South (i.e. bottom)
# Loop across each column
for i in range(x):

    # reset the mask
    for m in range(len(mask)):
        mask[m]=-1

    # go up each row of this column
    for j in range(y-1,-1,-1):
        for m in range(raw[i][j].h, 10):
            # if any tree has already been found at this height or higher then we know this tree is invisible
            if mask[m]>=0:
                # a tree of this height or higher has been found, so we know we can now mark this tree as invisible
                # in this direction
                raw[i][j].s=False

        # check to see if this is the first time we found a tree if this height
        if mask[raw[i][j].h]==-1:
            mask[raw[i][j].h]=j


# Check from the West (i.e. left)
# Loop through each row
for j in range(y):

    # reset the mask
    for m in range(len(mask)):
        mask[m]=-1

    # go down across each column in this row
    for i in range(x):
        for m in range(raw[i][j].h, 10):
            # if any tree has already been found at this height or higher then we know this tree is invisible
            if mask[m]>=0:
                # a tree of this height or higher has been found, so we know we can now mark this tree as invisible
                # in this direction
                raw[i][j].w=False

        # check to see if this is the first time we found a tree if this height
        if mask[raw[i][j].h]==-1:
            mask[raw[i][j].h]=j

# Check from the East (i.e. right)
# Loop through each row
for j in range(y):

    # reset the mask
    for m in range(len(mask)):
        mask[m]=-1

    # go down across each column in this row
    for i in range(x-1,-1,-1):
        for m in range(raw[i][j].h, 10):
            # if any tree has already been found at this height or higher then we know this tree is invisible
            if mask[m]>=0:
                # a tree of this height or higher has been found, so we know we can now mark this tree as invisible
                # in this direction
                raw[i][j].e=False

        # check to see if this is the first time we found a tree if this height
        if mask[raw[i][j].h]==-1:
            mask[raw[i][j].h]=j




# draw the current state
total=x*y
invisible=draw(scale, x, y, raw)
visible = (x*y)-invisible

# flip the display for double buffering
pygame.display.flip()


#print("n:{} s:{} w:{} e:{}".format(raw[3][3].n,raw[i][j].s,raw[i][j].w,raw[i][j].e))

print("X/Y {},{}".format(x,y))
print("Total:{} Vis:{} In:{}".format(total,visible,invisible))

# just pause the program and prevent exiting (so we can see the display)
a = input()
