# Nya~ Read me :3 

## Team Name: Kar-Vi-ng a Path
**Roster:** Vi Lin, Karen Shekyan

## Project Description
This project is a demonstration of a brainf*ck encoder for ASCII characters. It contains four versions of the encoder, numbered (00 - 03) in order from least optimal to most optimal (in terms of the length of the encoding).

00 is the minimum viable encoder, utilizing no brainf*ck loops, and is simply adding to registers and printing them.

01 is an optimization of setting registers to the average first using a loop, and then traversing from there.

02 optimizes by utilizing the same registers multiple times, shortening code by not doing unnecessary work.

03 similar to 02 but checks numbers close to the average, returning the set of instructions with the fewest amount of characters.

## Directions
All the code in this project is made in python, with no libraries. cd-ing to the `code/` directory and running the following commands will run parts of the project:
- `python3 00_minimum.py <MESSAGE> <OUTPUT_FILE>`
- `python3 01_average.py <MESSAGE> <OUTPUT_FILE>`
- `python3 02_distance.py <MESSAGE> <OUTPUT_FILE>`
- `python3 03_shotgun.py <MESSAGE> <OUTPUT_FILE>`

The `code/` directory also includes a brainf*ck compiler, `compiler.c`. This can be compiled using `gcc compiler.c`, and then run with `./a.out <FILE>`.

[WORKLOG](https://github.com/Stuycs-K/final-project-3-shekyank-linv/blob/main/WORKLOG.md)

[PRESENTATION](https://github.com/Stuycs-K/final-project-3-shekyank-linv/blob/main/PRESENTATION.md)
