import random
import turtle
from helpers import findMidpoint, mapRange
from foodlist import foodList

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



class Schmooble:
	def __init__(self,idnum,birthPoint=(0,0)):
		#Genes
		self.speed = random.randint(1,100)
		self.energy = random.randint(5,200)
		self.matingEnergyThreshold = random.randint(50,200)
		self.energyTransferToChild = round(random.uniform(0,1),2)
		self.sightRange = random.randint(10,200)
		self.boredomLimit = random.randint(1,5)
		self.mutationRate = round(random.uniform(0,1),2)

		#Meta info
		self.state = 1 #States: 0 = wait; 1 = search for food;
		self.id = idnum

		self.turtle = turtle.Turtle()
		self.turtle.speed = 10

		self.turtle.onclick(self.creatureInfoClickHelper)
		self.turtle.penup()
		self.turtle.goto(birthPoint)
		self.turtle.setheading(random.randint(0,360))
		self.turtle.pendown()
		self.turtle.speed = mapRange(self.speed,1,100,0,10)

		self.destination = self.turtle.pos()
		self.destinationType = None #Possible values: None, food, mate

	def tick(self):
		print("Energy left for Schmooble #"+str(self.id)+":",self.energy)
		self.energy = self.energy - 1
		if self.energy <= 0:
			self.die()
		if self.state == 0: # wait
			pass
		elif self.state == 1: # look for food
			self.destination = self.searchForFood()
			if self.turtle.distance(self.destination) > 5:
				self.state = 2
				self.destinationType = "food"
			else:
				self.state = 3
		elif self.state == 2: #moving to destination
			self.move()
			if self.turtle.distance(self.destination) < 5:
				print("Reached destination")
				self.state = 0
				if self.destinationType == 'food':
					self.eat()
					foodList.removePoint(self.destination)
					self.state = 1
				elif self.destinationType == "mate":
					pass
		elif self.state == 3: #wander
			for i in range(0,self.boredomLimit):
				self.turtle.setheading(random.randint(1,365))
				self.move()
			self.state = 1

	def move(self):
		self.turtle.setheading(self.turtle.towards(self.destination))
		if self.turtle.distance(self.destination) > self.speed:
			self.turtle.forward(self.speed)
		else:
			self.turtle.forward(self.turtle.distance(self.destination))

	def eat(self):
		self.energy = self.energy + 50

	def die(self):
		self.turtle.dot(10,'red')
		self.turtle.ht()
		self.state = -1

	def searchForFood(self,foodList=foodList.list):
		print("Searching for food...")
		closestPoint = (-50000000,-50000000)
		for foodSpot in foodList:
			if self.turtle.distance(foodSpot) <= self.sightRange:
				print("Found food in range! at",foodSpot)
				if self.turtle.distance(foodSpot) < self.turtle.distance(closestPoint):
					closestPoint = foodSpot
		print("Closest point of food:",closestPoint,"Distance:",self.turtle.distance(closestPoint))
		if closestPoint == (-50000000,-50000000):
			return self.turtle.pos()
		return closestPoint

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


