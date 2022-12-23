#### START OF DATA LOADING ####
file1 = open('Day21/data/input.txt', 'r')

# read file input.txt into an array of strings
lines = file1.readlines()

resolved = dict()
unresolved = []

# loop through each line
for line in lines:
    line = line.strip()
    print(line)
    parts = line.split(' ')

    if len(parts) == 2:
        resolved[parts[0]] = int(parts[1])
    elif len(parts) == 4:
        unresolved.append(parts)

#### DATA LOAD COMPLETE ####


print("Resolved items: ", end='')
print(resolved)

print("Unresolved items: ", end='')
print(unresolved)

while len(unresolved) > 0:
    print("iterating")

    for i in unresolved:

        # check to see if both of the vars this depends on are resolved
        if i[1] in resolved and i[3] in resolved:

            # we should be able to calculate this now
            match i[2]:
                case '+':
                    ans = resolved[i[1]] + resolved[i[3]]
                    pass
                case '*':
                    ans = resolved[i[1]] * resolved[i[3]]
                    pass
                case '-':
                    ans = resolved[i[1]] - resolved[i[3]]
                    pass
                case '/':
                    ans = resolved[i[1]] / resolved[i[3]]
                    pass

            resolved[i[0]] = ans
            unresolved.remove(i)
            break

print("Resolved items: ", end='')
print(resolved)

print("Unresolved items: ", end='')
print(unresolved)
