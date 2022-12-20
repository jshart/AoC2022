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
def impactedXValues(s, m, y):
    x1, y1 = s
    yOffset = abs(y1-y)
    xs = x1-(m-yOffset)
    xe = x1+(m-yOffset)
    return list(range(xs, xe+1))


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


cl = 2000000
coverage = set()
# check each sensor in turn, work out the area it can see, and then determine for the given value (cl)
# which X values are impacted (if any), append these to a set, so we can get a unique list of all impacted X values
# across the coverage line (cl) based on all the beacons overlapping fields of view
for c, v in enumerate(sensors):
    mRadius.append(mDist(v, beacons[c]))
    #print("{} sees {} at MDist {}".format(v, beacons[c], mRadius[c]), end='')

    if radiusOverlapsY(v, mRadius[c], cl):
        #print(" overlaps Y=10 ", end='')
        for x in impactedXValues(v, mRadius[c], cl):
            coverage.add(x)

        #print(impactedXValues(v, mRadius[c], cl))
    else:
        #print(" no overlap with Y=10")
        pass

#print("Coverage:", end='')
# print(coverage)
coverageLen = len(coverage)
# print(coverageLen)

# some of the values we can "see" are actually beacons and not empty spaces, given the beacon list
# is relatively small, its easier to simply check if an fall in the coverage line, and now reduce
# the count than try to take these into account above and complicate the area code
beaconsSeen = set()
# lets check how many beacons we have in this area;
for i in beacons:
    if i[1] == cl:
        if i[0] in coverage:
            beaconsSeen.add(i)

#print("Beacons:", end = '')
# print(beaconsSeen)
beaconsSeenLen = len(beaconsSeen)
# print(beaconsSeenLen)


finalAnswer = coverageLen-beaconsSeenLen
print("Final Answer:{}".format(finalAnswer))
