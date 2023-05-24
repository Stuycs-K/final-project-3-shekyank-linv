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
string="Hello!"
fck=""
for i in string:
    fck += ord(i) * '+' + '.' + '>'
```

Output:
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++.>
```

This code creates very inoptimal brainf*ck code for printing out our message. Here we aren't attempting to optimize for time, but instead space, as we want to encode our message cleanly.