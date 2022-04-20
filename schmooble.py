import random
import turtle

# class MatingRegister:
# 	def __init__(self):
# 		self.dict = {}
# 		self.schmoobles = {}

# 	def addSchmooble(self, turtleID, position,schmooble):
# 		if turtleID not in self.dict.keys():
# 			self.dict[str(turtleID)] = position
# 			self.schmoobles[str(turtleID)] = schmooble
# 			print("Added turtle:",turtleID)

# 	def removeTurtle(self,turtleID):
# 		self.dict.pop(str(turtleID))

# 	def getMatePositions(self):
# 		outputList = []
# 		for key in self.dict.keys():
# 			outputList.append(self.dict[key])
# 		return outputList

# 	def getMatePosition(self,turtleID):
# 		return self.dict[turtleID]

# 	def getSchmooble(self,turtleID):
# 		return self.schmoobles[turtleID]

# matingRegister = MatingRegister()

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

class Schmooble:
	def __init__(self,idnum,birthPoint=(0,0)):
		#Genes
		self.speed = random.randint(1,100)
		self.energy = random.randint(5,200)
		self.matingEnergyThreshold = random.randint(50,200)
		self.energyTransferToChild = round(random.uniform(0,1),2)
		self.sightRange = random.randint(10,200)
		self.boredomLimit = random.randint(1,21)
		self.mutationRate = round(random.uniform(0,1),2)

		#Meta info
		self.state = 0 #States: 0 = wait; 1 = search for food;
		self.id = idnum

		self.turtle = turtle.Turtle()
		self.turtle.speed = mapRange(self.speed,1,100,0,10)

		self.turtle.onclick(self.creatureInfoClickHelper)
		self.turtle.penup()
		self.turtle.goto(birthPoint)
		self.turtle.pendown()

		self.destination = self.turtle.pos()

	def creatureInfoClickHelper(self,x,y):
		print("Location:",x,y)
		self.creatureInfo()

	def creatureInfo(self):
		print("ID Number:",self.id)
		print("Speed:",self.speed)
		print("Energy:",self.energy)
		print("Mating Threshold:",self.matingEnergyThreshold)
		print("Energy Transfer to Offspring:",self.energyTransferToChild)
		print("Sight Range:",self.sightRange)
		print("Boredom Limit:",self.boredomLimit)
		print("Mutation Rate:",self.mutationRate)
		print("Current State:",self.state)
		print("\n\n")


