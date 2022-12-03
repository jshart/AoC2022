# open the file

f = open("Day2/data/input_test.txt", "r")

# read each line in the file

num=0
for line in f:
    # print the line
    print(line)

    # count the number of lines
    num += 1

    # print the num of lines
    print(num)

