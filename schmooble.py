import random
import turtle
from helpers import findMidpoint, mapRange, randomPosition
from foodlist import foodList

class Census:
	def __init__(self,startingPopulation):
		self.population = {}
		self.livingPop = []
		self.deadPop = []
		self.possibleMates = []
		while len(self.population) < startingPopulation:
			self.population[len(self.population)+1] = Schmooble(len(self.population)+1,randomPosition(100))

	def step(self):
		self.getDeadPopulation()
		self.getLivingPopulation()
		self.getEligableMates()

		if len(self.possibleMates) >= 2:
			for critter1 in self.possibleMates:
				for critter2 in self.possibleMates:
					if critter1 != critter2 and self.population[critter1].canSee(self.population[critter2].turtle.pos()) and self.population[critter2].canSee(self.population[critter1].turtle.pos()):
						if self.population[critter1].turtle.distance(self.population[critter2].turtle.pos()) < 5:
							self.mate(critter1,critter2)
						self.population[critter1].state = 2
						self.population[critter1].destinationType = "mate"
						self.population[critter2].state = 2
						self.population[critter2].destinationType = "mate"
						midpoint = findMidpoint(self.population[critter1].turtle.pos(),self.population[critter2].turtle.pos())
						self.population[critter1].destination = midpoint
						self.population[critter2].destination = midpoint
						print("Found two mates:")
						self.population[critter1].creatureInfo()
						self.population[critter2].creatureInfo()

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
				self.deadPop.append(popID)

	def getLivingPopulation(self):
		self.livingPop = []
		for popID in self.population.keys():
			if self.population[popID].state != -1:
				self.livingPop.append(popID)

	def getEligableMates(self):
		self.possibleMates = []
		for popID in self.population.keys():
			if self.population[popID].mateable == True:
				self.possibleMates.append(popID)

	def mate(parent1ID,parent2ID):
		parent1 = self.population[parent1ID]
		parent2 = self.population[parent2ID]

		outputSchmooble = Schmooble(len(self.population)+1,parent1.turtle.pos())

		mutationRate = abs(((parent1.mutationRate + parent2.mutationRate) / 2) + random.uniform(-1,1))

		outputSchmooble.speed = (parent1.speed + (parent2.speed)/2) * mutationRate
		outputSchmooble.setSpeed(parent1.speed)
		outputSchmooble.energy = round((parent1.energy * parent1.energyTransferToChild) + (parent2.energy * parent2.energyTransferToChild) * mutationRate)
		parent1.energy = round(parent1.energy - (parent1.energy * parent1.energyTransferToChild))
		parent2.energy = round(parent2.energy - (parent2.energy * parent2.energyTransferToChild))
		outputSchmooble.matingEnergyThreshold = round(((parent1.matingEnergyThreshold + parent2.matingEnergyThreshold) / 2) * mutationRate,2)
		outputSchmooble.energyTransferToChild = round(((parent1.energyTransferToChild + parent2.energyTransferToChild) / 2) * mutationRate,2)
		outputSchmooble.sightRange = ((parent1.sightRange + parent2.sightRange)/2)*mutationRate
		outputSchmooble.boredomLimit = ((parent1.boredomLimit + parent2.boredomLimit)/2)*mutationRate
		outputSchmooble.mutationRate = round(mutationRate,2)

		parent1.state = 1
		parent2.state = 1

		return outputSchmooble



class Schmooble:
	def __init__(self,idnum,birthPoint=(0,0)):
		#Genes
		self.speed = random.randint(1,100)
		self.energy = random.randint(5,200)
		self.matingEnergyThreshold = random.randint(50,200)
		self.energyTransferToChild = round(random.uniform(0,1),2)
		self.sightRange = random.randint(50,250)
		self.boredom = 0
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
			print("Ready to mate!")
			self.mateable = True
			self.turtle.color('pink')


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
					self.state = 4
		elif self.state == 3: #wander
			print("This schmooble is wandering!")
			if self.boredom < self.boredomLimit:
				self.move()
				self.boredom = self.boredom + 1
			elif self.boredom >= self.boredomLimit:
				self.boredom = 0
				self.state = 1
		elif self.state == 4: #mate
			pass





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

	def canSee(self,point):
		distance = self.turtle.distance(point)
		if distance <= self.sightRange:
			return True
		else:
			return False

	def creatureInfoClickHelper(self,x,y):
		self.creatureInfo()

	def creatureInfo(self):
		print("\nID Number:",self.id)
		print("Speed:",self.speed)
		print("Energy:",self.energy)
		print("Mating Threshold:",self.matingEnergyThreshold)
		print("Energy Transfer to Offspring:",self.energyTransferToChild)
		print("Sight Range:",self.sightRange)
		print("Location",self.turtle.pos())
		print("Destination:",self.destination)
		print("Boredom Limit:",self.boredomLimit)
		print("Mutation Rate:",self.mutationRate)
		print("Current State:",self.state)
		print("Mating State:",self.mateable)
		
		print("\n\n")


