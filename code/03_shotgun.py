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

closeToAvg = [average-2, average-1, average, average+1, average+2]
minimumSum = float('inf')
minInstructions = ""
fac1 = 1
fac2 = average

for number in closeToAvg:
    f1 = 1
    f2 = number
    for i in range(1, int(number ** 0.5) + 1):
        if (number // i * i == number):
            f1 = i
    f2 = int(number / f1)

    # From p1 to p2
    def getShift (p1, p2):
        if(p2 < p1):
            return (p1-p2) * "+"
        else:
            return (p2-p1) * "-"

    def getMove (n1, n2):
        if (n2 < n1):
            return (n1-n2) * "<"
        else:
            return (n2-n1) * ">"

    registers = [number] # Set starting register
    lastreg = 0 # Set starting registry
    instList = [] # Create instruction list
    # I'm so sorry this is horrendous code
    for i in message:
        bestreg = 0 # Set default register to look at.
        inst = getShift(ord(i), registers[bestreg]) # Set default instructions.
        # Look through list of existing registers, finding the best register to go to, and get instructions for going there and getting value.
        for j in range(0, len(registers)):
            # If the amt of chars needed to change ascii values to desired + amt of chars needed to traverse to register is better, select that registry.
            if(abs(ord(i) - registers[j] + abs(j - lastreg)) <
               abs(ord(i) - registers[bestreg]) + abs(bestreg - lastreg)):
                bestreg = j
        # Check if going from a new register is better.
        # Check if chars to average plus chars to go to a new register is better than existing.
        if(abs(ord(i) - number) + abs(len(registers) - lastreg) <
           abs(ord(i) - registers[bestreg]) + abs(bestreg - lastreg)):
            # If so, create the new register, and set best register.
            registers.append(number)
            bestreg = len(registers)-1
        # Calculate instruction based on best register.
        inst = getMove(lastreg, bestreg) + getShift(ord(i), registers[bestreg])

        # Update registers, and best registers in order to calculate the direction we have to move next.
        registers[bestreg] = ord(i)
        lastreg = bestreg
        instList.append(inst)

    instList = '.'.join(instList)+'.'
    if (f1 + f2 + len(instList) < minimumSum):
        minimumSum = f1 + f2 + len(instList)
        minInstructions = instList
        fac1 = f1
        fac2 = f2


# write to file
file = open(sys.argv[2], "w")
file.write(">" + "+" * len(registers)) #setup, only need as many registers as calculated.
file.write("[[>]>" + "+" * fac2)
file.write("[<" + "+" * fac1 + ">-]<[<]>-]>") #set registers to f1*f2
file.write(minInstructions) #write calculated instructions
file.close()
