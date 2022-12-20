# for each sensor/beacon pair:
# 1) calculate the Man-dist for sensor/beacon pair - call it M
# 2) any sensor within distant M of target row Y can block some cells
# 3) based on distance calculate impacted X values (impacted X values inversely proportional to Y distance)
# 4) add impacted values to a *set*
# 5) if either the sensor or beacon sit on the line also add them to the set
# count elements in set
# m-dist dealing with negatives - the distance is the ABS() of the X delta + the ABS() of the Y delta


# used for parsing the raw data from the input file, this just splits the pairs into ints
def getCoords(s):
    parts = s.split(',')
    return (int(parts[0]), int(parts[1]))


# given a sensor and a beacon work out the manhattan distance between them
def mDist(s, b):
    x1, y1 = s
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


# for a given sensor and the manhatten distance calculated based on the beacon it can detect
# work out an area it can see and then determine if a given Y value is in that area
def radiusOverlapsY(s, m, y):
    x1, y1 = s
    ys = y-m
    ye = y+m
    return ys <= y1 <= ye


# for a given sensor and the manhatten distance calculated based on the beacon it can detect
# work out the range of X values at a given Y value in that area and return them
def impactedXValues(s, m, y, max):
    x1, y1 = s
    yOffset = abs(y1-y)
    xs = x1-(m-yOffset)
    xs = limitRange(xs, 0, max)
    xe = x1+(m-yOffset)
    xe = limitRange(xe, 0, max)
    return set(range(xs, xe+1))


def limitRange(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x


def checkMissingElement(s, v):
    for i in range(v+1):
        if i not in s:
            return i


#### START OF DATA LOADING ####
file1 = open('Day15/data/input.txt', 'r')

# read file input.txt into an array of strings
Lines = file1.readlines()

sensors = []
beacons = []
mRadius = []

# loop through each line
for line in Lines:
    line = line.strip()
    parts = line.split(':')
    sensor = parts[0]
    beacon = parts[1]
    sensors.append(getCoords(sensor))
    beacons.append(getCoords(beacon))

print("SENSORS:", end='')
print(sensors)
print("BEACONS:", end='')
print(beacons)
#### DATA LOAD COMPLETE ####


# build the manhattan distances as they are constant;
for c, v in enumerate(sensors):
    mRadius.append(mDist(v, beacons[c]))
    # print("{} sees {} at MDist {}".format(v, beacons[c], mRadius[c]), end='')


max = 4000000

for cl in range(max):
    print(cl)

    coverage = set()
    for c, v in enumerate(sensors):
        if radiusOverlapsY(v, mRadius[c], cl):
            coverage.update(impactedXValues(v, mRadius[c], cl, max))

    coverageLen = len(coverage)
    # print(coverageLen)

    lineAnswer = coverageLen
    if lineAnswer < max+1:
        print("WINNA!", end='')
        print("Line {} Answer:{} ".format(cl, lineAnswer))
        # print(coverage)

        me = checkMissingElement(coverage, max)
        print("Missing Element:{}".format(me))
        answer = (me*4000000)+cl
        print("Final Answer:{}".format(answer))
        # exit()
    else:
        #print("Line {} Answer:{} ".format(cl, lineAnswer), end = '')
        # print(coverage)
        pass

