import sys
if(len(sys.argv) < 3):
    print("Not enough arguments.\n")
    print("Usage: python3 zero-minimum.py <message> <output_file>")
    sys.exit()

message = sys.argv[1]
filename = sys.argv[2]

average = 0
for i in message:
    average += ord(i)
average /= len(message)
average = round(average)

f1 = 1
f2 = average
for i in range(1, int(average ** 0.5) + 1):
    if (average // i * i == average):
        f1 = i
f2 = int(average / f1)

# From p1 to p2
def getShift(p1, p2):
    if(p2 < p1):
        return (p1-p2) * "-"
    else:
        return (p2-p1) * "+"
    
def getMove(n1, n2):
    if(n2 < n1):
        return (n1-n2) * "<"
    else:
        return (n2-n1) * ">"

registers = [average]
bestregs = [0]
instList = []
for i in message:
    bestreg = 0
    inst = getShift(ord(i), registers[bestreg])
    for j in range(0, len(registers)):
        if(abs(ord(i) - registers[j]) < abs(ord(i) - registers[bestreg])):
            bestreg = j
            inst = getShift(ord(i), registers[bestreg])
    if(abs(ord(i) - average) < abs(ord(i) - registers[bestreg])):
        registers.append(average)
        bestreg = len(registers)-1
        inst = getShift(ord(i), registers[bestreg])
    
    registers[bestreg] = ord(i)
    inst = getMove(bestregs[len(bestregs)-1], bestreg) + inst
    bestregs.append(bestreg)
    instList.append(inst)

# print(instList)
# print(bestregs)

instList = '.'.join(instList)
print(instList)

#write to file
# file = open(sys.argv[2], "w")
# file.write(">" + "+" * len(message)) #setup
# file.write("[[>]>" + "+" * f2)
# file.write("[<" + "+" * f1 + ">-]<[<]>-]>") #set registers to f1*f2
# for i in range(len(distances)):
# 	if (distances[i] < 0):
# 		file.write("-" * abs(distances[i]))
# 	else:
# 		file.write("+" * distances[i])
# 	if (i < len(distances) - 1):
# 		file.write(">")
# file.write("[<]>.[>.]")
# file.close()
