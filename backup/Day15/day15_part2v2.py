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
    return (xs, xe)


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


def compressRanges(r):
    start = 0
    end = 1

    notFinished = True
    while notFinished == True:

        notFinished = False
        # remove completely overlapped ranges...
        tr = r.copy()
        for i in r:
            for c in r:
                if i != c:
                    # if the range is within the compressed range, remove the range from the list
                    if i[start] >= c[start] and i[end] <= c[end]:
                        if i in tr:
                            tr.remove(i)
                            notFinished = True

        # Now lets do a 2nd pass looking for overlapping ranges
        for i in r:
            for c in r:

                # print("   comparing i{} with c{}".format(i, c))
                merged = False

                # if these are not the exact same 2 elements that we're comparing
                if i != c:
                    # lets check if the ranges overlap
                    # first of all, are the 2 ranges concurrent
                    if i[end]+1 == c[start]:
                        tr.append((i[start], c[end]))
                        merged = True
                    elif c[end]+1 == i[start]:
                        tr.append((c[start], i[end]))
                        merged = True
                        # if the start of 'i' range is inside the 'c' range
                    elif i[start] >= c[start] and i[start] <= c[end]:
                        # create a new combined range and add it to the list
                        tr.append((c[start], i[end]))
                        merged = True
                        # else if the end of the 'i' range is inside the 'c' range
                    elif i[end] <= c[end] and i[end] >= c[start]:
                        # create a new combined range and add it to the list
                        tr.append((i[start], c[end]))
                        merged = True

                if merged:
                    notFinished = True

                    # remove any of the old ranges we now do not need
                    if i in tr:
                        tr.remove(i)
                    if c in tr:
                        tr.remove(c)

                break

        # reset r to the latest comoressed range
        r = tr.copy()

    return tr


#### START OF DATA LOADING ####
file1 = open('Day15/data/input_test.txt', 'r')
#file1 = open('Day15/data/input.txt', 'r')


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


#max = 4000000
max = 20


for cl in range(max):
    # print(cl, end='')

    coverage = []
    for c, v in enumerate(sensors):
        if radiusOverlapsY(v, mRadius[c], cl):
            coverage.append(impactedXValues(v, mRadius[c], cl, max))

    # print(coverage)
    cr = compressRanges(coverage)

    if (len(cr) > 1):
        print("Line:{} R:{}".format(cl, cr))

    if cl % 1000 == 0:
        print("HB:{}".format(cl))

        # print(cr)
        # print()

        # coverageLen = len(coverage)
        # # print(coverageLen)

        # lineAnswer = coverageLen
        # if lineAnswer < max+1:
        #     print("WINNA!", end='')
        #     print("Line {} Answer:{} ".format(cl, lineAnswer))
        #     # print(coverage)

        #     me = checkMissingElement(coverage, max)
        #     print("Missing Element:{}".format(me))
        #     answer = (me*4000000)+cl
        #     print("Final Answer:{}".format(answer))
        #     # exit()
        # else:
        #     #print("Line {} Answer:{} ".format(cl, lineAnswer), end = '')
        #     # print(coverage)
        #     pass
