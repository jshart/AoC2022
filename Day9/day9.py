
# Importing the library
import pygame
import numpy


class Rope:
    def __init__(self, h, t):
        self.head = h
        self.tailSegment = t
        self.history = []
        self.history.append(self.tailSegment.copy())

    def draw(self, screen, scale):
        offset = scale/4

        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
            self.head[0]*scale, self.head[1]*scale, scale, scale))

        pygame.draw.rect(screen, (0, 125, 0), pygame.Rect(
            self.tailSegment[0]*scale, self.tailSegment[1]*scale, scale, scale))

        for h in self.history:
            #pygame.draw.rect(screen, (100, 0, 0), pygame.Rect((h[0]*scale)+offset, (h[1]*scale)+offset, offset*2, offset*2))
            pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(
                (h[0]*scale), (h[1]*scale), scale, scale))

    def moveHead(self, dx, dy):
        self.head[0] += dx
        self.head[1] += dy

    def moveTail(self):

        xdelta = self.head[0] - self.tailSegment[0]
        ydelta = self.head[1] - self.tailSegment[1]
        #print("dX/Y {},{}".format(xdelta, ydelta))
        moved = False

        # if xdelta is greater than 1, then move the tail towards the head
        if xdelta > 1 or xdelta < -1:
            moved = True
            # need to move the tail towards the head in the X direction
            if xdelta > 0:
                self.tailSegment[0] += 1
                if ydelta > 0:
                    self.tailSegment[1] += 1
                elif ydelta < 0:
                    self.tailSegment[1] -= 1
            else:
                self.tailSegment[0] -= 1
                if ydelta > 0:
                    self.tailSegment[1] += 1
                elif ydelta < 0:
                    self.tailSegment[1] -= 1

        if ydelta > 1 or ydelta < -1:
            moved = True
            # need to move the tail towards the head in the X direction
            if ydelta > 0:
                self.tailSegment[1] += 1
                if xdelta > 0:
                    self.tailSegment[0] += 1
                elif xdelta < 0:
                    self.tailSegment[0] -= 1
            else:
                self.tailSegment[1] -= 1
                if xdelta > 0:
                    self.tailSegment[0] += 1
                elif xdelta < 0:
                    self.tailSegment[0] -= 1

        if moved == True:
            self.history.append(self.tailSegment.copy())


# Initializing Pygame
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 8)


#### START OF DATA LOADING ####

# read file input.txt into an array of strings
file1 = open('Day9/data/input.txt', 'r')
Lines = file1.readlines()

raw = []
instruction = []

# loop through each line
for line in Lines:
    # break up each line into instruction components
    line = line.strip()
    instruction = line.split(' ')
    raw.append(instruction)
    print(instruction)

r = Rope([0, 5], [0, 5])


def draw(surface, scale, maxx, maxy, raw):

    for x in range(0, maxx, scale):
        for y in range(0, maxy, scale):
            pygame.draw.rect(surface, (100, 100, 100),
                             pygame.Rect(x, y, scale, scale), width=1)

    # You can use `render` and then blit the text surface ...
    # text_surface = myFont.render(str(raw[i][j].h), False, (255, 255, 255))
    # surface.blit(text_surface, (i*scale, (j*scale)))


maxx = 1000
maxy = 1000
scale = 4
surface = pygame.display.set_mode((maxx, maxy))

#pygame.time.wait(5000)

count=0
# run through each instruction
for ins in raw:

    print("{} Executing Instruction: {}".format(count,ins))

    # move the head based on the instruction
    for j in range(int(ins[1])):
        if ins[0] == 'U':
            r.moveHead(0, -1)
        if ins[0] == 'D':
            r.moveHead(0, 1)
        if ins[0] == 'L':
            r.moveHead(-1, 0)
        if ins[0] == 'R':
            r.moveHead(1, 0)

        r.moveTail()

        surface.fill((0, 0, 0))
        draw(surface, scale, maxx, maxy, raw)
        # flip the display for double buffering
        pygame.display.flip()

        r.draw(surface, scale)

        # flip the display for double buffering
        pygame.display.flip()

        # pause for a short while
        #pygame.time.wait(100)

        count+=1

ch = set()
# compress the history list into a set for counting
for h in r.history:
    ch.add((h[0], h[1]))

print(ch)
print("len:{}".format(len(ch)))

a=input()
