# read file input.txt into an array of strings
file1 = open('Day10/data/input.txt', 'r')
Lines = file1.readlines()

# create a dictionary to track the number of operations for a command
cycles = {
    'noop': 1,
    'addx': 2}

checkCycles = [20, 60, 100, 140, 180, 220]

results = []

X = 1
cycleCount = 0
pc = 0

parsed = []

print("### PARSING PROGRAM ###")
# parse each line
for line in Lines:
    line = line.strip()
    parts = line.split(' ')

    if (len(parts) > 1):
        print("[{}][{}]".format(parts[0], parts[1]))
    else:
        print(parts[0])

    parsed.append(parts)

print("### STARTING PROGRAM LEN={} ###".format(len(parsed)))
print(parsed)

process = []

hpos = 0
xvalues = []

while True:
    p = parsed[pc]

    for i in range(cycles[p[0]]):


        # sprite is "3" wide, so we need to check if the register position over
        # laps any of the 3 sprite positions
        if hpos == X-1 or hpos == X or hpos == X+1:
            print("#", end='')
        else:
            print(" ", end='')

        cycleCount += 1

        hpos = cycleCount % 40

        if hpos == 0:
            print("| C:{}".format(cycleCount), end='')
            print(xvalues)
            xvalues.clear()

    if p[0] == "addx":
        X += int(p[1])
        xvalues.append(X)

    if cycleCount > 300:
        break

    if pc == len(parsed)-1:
        pc = 0
    else:
        pc += 1

print(results)
print("Total:{}".format(sum(results)))
