# Brainf*ck Encoder

## What is Brainf*ck?

Brainf*ck is an esoteric programming language made in 1993. It's an extremely minimalist, turing complete language using only eight symbols.

Esoteric programming languages are typically used to test language design, and are not intended for actual use.

## The (Brain)f*cking Basics

Brainf*ck only has eight symbols, as mentioned earlier, which are:
`>`, `<`, `+`, `-`, `.`, `,`, `[`, `]`

The language directly manipulates bytes using a data pointer and an instruction pointer.

We'll go over the first six symbols first with examples.
Starting off fresh, this is how any brainf*ck's byte registers will look with no instructions.

|Pointer|v||
|-|-|-|
|Value|0|0|
|Index|0|1|

We'll try our first command here.

`>`

|Pointer||v|
|-|-|-|
|Value|0|0|
|Index|0|1|

We move our pointer over to the right by one to a new register, set at zero. We can assume that with our next symbol, `<`, it will move... to the left!

`><`

|Pointer|v||
|-|-|-|
|Value|0|0|
|Index|0|1|

`+` and `-` should be fairly intuitive, as we see below.

`+`

|Pointer|v|
|-|-|
|Value|1|
|Index|0|

`+-`

|Pointer|v|
|-|-|
|Value|0|
|Index|0|

Brainf*ck is unable to handle negative numbers in a consistent fashion; depending on the compiler you may get a byte underflow or just a segfault. Each byte only goes from 0-255.

Our next symbol is `.`, which just prints out the current byte. The byte is rendered as an ASCII character rather than an integer.

Here's thirty three `+`'s!
`+++++++++++++++++++++++++++++++++.`

|Pointer|v|
|-|-|
|Value|33|
|Index|0|

Output:
`!`

We know that `!`'s ASCII value is 33, which lines up with our byte at index 0.

We're going to skip over `,`, but it should be known that it simply lets you take in a user input.

|Symbol|Purpose|
|-|-|
|>|Shift the data pointer one index to the right.|
|<|Shift the data pointer one index to the left.|
|+|Add one to the byte that the data pointer is pointing at.|
|-|Subtract one from the byte that the data pointer is pointing at.|
|.|Print out byte that the data pointer is pointing at.|

## Brainf*ck Intermediates

The `[` and `]` symbols designate the start/end of a loop. If the current register is 0 when `[` is encountered, the instruction pointer jumps to the corresponding `]` and the next instruction is read. Conversely, if the current register is not 0 when `]` is encountered, the instruction pointer jumps back to the corresponding `[`.

With the use of loops we can easily construct a piece of brainf*ck code to multiply two numbers:

`+++[->++++<]`

<table>
<tr><th> Before Loop </th><th> After Loop </th></tr>
<tr><td>

|Pointer|v||
|-|-|-|
|Value|3|0|
|Index|0|1|

</td><td>

|Pointer|v||
|-|-|-|
|Value|0|12|
|Index|0|1|

</td></tr> </table>

**Visualizer:** https://ashupk.github.io/Brainfuck/brainfuck-visualizer-master/index.html

When encoding messages we'll also need to efficiently traverse registers, especially to find the start/end of our message. Again, loops simplify this task:

- `[<]` seeks the start of the message
- `[>]` seeks the end of the message

Visualize this: `>+++++[[>]+[<]>-]`
<!-- >+++++[-[>]+[<]>] is an infinite loop!-->

## Encoding ASCII in Brainf*ck
We started off with the simplest form of the project, with no loops and just adding to the registers.

Python code below:
```
message="Hello?"
fck=""
for i in message:
    fck += ord(i) * '+' + '.' + '>'
print(fck)
```

Output:
```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++.>
```
`575 characters of garbage!`


This code creates very unoptimal brainf*ck code for printing out our message. Here we aren't attempting to optimize for time, but instead space, as we want to encode our message cleanly.

### Looping
From there, we see that there is clearly a lot of room for improvement. A first idea may be to factor the number we need to add, in order to save characters. This idea was quickly ditched, as for longer strings, we see that we need to loop up to where we want to be for every character.

Our solution was setting many byte registers to a nearby number. We set `n` byte registers to the average of all the ASCII values, where `n` is the total number of characters we are encoding.

Example for setting 4 registers to 8 * 9
```
>++++
[
    [>]
    >++++++++
    [
        <+++++++++>-
    ]
    <[<]
    >-
]
```

From here, we can use significantly fewer characters to get those registers to where they should be, which is a large improvement to using 97 `+` symbols just to get to "a".

Python code below:
```
message="Hello?"
fck=""
average = 0
for i in message:
    average += ord(i)
average /= len(message)
average = round(average)

# Factor Average
f1 = 1
f2 = average
for i in range(1, int(average ** 0.5) + 1):
    if (average // i * i == average):
        f1 = i
f2 = int(average / f1)

# Find distances from each character to average
distances = []
for i in message:
    distances += [ord(i) - average]

# Set registers to f1*f2, being the factors of the average
fck += ">" + "+" * len(message)
fck += "[[>]>" + "+" * f2 + "[<" + "+" * f1 + ">-]<[<]>-]>"

# Adjust each register to be its assigned character
for i in range(len(distances)):
    if (distances[i] < 0):
        fck += "-" * abs(distances[i])
    else:
        fck += "+" * distances[i]
    if (i < len(distances) - 1):
        fck += ">"

# Print out all the registers
fck += "[<]>.[>.]"

print(fck)
```

Output:
```
>++++++[[>]>+++++++++++++++++++++++++++++++++++++++++++++++[<++>-
]<[<]>-]>---------------------->+++++++>++++++++++++++>++++++++++
++++>+++++++++++++++++>-------------------------------[<]>.[>.]
```
`194 characters of clean garbage!`

We can immediately see the optimization here. We do notice however, that if the average is fairly far away, we still need to add/subtract quite a bit each time, leading to our next optimization.

### Re-using Registers
While the average (`n`) is a good approximation for all the ASCII values, it's sometimes better to simply reuse registers. For example, suppose we're in this situation (where our `n` is 110):

|Pointer|||||v|||
|-|-|-|-|-|-|-|-|
|Value|0|100|120|107|110|110|...|
|Index|0|1|2|3|4|5|...|

If the next letter in our message is 'e' (ASCII value of 101), we can see that it's better to use register 3 and subtract 6 from it than to use register 4 and subtract 9. In fact, it's even better to use register 1 and add 1!

Notice that we must consider both distance and difference since both contribute equally to the length of our code. Now this is essentially a pathfinding problem.

Python code below:
```
message = "Hello?"
fck = ""

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
        return (p1-p2) * "+"
    else:
        return (p2-p1) * "-"

def getMove(n1, n2):
    if(n2 < n1):
        return (n1-n2) * "<"
    else:
        return (n2-n1) * ">"

registers = [average] # Set starting register
lastreg = 0 # Set starting registry
instList = [] # Create instruction list
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
    if(abs(ord(i) - average) + abs(len(registers) - lastreg) <
       abs(ord(i) - registers[bestreg]) + abs(bestreg - lastreg)):

        # If so, create the new register, and set best register.
        registers.append(average)
        bestreg = len(registers)-1

    # Calculate instruction based on best register.
    inst = getMove(lastreg, bestreg) + getShift(ord(i), registers[bestreg])

    # Update registers, and best registers in order to calculate the direction we have to move next.
    registers[bestreg] = ord(i)
    lastreg = bestreg
    instList.append(inst)

instList = '.'.join(instList)+'.'

fck += ">" + "+" * len(registers) #setup, only need as many registers as calculated
fck += "[[>]>" + "+" * f2
fck += "[<" + "+" * f1 + ">-]<[<]>-]>" # Set registers to f1*f2
fck += instList # Write calculated instructions

print(fck)
```
Output:
```
>++[[>]>+++++++++++++++++++++++++++++++++++++++++++++++[<++>-]<[<]
>-]>----------------------.>+++++++.+++++++..+++.<---------.
```
`126 characters of cleaner garbage!`

There's still room for improvement. We currently rely on our average being "nice," meaning that it has a pair of factors that are close together. If our average happens to be prime or the product of 2 and a large prime, then our code will still be annoyingly long.

### Takin' It Out Back
"Good-bye old boy. Take good care of that old yeller dog."

Instead of solving the problem in a more algorithmic way, we decided that since the code ran fairly quickly anyways, we could take a more brutish approach, which we called "shotgunning".

We would take every number within a range of 2 from the average, and run our above algorithm above on it. We would take the one with the least amount of brainf*ck characters, and that would be the best one we selected.

This of course relied on the assumption that the best number would be within 2 of the mean, even though this likely isn't true for every case, it was always going to be as good or better than just selecting the average.

Python code below:
```
message = "Hello?"

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

fck += ">" + "+" * len(registers) #setup, only need as many registers as calculated.
fck += "[[>]>" + "+" * fac2
fck += "[<" + "+" * fac1 + ">-]<[<]>-]>" #set registers to fac1*fac2
fck += minInstructions
print(fck)
```
Output:

```
>++[[>]>++++++++++++[<++++++++>-]<[<]>-]>------------------------.>+++++.+++++++..+++.<---------.
```
`97 characters of the cleanest garbage around!`
