# home grown tree example
class Directory:
    def __init__(self, name):
        self.name = name
        self.directories = []
        self.files = []
    
    def add_directory(self, directory):
        self.directories.append(directory)
    
    def add_file(self, file):
        self.files.append(file)
    
    def search_file(self, file_name):
        # search the files in the current directory
        for file in self.files:
            if file.name == file_name:
                print(f"Found file {file_name} in directory {self.name}")
        
        # search the files in the sub-directories
        for directory in self.directories:
            directory.search_file(file_name)

# create a root directory
root = Directory("root")

# create some sub-directories
home = Directory("home")
etc = Directory("etc")

# add the sub-directories to the root directory
root.add_directory(home)
root.add_directory(etc)

# create some files
file1 = File("file1")
file2 = File("file2")
file3 = File("file3")

# add the files to the home directory
home.add_file(file1)
home.add_file(file2)
home.add_file(file3)

# search the directory structure for a file named "file2"
root.search_file("file2")
