# home grown tree example
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.directories = []
        self.dirSize = []
        self.files = []
        self.fileSize = []
        self.parent = None

    def add_directory(self, directory):
        temp = TreeNode(directory)
        temp.parent = self

        self.directories.append(temp)
        self.dirSize.append(0)

    def add_file(self, file, size):
        temp = TreeNode(file)
        temp.parent = self

        self.files.append(temp)
        self.fileSize.append(size)

    def search_file(self, file_name):
        # search the files in the current directory
        for file in self.files:
            if file.name == file_name:
                print(f"Found file {file_name} in directory {self.name}")

        # search the files in the sub-directories
        for directory in self.directories:
            directory.search_file(file_name)

    def print_tree(self, depth):

        print("["+ self.name + "]")
        for i in range(len(self.directories)):
            print("|"*depth, end='\_ ')
            print(
                f"{self.name} -> {self.directories[i].name} {self.dirSize[i]}")
            self.directories[i].print_tree(depth+1)

        for i in range(len(self.files)):
            print("|"*depth, end='\_')
            print(f"{self.files[i].name} {self.fileSize[i]}")

    def update_dir_size(self):
        newTotal = 0

        # get update from all sub-directories
        for i in range(len(self.directories)):
            self.dirSize[i] += self.directories[i].update_dir_size()
            newTotal += self.dirSize[i]

        # add on all the file sizes in the current directory
        for i in range(len(self.files)):
            newTotal += int(self.fileSize[i])

        return (newTotal)

    def check_for_size(self, minSize):

        totalDirSize = 0

        # check each directory to see if its less than or equal to the maxSize
        for i in range(len(self.directories)):
            totalDirSize += self.directories[i].check_for_size(minSize)

            if int(self.dirSize[i]) >= minSize:
                print(f"{self.directories[i].name} {self.dirSize[i]}")
                totalDirSize += (int(self.dirSize[i]))
            else:
                #print(f"{self.directories[i].name} {self.dirSize[i]} < {minSize}")
                pass

        return totalDirSize


# create a root directory
root = TreeNode("root")
pwd = root

# read file input.txt into an array of strings
file1 = open('Day7/data/input.txt', 'r')
Lines = file1.readlines()

# parse each line

for line in Lines:
    line = line.strip()
    parts = line.split(' ')

    # if its a directory
    if parts[0] == 'dir':
        pwd.add_directory(parts[1])

    # if its a command $
    elif parts[0] == '$':
        if parts[1] == 'ls':
            # ls is effectively a no-op as the info we're interested
            # in is the output of the command, not the command itself
            pass

        if parts[1] == 'cd':
            if parts[2] != '..':
                for directory in pwd.directories:
                    if directory.name == parts[2]:
                        pwd = directory
                        break
            elif parts[2] == '..':
                pwd = pwd.parent
            pass

    # if its a file it starts with the size of the file as a number
    elif parts[0].isdigit():
        pwd.add_file(parts[1], parts[0])

# root.print_tree(0)
totalSpaceUsed=root.update_dir_size();
print("Total consumed space={}".format(totalSpaceUsed))
totalFreeSpace=(70000000-totalSpaceUsed)
print("Total free space ={}".format(totalFreeSpace))
spaceToFree=(30000000-totalFreeSpace)
print("Space to free ={}".format(spaceToFree))

root.print_tree(0)
print("#### RESULTS ####")
print(root.check_for_size(spaceToFree))
