# Brainf*ck Encoder

## What is Brainf*ck?

Brainf*ck is an esoteric programming language made in 1993. It's extremely minimalist, creating a turing complete language using only eight symbols.

Esoteric programming languages are typically used to test language design, and are typically not intended for actual use.

## Brainf*ck Basics

Brainf*ck only has eight symbols as mentioned earlier, being:
`>`, `<`, `+`, `-`, `.`, `,`, `[`, `]`

The language functions on directly manipulating bytes, with a data pointer and an instruction pointer.

We'll go over the first six symbols first with an example.
Starting off fresh, this is how any brainf*ck's byte registers will look with no instructions.


`v`
`0`
`0`

Row one shows the current instructions we have. It is currently empty.
Row two will show where the data pointer is pointing at.
Row three shows the value of the byte at that location.
Row four represents the index of the byte ( for instruction purposes ).

We'll try our first command here.
`>`
`  v`
`0 0`
`0 1`

We move our pointer over to the right by one, creating a new register, set at zero. We can assume that with our next symbol, `<`, it will move... to the left!

`><`
`v  `
`0 0`
`0 1`
