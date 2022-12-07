
import math

ds = "bvwbjplbgvbhsrlpgdmjqwftvncz"
ds = "nppdvjthqldpwncqszvftbrmjlhg"
ds = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
ds = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"


# open and read the header file
file1 = open('Day6/data/input.txt', 'r')
ds = file1.read()

print(ds)
print(len(ds))

# loop through the characters in ds

for i in range(len(ds)-13):
    # create a substring of the string ds 4 characters long
    sub = ds[i:i+14]

    if (len(sub) == len(set(sub))):
        print("[{}] i=={}".format(sub, i+14))
        break
    else:
        print(".",end="")
