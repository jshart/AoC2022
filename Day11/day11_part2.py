# read file input.txt into an array of strings
file1 = open('Day11/data/input.txt', 'r')
lines = file1.readlines()

key = 3*13*2*11*5*17*19*7


class Monkey:
    def __init__(self, raw):
        self.raw = raw
        self.inspections = 0
        for s in raw:
            if s.startswith("Monkey"):
                self.monkeyNumber = int(s.split(' ')[1].split(':')[0])
            if s.startswith("Starting items"):
                s = s.replace("Starting items: ", "")
                itemstr = s.split(", ")
                self.items = list(map(int, itemstr))
                print(self.items)
            if s.startswith("If true"):
                temp = s.split(' ')
                self.ifTrue = int(temp[-1])
            if s.startswith("If false"):
                temp = s.split(' ')
                self.ifFalse = int(temp[-1])
            if s.startswith("Test"):
                temp = s.split(' ')
                self.test = int(temp[-1])
            if s.startswith("Operation"):
                self.ops = s.split(' ')
                # output:
                # ops:[['Operation:', 'new', '=', 'old', '+', '3']]
                # but we're only really interested in the last 2 elements
                # as everything else is constant.
                del self.ops[:4]
                # ops:[['+', '3']]

    def printRaw(self):
        print(self.raw)

    def printMonkey(self):
        print("Monkey ID:{} ".format(self.monkeyNumber))
        print("- Test:{} ".format(self.test))
        print("- If true:{} ".format(self.ifTrue))
        print("- If false:{} ".format(self.ifFalse))
        print("- items:[{}] ".format(self.items))
        print("- ops:[{}] ".format(self.ops))

    def inspect(self, monkeys):

        self.inspections += 1

        # fetch the items we'll be working on
        item = self.items.pop(0)
        if self.ops[1] == 'old':
            rhs = item
        else:
            rhs = int(self.ops[1])

        # execute the operation
        match self.ops[0]:
            case '+':
                item += rhs
            case '*':
                item *= rhs

        # reduce the worry level now that its been inspected
        # item = int(item/3)
        item = item % key

        # now lets perform the test
        if item % self.test == 0:
            # divisible
            monkeys[self.ifTrue].items.append(item)
            #print("Monkey {} throwing {} to Monkey {}".format(self.monkeyNumber, item, self.ifTrue))
        else:
            monkeys[self.ifFalse].items.append(item)
            #print("Monkey {} throwing {} to Monkey {}".format(self.monkeyNumber, item, self.ifFalse))


print("### PARSING PROGRAM ###")
raw = []
monkeys = []
# parse each line
for line in lines:
    line = line.strip()
    if (len(line) == 0):
        print("====")
        monkeys.append(Monkey(raw.copy()))
        raw.clear()
    else:
        raw.append(line)

monkeys.append(Monkey(raw.copy()))

print("Key: {}".format(key))


for m in monkeys:
    m.printRaw()
    m.printMonkey()


print("### STARTING GAME ###")
for i in range(10000):
    print("### ROUND = {}".format(i))
    for m in monkeys:
        while len(m.items) > 0:
            m.inspect(monkeys)

ins = []
for m in monkeys:
    print("Monkey {} did {} inspections".format(m.monkeyNumber, m.inspections))
    ins.append(m.inspections)

ins.sort(reverse=True)
print(ins)
print("Final answer:{}".format(ins[0]*ins[1]))
