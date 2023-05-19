import sys

if (len(sys.argv) < 3):
	print("Usage: python3 one-average.py <message> <output_file>")
else:
	message = sys.argv[1]
	average = 0
	for i in message:
		average += ord(i)
	average /= len(message)
	average = round(average)

	#factor the average
	f1 = 1
	f2 = average
	for i in range(1, int(average ** 0.5) + 1):
		if (average // i * i == average):
			f1 = i
	f2 = int(average / f1)

	#find distances
	distances = []
	for i in message:
		distances += [ord(i) - average]

	#write to file
	file = open(sys.argv[2], "w")
	file.write(">" + "+" * len(message)) #setup
	file.write("[[>]>" + "+" * f2)
	file.write("[<" + "+" * f1 + ">-]<[<]>-]>") #set registers to f1*f2
	for i in range(len(distances)):
		if (distances[i] < 0):
			file.write("-" * abs(distances[i]))
		else:
			file.write("+" * distances[i])
		if (i < len(distances) - 1):
			file.write(">")
	file.write("[<]>.[>.]")
	file.close()
