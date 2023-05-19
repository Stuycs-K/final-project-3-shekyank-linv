import sys
if(len(sys.argv) < 3):
    print("Not enough arguments.\n")
    print("Usage: python3 zero-minimum.py <message> <output_file>")
    sys.exit()

string = sys.argv[1]
filename = sys.argv[2]
fck = ""

for i in string:
    fck += ord(i) * '+' + '.' + '>'

f = open(filename, "w")
f.write(fck)
f.close()