import random
import turtle
from helpers import findMidpoint, mapRange, randomPosition, getDeadPopulation, getLivingPopulation
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

class Census:
	def __init__(self,startingPopulation):
		self.population = {}
		self.livingPop = []
		self.deadPop = []
		while len(self.population) < startingPopulation:
			self.population[len(self.population)+1] = Schmooble(len(self.population)+1,randomPosition(100))

	def step(self):
		self.deadPop = getDeadPopulation(self.population)
		self.livingPop = getLivingPopulation(self.population)

		if len(self.deadPop) == len(self.population):
			print("Everyone's dead!")
			return False
		else:
			for schmoobleID in self.livingPop:
				self.population[schmoobleID].tick()
			return True

	def getDeadPopulation(self):
		self.deadPop = []
		for popID in self.population.keys():
			if self.population[popID].state == -1:
				self.deadPops.append(popID)

	def getLivingPopulation(self):
		self.livingPop = []
		for popID in self.population.keys():
			if self.population[popID].state != -1:
				livingPops.append(popID)

	def getEligableMates(self):
		allMates = []
		for popID in self.population.keys():
			if self.population[popID].mateable == True:
				allMates.append(popID)
		return allMates		



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
		self.mateable = False

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


		if self.energy > self.matingEnergyThreshold:
			self.mateable = True


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
			print("This schmooble is wandering!")
			for i in range(0,self.boredomLimit):
				self.move()
				self.energy = self.energy - 1
			self.state = 1


	def move(self):
		if self.state == 2:
			self.turtle.setheading(self.turtle.towards(self.destination))
			if self.turtle.distance(self.destination) > self.speed:
				self.turtle.forward(self.speed)
			else:
				self.turtle.forward(self.turtle.distance(self.destination))
		elif self.state == 3:
			self.turtle.setheading(random.randint(1,365))
			self.turtle.forward(self.speed)


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


