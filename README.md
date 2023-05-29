# Nya~ Read me :3 
## Project Description
This project is a demonstration of a brainf*ck encoder for ASCII characters. It contains four versions of the encoder, numbered in order from least optimal to most optimal. (00 - 03)

00 is the minimum viable encoder, utilizing no brainf*ck loops, and is simply adding to registers and printing them.

01 is an optimization of setting registers to the average first using a loop, and then traversing from there.

02 optimizes by utilizing the same registers multiple times, saving time so that moving from the average over and over doesn't have to be done continually.

03 iterates on 02, instead using just the average as the base, it tests numbers close to the average, and returns the set of instructions with the least amount of characters.

## Directions
All the code in this project is made in python, with no libraries. Coing to the `code/` directory and running the following commands will run parts of the project:
- `python3 00_minimum.py <MESSAGE> <OUTPUT_FILE>`
- `python3 01_average.py <MESSAGE> <OUTPUT_FILE>`
- `python3 02_distance.py <MESSAGE> <OUTPUT_FILE>`
- `python3 03_shotgun.py <MESSAGE> <OUTPUT_FILE>`

The `code/` directory also includes a brainf*ck compiler, being `compiler.c`. This can be compiled using `gcc compiler.c`, and then run with `./a.out <FILE>`.

[WORKLOG](https://github.com/Stuycs-K/final-project-3-shekyank-linv/blob/main/WORKLOG.md)

[PRESENTATION](https://github.com/Stuycs-K/final-project-3-shekyank-linv/blob/main/PRESENTATION.md)
