# read file input.txt into an array of strings
file1 = open('Day20/data/input_test.txt', 'r')
lines = file1.readlines()

staticIndex = []

# create a linked list class with forward and backward points
# TODO: Need to make this looped (tail->head)
# TODO: Need to make it circular listed safe


class Node:
    def __init__(self, value):
        self.data = value
        self.next = None
        self.prev = None

    def add(self, value):
        newNode = Node(value)
        newNode.prev = self
        self.next = newNode
        return newNode

    # loop unsafe atm
    def printFromHere(self):
        self.printThisNode()
        if self.next != None:
            self.next.printFromHere()

    def printThisNode(self):
        print("[P:{} c:{} N:{}]  == V:{} ".format(
            self.prev, self, self.next, self.data))

    def printNNodesFromHere(self, n):
        print("Loop:{} == ".format(n), end='')
        self.printThisNode()
        if n > 1:
            if self.next != None:
                self.next.printNNodesFromHere(n-1)

    def printNValuesFromHere(self, n):
        print("[{}]".format(self.data), end='')
        if n > 1:
            if self.next != None:
                self.next.printNValuesFromHere(n-1)

    def removeThisNode(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = None
        self.prev = None

    def linkToNode(self, n):
        self.next = n
        n.prev = self

    # insert X after A, so we should have A,X,B
    def insertNodeAfter(self, after):
        after.prev = self
        after.next = self.next
        self.next.prev = after
        self.next = after

    def insertNodeBefore(self, before):
        before.prev = self.prev
        before.next = self
        self.prev.next = before
        self.prev = before

    def findNodeNForward(self, n):
        thisNode = self
        while n > 0:
            thisNode = thisNode.next
            n -= 1
        return thisNode

    def findNodeNBackward(self, n):
        thisNode = self
        n = abs(n)
        while n > 0:
            thisNode = thisNode.prev
            n -= 1
        return thisNode

    def findNodeNDistance(self, n):
        if n > 0:
            return self.findNodeNForward(n)
        else:
            return self.findNodeNBackward(n)

    def moveNodeNDistance(self, n):
        if n > 0:
            print("Moving forward {} nodes".format(n))
            self.findNodeNForward(n).insertNodeBefore(self)
        else:
            print("Moving backwards {} nodes".format(n))
            self.findNodeNBackward(n).insertNodeAfter(self)


print("### PARSING PROGRAM ###")
# parse each line
for line in lines:
    line = line.strip()
    print(line)
    staticIndex.append(int(line))

# Build the linked list from the input data, and geneate a direct
# access index that allows us to connect to a node based on its *original*
# position in the list.
ll = Node(staticIndex[0])
staticIndex[0] = (staticIndex[0], ll)
head = ll
for i in range(1, len(staticIndex)):
    ll = ll.add(staticIndex[i])
    staticIndex[i] = (staticIndex[i], ll)

ll.linkToNode(head)
head.printNNodesFromHere(len(staticIndex))


# print("### STARTING PROGRAM Static Index len={} ###".format(len(staticIndex)))
# for i in staticIndex:
#     print("Processing item [{}] which has value [{}]".format(i[0], i[1].data))
#     thisNode = i[1]
#     # find this nodes new position
#     newPosition = thisNode.findNodeNDistance(i[0])
#     print(
#         "--> move to new position, after data item set to value [{}]".format(newPosition.data))


print("### STARTING PROGRAM Static Index len={} ###".format(len(staticIndex)))
print("Starting State:", end='')
staticIndex[0][1].printNValuesFromHere(len(staticIndex))
print()

for i in staticIndex:
    thisNode = i[1]

    thisNode.moveNodeNDistance(i[0])
    print("Executing move for:", end='')
    thisNode.printThisNode()
    print("State after move:", end='')
    thisNode.printNValuesFromHere(len(staticIndex))
    print()
