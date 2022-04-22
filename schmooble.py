import random
import turtle
from helpers import findMidpoint, mapRange, randomPosition
from foodlist import foodList
import logging

class Schmooble:
	def __init__(self,idnum,birthPoint=(0,0)):
		#Genes
		self.speed = random.randint(1,100)
		self.energy = random.randint(5,100)
		self.matingEnergyThreshold = random.randint(50,200)
		self.energyTransferToChild = round(random.uniform(0.25,1),2)
		self.sightRange = random.randint(50,250)
		self.boredom = 0
		self.boredomLimit = random.randint(1,5)
		self.mutationRate = round(random.uniform(0,1),2)
		self.mateable = False
		self.matingCooldown = random.randint(20,100)
		self.cooldownCounter = 0
		self.age = 0

		#Meta info
		self.state = 1 #States: 0 = wait; 1 = search for food;
		self.id = idnum

		self.turtle = turtle.Turtle()
		self.turtle.speed = 10

		self.turtle.onclick(self.creatureInfoClickHelper)
		self.turtle.penup()
		self.turtle.ht()
		self.turtle.goto(birthPoint)
		self.turtle.setheading(random.randint(0,360))
		self.turtle.st()
	#	self.turtle.pendown()
		self.turtle.speed = mapRange(self.speed,1,100,0,10)
		self.turtle.shape("turtle")
		self.turtle.color("green")

		self.destination = self.turtle.pos()
		self.destinationType = None #Possible values: None, food, mate

	def tick(self):
		if self.state == 0: # wait, mostly unused
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
				logging.debug("Reached destination")
				self.state = 0
				if self.destinationType == 'food':
					if self.destination in foodList.list:
						self.eat()
						foodList.removePoint(self.destination)
						self.state = 1
					else:
						logging.debug("Food disappeared before I got there!")
						self.state = 1
				elif self.destinationType == "mate":
					logging.debug("Reached mate!")
					self.state = 4

			if self.boredom < self.boredomLimit:
				self.boredom = self.boredom + 1
			elif self.boredom >= self.boredomLimit:
				self.boredom = 0
				self.state = 1
		elif self.state == 3: #wander
			logging.debug("This schmooble is wandering!")
			if self.boredom < self.boredomLimit:
				self.move()
				self.boredom = self.boredom + 1
			elif self.boredom >= self.boredomLimit:
				self.boredom = 0
				self.state = 1
		elif self.state == 4: #mate
			if self.boredom < self.boredomLimit:
				self.move()
				self.boredom = self.boredom + 1
			elif self.boredom >= self.boredomLimit:
				self.boredom = 0
				self.state = 1
			pass

		self.energy = self.energy - 1
		logging.debug("Energy left for Schmooble #"+str(self.id)+": "+str(self.energy))

		if self.energy <= 0:
			self.die()

		if abs(self.turtle.pos()[0]) > 475 or abs(self.turtle.pos()[1]) > 475:
			logging.error("Went out of bounds! Location:")
			logging.error(self.turtle.pos())
			self.die()

		if self.cooldownCounter > 0:
			self.cooldownCounter = self.cooldownCounter - 1
			self.mateable = False
		elif self.cooldownCounter == 0 and self.energy >= self.matingEnergyThreshold:
			self.mateable = True

		if self.mateable:
			self.turtle.color("violet red")
		else:
			self.turtle.color("green")


	def move(self):
		logging.debug("Moving...")
		if self.state == 2:
			self.turtle.setheading(self.turtle.towards(self.destination))
			if self.turtle.distance(self.destination) > self.speed:
				self.turtle.forward(self.speed)
			else:
				self.turtle.forward(self.turtle.distance(self.destination))
		elif self.state == 3:
			self.turtle.setheading(self.turtle.heading() + random.randint(-45,45))
			self.turtle.forward(self.speed)


	def eat(self):
		self.energy = self.energy + 25

	def die(self):
		logging.warning("Schmooble #"+str(self.id)+" has died.")
		self.turtle.dot(10,'red')
		self.turtle.ht()
		self.state = -1
		self.creatureInfo()

	def searchForFood(self,foodList=foodList.list):
		logging.debug("Searching for food...")
		closestPoint = (-50000000,-50000000)
		for foodSpot in foodList:
			if self.turtle.distance(foodSpot) <= self.sightRange:
				if self.turtle.distance(foodSpot) < self.turtle.distance(closestPoint):
					closestPoint = foodSpot
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
		print("Energy Transfer to Offspring:",self.energyTransferToChild,"|",round(self.energyTransferToChild * self.energy))
		print("Sight Range:",self.sightRange)
		print("Location",self.turtle.pos())
		print("Destination:",self.destination)
		print("Boredom Limit:",self.boredomLimit)
		print("Mutation Rate:",self.mutationRate)
		print("Current State:",self.state)
		print("Mating State:",self.mateable)
		print("Mating cooldown:",self.matingCooldown)
		print("Current cooldown:",self.cooldownCounter)
		
		# print("\n\n")
		pass

