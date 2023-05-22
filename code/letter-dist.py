import math

def getBestFactors(num):
    greatest = 0
    for i in range(1, int(math.sqrt(num)) + 1):
        if(num % i == 0):
            greatest = i
    return [greatest, int(num/greatest)]


print(getBestFactors(98))