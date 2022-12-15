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


# This function can be called recusively to;
# 1. check if both parameters are lists
# 2. if either is an int, convert it to a list
# compare an element from list one with element from list two
# if the first int is higher than the second end. (LEFT SIDE SHOULD BE LOWER)
# if both elements are lists, call this function again
# with the element from list one and the element from list two

def compare(l, r):
    j = 0
    print("   Range:{}".format(len(l)))
    for j in range(len(l)):

        print("   Checking left index:{} value:{}".format(j, l[j]))
        # if we've run out of elements on the right then these
        # are not in order
        if (j >= len(r)):
            print("   right ran out of elements - FAILED")
            return False

        le = l[j]
        re = r[j]
        print("   comparing {} with {}".format(le, re))

        if (isinstance(le, int) == True and isinstance(re, int) == True):
            print("   both are ints")

            # both are ints, so do a straight compare
            if le > re:
                print("   left is higer - FAILED")
                return False
            elif le < re:
                print("   left is lower - PASSED")
                return True
            else:
                # if they're equal, we just continue
                print("   left/right equal - CONTINING")
        else:
            # At least one of these elements is a list, so we need
            # to normalise them both to lists (if one is an int)
            # and then recursively call this function
            if isinstance(le, int) == True:
                # need to convert le to a list
                le = [le]

            if isinstance(re, int) == True:
                # need to convert re to a list
                re = [re]

            # now we can compare
            result = compare(le, re)

            return result
        print("   looping")

    print("   Consumed all of Left - PASSED")
    return True


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

    if result == True:
        indices.append(i+1)
        total += i+1

print("Pairs checked:{}".format(len(left)))
print(indices)
print(total)
