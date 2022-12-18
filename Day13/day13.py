# read file input.txt into an array of strings
# file1 = open('Day13/data/input_test.txt', 'r')
# file1 = open('Day13/data/input_test_ints_only.txt', 'r')
# file1 = open('Day13/data/input_test_short_rhs.txt', 'r')
# file1 = open('Day13/data/input_test_short_rhs2.txt', 'r')
# file1 = open('Day13/data/input_test_short_lhs.txt', 'r')
# file1 = open('Day13/data/input_test_complex.txt', 'r')
# file1 = open('Day13/data/input_test_4s.txt', 'r')
file1 = open('Day13/data/input.txt', 'r')

# 3114 is too low
# 5626 is too high
# max is 11325

Lines = file1.readlines()

left = []
right = []

print("### PARSING PROGRAM ###")
flip = False
# parse each line
for line in Lines:
    line = line.strip()
    if (len(line) > 0):
        print("exp:{}".format(line))
        if (flip == False):
            flip = True
            left.append(line)
        else:
            flip = False
            right.append(line)
print("### PARSING COMPLETE ###")


# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/13.py
def compare(p1,p2):
    if isinstance(p1, int) and isinstance(p2,int):
        if p1 < p2:
            return -1
        elif p1 == p2:
            return 0
        else:
            return 1
    elif isinstance(p1, list) and isinstance(p2, list):
        i = 0
        while i<len(p1) and i<len(p2):
            c = compare(p1[i], p2[i])
            if c==-1:
                return -1
            if c==1:
                return 1
            i += 1
        if i==len(p1) and i<len(p2):
            return -1
        elif i==len(p2) and i<len(p1):
            return 1
        else:
            return 0
    elif isinstance(p1, int) and isinstance(p2, list):
        return compare([p1], p2)
    else:
        return compare(p1, [p2])



indices = []
total = 0
print("sizes:{}/{}".format(len(left), len(right)))
for i in range(len(left)):
# for i in range(1):
    l = eval(left[i])
    r = eval(right[i])
    print("*** left:{}".format(l))
    print("    right:{}".format(r))

    result = compare(l, r)
    print("*** result:{}".format(result))
    print()

    if result == -1:
        indices.append(i+1)
        total += i+1

print("Pairs checked:{}".format(len(left)))
print(indices)
print(total)
