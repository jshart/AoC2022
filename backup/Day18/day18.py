# read file input.txt into an array of strings
file1 = open('Day18/data/input_test.txt', 'r')
lines = file1.readlines()


print("### PARSING PROGRAM ###")
raw = []
maxx = 0
maxy = 0
maxz = 0
coordsList = []
# parse each line
for line in lines:
    line = line.strip()
    coords = list(map(int, line.split(",")))
    print(coords)
    if (coords[0] > maxx):
        maxx = coords[0]
    if (coords[1] > maxy):
        maxy = coords[1]
    if (coords[2] > maxz):
        maxz = coords[2]

    coordsList.append(coords)

maxx += 1
maxy += 1
maxz += 1
print("maxx:", maxx)
print("maxy:", maxy)
print("maxz:", maxz)

# create a 3 dimensional array sized maxx,maxy,maxz
space = [[['.' for z in range(maxz)] for y in range(maxy)]
         for x in range(maxx)]
print("L1:{}".format(len(space)))
print("L2:{}".format(len(space[0])))
print("L3:{}".format(len(space[0][0])))

for c in coordsList:
    space[c[0]][c[1]][c[2]] = '#'

for x in range(maxx):
    for y in range(maxy):
        for z in range(maxz):
            print(space[x][y][z], end='')
        print()
    print()

count = 0
hidden = 0
for x in range(maxx):
    for y in range(maxy):
        for z in range(maxz):
            if space[x][y][z] == '#':
                if x > 0:
                    if space[x-1][y][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After +x:{} {}".format(count, hidden))
for x in range(maxx):
    for y in range(maxy):
        for z in range(maxz):
            if space[x][y][z] == '#':
                if y > 0:
                    if space[x][y-1][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After +y:{} {}".format(count, hidden))
for x in range(maxx):
    for y in range(maxy):
        for z in range(maxz):
            if space[x][y][z] == '#':
                if z > 0:
                    if space[x][y][z-1] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After +z:{} {}".format(count, hidden))

for x in range(maxx-1,0,-1):
    for y in range(maxy):
        for z in range(maxz):
            if space[x][y][z] == '#':
                if x < maxx-1:
                    if space[x+1][y][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After -x:{} {}".format(count, hidden))
for x in range(maxx):
    for y in range(maxy-1,0,-1):
        for z in range(maxz):
            if space[x][y][z] == '#':
                if y < maxy-1:
                    if space[x][y+1][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After -y:{} {}".format(count, hidden))
for x in range(maxx):
    for y in range(maxy):
        for z in range(maxz-1,0,-1):
            if space[x][y][z] == '#':
                if z < maxz-1:
                    if space[x][y][z+1] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After -z:{} {}".format(count, hidden))