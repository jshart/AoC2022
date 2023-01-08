class VoxelLoader:
    def __init__(self, fileName):
        self.fileName=fileName
        self.file1=None
        self.lines=None
        self.raw = []
        self.maxx = 0
        self.maxy = 0
        self.maxz = 0
        self.coordsList = []
        self.space=None

    def loadFile(self):
        # read file input.txt into an array of strings
        self.file1 = open(self.fileName, 'r')
        self.lines = self.file1.readlines()


    def parseFile(self):
        print("### PARSING PROGRAM ###")

        # parse each line
        for line in self.lines:
            line = line.strip()
            self.coords = list(map(int, line.split(",")))
            print(self.coords)
            if (self.coords[0] > self.maxx):
                self.maxx = self.coords[0]
            if (self.coords[1] > self.maxy):
                self.maxy = self.coords[1]
            if (self.coords[2] > self.maxz):
                self.maxz = self.coords[2]

            self.coordsList.append(self.coords)

        self.maxx += 1
        self.maxy += 1
        self.maxz += 1
        print("maxx:", self.maxx)
        print("maxy:", self.maxy)
        print("maxz:", self.maxz)

        # create a 3 dimensional array sized maxx,maxy,maxz
        self.space = [[['.' for z in range(self.maxz)] for y in range(self.maxy)]
                for x in range(self.maxx)]
        print("L1:{}".format(len(self.space)))
        print("L2:{}".format(len(self.space[0])))
        print("L3:{}".format(len(self.space[0][0])))

        for c in self.coordsList:
            self.space[c[0]][c[1]][c[2]] = '#'

    def printVoxels(self):
        for x in range(self.maxx):
            for y in range(self.maxy):
                for z in range(self.maxz):
                    print(self.space[x][y][z], end='')
                print()
            print()


if __name__ == "__main__":
    print("File executed directly")

v = VoxelLoader('Day18/data/input_test.txt')
v.loadFile()
v.parseFile()
v.printVoxels()

count = 0
hidden = 0
for x in range(v.maxx):
    for y in range(v.maxy):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                if x > 0:
                    if v.space[x-1][y][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After +x:{} {}".format(count, hidden))
for x in range(v.maxx):
    for y in range(v.maxy):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                if y > 0:
                    if v.space[x][y-1][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After +y:{} {}".format(count, hidden))
for x in range(v.maxx):
    for y in range(v.maxy):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                if z > 0:
                    if v.space[x][y][z-1] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After +z:{} {}".format(count, hidden))

for x in range(v.maxx-1,0,-1):
    for y in range(v.maxy):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                if x < v.maxx-1:
                    if v.space[x+1][y][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After -x:{} {}".format(count, hidden))
for x in range(v.maxx):
    for y in range(v.maxy-1,0,-1):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                if y < v.maxy-1:
                    if v.space[x][y+1][z] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After -y:{} {}".format(count, hidden))
for x in range(v.maxx):
    for y in range(v.maxy):
        for z in range(v.maxz-1,0,-1):
            if v.space[x][y][z] == '#':
                if z < v.maxz-1:
                    if v.space[x][y][z+1] == '#':
                        hidden += 1
                    else:
                        count += 1
                else:
                    count += 1
print("After -z:{} {}".format(count, hidden))
