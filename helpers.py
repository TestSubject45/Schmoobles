import random

def findMidpoint(p1,p2):
	p1x = p1[0]
	p1y = p1[1]

	p2x = p2[0]
	p2y = p2[1]

	midpointX = (p1x + p2x) / 2
	midpointY = (p1y + p2y) / 2

	return (midpointX,midpointY)

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def randomPosition(maxRange):
	return (random.randint(-maxRange,maxRange),random.randint(-maxRange,maxRange))

