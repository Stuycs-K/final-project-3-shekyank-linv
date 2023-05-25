# Brainf*ck Encoder

## What is Brainf*ck?

Brainf*ck is an esoteric programming language made in 1993. It's extremely minimalist, creating a turing complete language using only eight symbols.

Esoteric programming languages are typically used to test language design, and are typically not intended for actual use.

## The (Brain)f*cking Basics

Brainf*ck only has eight symbols as mentioned earlier, being:
`>`, `<`, `+`, `-`, `.`, `,`, `[`, `]`

The language functions on directly manipulating bytes, with a data pointer and an instruction pointer.

We'll go over the first six symbols first with an example.
Starting off fresh, this is how any brainf*ck's byte registers will look with no instructions.

|Pointer|v|
|-|-|
|Value|0|
|Index|0|

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

Brainf*ck is unable to handle negative numbers in a consistent fashion, depending on the compiler you may get a byte underflow, or just a segfault. Each byte only goes from 0-255, as negative numbers use an extra bit to identify themselves.

Our next symbol is `.`, which just prints out the byte we have. It doesn't print out the number, but instead the byte itself, which is represented by an ASCII character.

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
|>|Shift the data pointer one index to the right. +1|
|<|Shift the data pointer one index to the left. -1|
|+|Add one to the byte that the data pointer is pointing at.|
|-|Subtract one from the byte that the data pointer is pointing at.|
|.|Print out byte that the data pointer is pointing at.|

## Brainf*ck Intermediates

The `[` and `]` symbols designate the start/end of a loop. If the current register is 0 when `[` is encountered, the loop is skipped and the instruction following the corresponding `]` is read. Similarly, if the current register is 0 when `]` is encountered, the loop ends and the next instruction is read.

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
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++.>
```
`558 characters of garbage!`


This code creates very unoptimal brainf*ck code for printing out our message. Here we aren't attempting to optimize for time, but instead space, as we want to encode our message cleanly.

### Looping
From there, we see thatthere is clearly a lot of room for improvement. A first idea may be to factor the number we need to add, in order to save characters. This idea was quickly ditched, as for longer strings, we see that we need to to loop up to where we want to be for every character.

Our solution was setting many byte registers to a nearby number. We set `n` number of byte registers to the average of all the ASCII values, with n here being the total number of characters we are encoding.

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

From here, we can use significantly less characters to get those registers to where they should be, which is a large improvement of using 97 `+` symbols just to get to "a".

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
>++++++[[>]>+++++++++++++[<+++++++>-]<[<]>-]>------------------->++++++++++>+++++++++++++++++>+++++++++++++++++>++++++++++++++++++++>---------------------------------------------[<]>.[>.]
```
`187 characters of clean garbage!`

We can immediately see the optimization here. We do notice however, that if the average is fairly far away, we need to add quite a bit each time, leading to our next optimization.

### Re-using Registers