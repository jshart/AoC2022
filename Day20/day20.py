# read file input.txt into an array of strings
file1 = open('Day20/data/input.txt', 'r')
lines = file1.readlines()

staticIndex = []

# create a linked list class with forward and backward points
# TODO: Need to make this looped (tail->head)
# TODO: Need to make it circular listed safe

# 1650 is too low? (probably not negative)

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
        # print("Removing {}".format(self.data))
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = None
        self.prev = None

    def linkToNode(self, n):
        self.next = n
        n.prev = self

    # insert X(self) after A, so we should have A,X,B
    def insertNodeAfter(self, after):

        # first of all lets detach this node from the list
        self.removeThisNode()
        # after.printNValuesFromHere(7)
        # print()

        # A is the point after where we want to insert
        A = after
        # B is currently the next node after A
        B = after.next

        # now let insert our node and relink the list
        A.next = self
        self.prev = A
        self.next = B
        B.prev = self

    # # insert X(self) before A, so we should have A,X,B
    # def insertNodeBefore(self, before):
    #     # first of all lets detach this node from the list
    #     self.removeThisNode()
    #     # before.printNValuesFromHere(7)
    #     # print()

    #     # B is the point before where we want to insert
    #     A = before

    #     # A is currently the node previous to B
    #     B = before.prev

    #     # now let insert our node and relink the list
    #     A.next = self
    #     self.prev = A
    #     self.next = B
    #     B.prev = self

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
            # print("Moving forward {} nodes".format(n))
            self.insertNodeAfter(self.findNodeNForward(n))
        else:
            # we need to move one less in the backward direction, as it lets as
            # still treat it as a "move after"
            n -= 1
            # print("Moving backwards {} nodes".format(n))
            self.insertNodeAfter(self.findNodeNBackward(n))


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

# head.printNNodesFromHere(len(staticIndex))


# print("### STARTING PROGRAM Static Index len={} ###".format(len(staticIndex)))
# for i in staticIndex:
#     print("Processing item [{}] which has value [{}]".format(i[0], i[1].data))
#     thisNode = i[1]
#     # find this nodes new position
#     newPosition = thisNode.findNodeNDistance(i[0])
#     print(
#         "--> move to new position, after data item set to value [{}]".format(newPosition.data))


print("### STARTING PROGRAM Static Index len={} ###".format(len(staticIndex)))
# print("Starting State:", end='')
# staticIndex[0][1].printNValuesFromHere(len(staticIndex))
# print()

for c, i in enumerate(staticIndex):
    thisNode = i[1]
    print("Shuffle Round:{} for value:{}".format(c, thisNode.data))
    if i[0] != 0:

        # performance optimisation - if its longer than the list size, we can reduce it by
        # the list size as the first 5000 moves does one complete move and we end up where we
        # are anyway
        # if i[0] > 5000:
        #     thisNode.moveNodeNDistance(i[0]-5000)
        # else:
        thisNode.moveNodeNDistance(i[0])

        # r=i[0] % len(staticIndex)
        # thisNode.moveNodeNDistance(r)


        # print("Executing move for:", end='')
        # thisNode.printThisNode()
        # print("State after move:", end='')
        # thisNode.printNValuesFromHere(len(staticIndex))
        # print()

# sanity check
errorFound = False
pNode = head
for c, i in enumerate(staticIndex):
    thisNode = i[1]
    if i[0] != thisNode.data:
        errorFound = True
        print("data error: c={} i[0]={} n={}".format(c, i[0], thisNode.data))
        exit()

    print("[{}],".format(pNode.data),end='')
    pNode = pNode.next

print()
if errorFound:
    print("ERROR: Error found in data")

for c, i in enumerate(staticIndex):
    thisNode = i[1]

    if i[0] == 0:
        break

sum = 0
print("Found zero at position [{}]".format(c))
n = i[1].findNodeNForward(1000)
sum += n.data
print("Found 1000 nodes forward of zero:{}".format(n.data))
n = i[1].findNodeNForward(2000)
sum += n.data
print("Found 2000 nodes forward of zero:{}".format(n.data))
n = i[1].findNodeNForward(3000)
sum += n.data
print("Found 3000 nodes forward of zero:{}".format(n.data))

print("Final sum:{}".format(sum))
