import random
import turtle

foodDistanceLimit = 300
foodLimit = 10

class FoodList:
	def __init__(self,foodDistanceLimit,foodLimit):
		self.list = []
		self.distanceLimit = foodDistanceLimit
		self.pointLimit = foodLimit
		self.makeFoodList()

		self.turtle = turtle.Turtle()
		self.turtle.speed(0)
		self.turtle.pencolor('red')

	def makeFoodList(self):
		for i in range(0,self.pointLimit):
			self.addPoint()

	def addPoint(self):
		self.list.append((random.randint(-self.distanceLimit,self.distanceLimit),random.randint(-self.distanceLimit,self.distanceLimit)))

	def removePoint(self,point):
		print(self.list)
		print(point)
		self.list.remove(point)
		self.addPoint()
		self.drawPoints()

	def drawPoints(self):
		self.turtle.clear()
		for i in range(0,len(self.list)):
			self.turtle.penup()
			self.turtle.goto(self.list[i])
			self.turtle.dot()
			self.turtle.goto(-2000,-2000)

foodList = FoodList(foodDistanceLimit,foodLimit)
foodList.drawPoints()


class Schmooble:
	def __init__(self,parent1=None,parent2=None):
		if parent1 == None or parent2 == None:
			self.speed = random.randint(1,10)
			self.energy = random.randint(5,200)
			self.matingEnergyThreshold = round(random.uniform(0,1),2)
			self.energyTransferToChild = round(random.uniform(0,1),2)
			self.sightRange = random.randint(10,200)
			self.boredomLimit = random.randint(1,20)
			self.mutationRate = round(random.uniform(0,1),2)
		else:
			self.mate(parent1,parent2)

		self.turtle = turtle.Turtle()
		self.turtle.speed = self.speed
		self.state = 0 #States: 0 = search, 1 = move, 2 = wander, 3 = mate
		self.destination = self.turtle.pos()
		self.timeSpentWandering = 0

	def setSpeed(self,speed):
		if speed > 10:
			self.speed = mapRange(speed,0,speed,0,10)
			self.turtle.speed = mapRange(speed,0,speed,0,10)
		else:
			self.speed = speed
			self.turtle.speed = speed

	def update(self):
		global foodList
		if self.state == 0:
			self.destination = self.searchForFood(foodList.list)
		elif self.state == 1:
			self.move(self.destination)
		elif self.state == 2:
			self.wander()
		elif self.state == 3:
			self.searchForMate()

	def searchForFood(self,foodList):
		closestPoint = (-500000,-500000)
		for foodSpot in foodList:
			if self.turtle.distance(foodSpot) <= self.sightRange:
				print("Found food in range! at",foodSpot)
				if self.turtle.distance(foodSpot) < self.turtle.distance(closestPoint):
					closestPoint = foodSpot
					print("Closest point of food:",closestPoint)
		self.state = 1
		if closestPoint == (-500000,-500000):
			self.state = 2
			return self.turtle.pos()
		return closestPoint

	def move(self,point):
		# print("Moving to",point)
		# print("Current Point",self.turtle.pos())
		self.turtle.setheading(self.turtle.towards(point))
		self.turtle.forward(self.speed)
		if self.turtle.distance(point) < 5:
			print("Yum!")
			self.eat(50)
			foodList.removePoint(point)
			self.state = 0

	def eat(self,energy):
		self.energy = self.energy + energy
		if self.energy >= self.matingEnergyThreshold:
			self.state = 3

	def searchForMate(self):
		pass

	def wander(self):
	#	print("Wandering!")
	#	print("Been wandering for:",self.timeSpentWandering)
		if self.timeSpentWandering == 0:
			randomDirection = random.randint(0,360)
			self.turtle.setheading(randomDirection)
		if self.timeSpentWandering % round(self.boredomLimit/10) == 0:
			randomDirection = random.randint(0,360)
			self.turtle.setheading(randomDirection)
		if self.timeSpentWandering < self.boredomLimit:
			self.turtle.forward(self.speed)
			self.timeSpentWandering = self.timeSpentWandering + 1
		elif self.timeSpentWandering >= self.boredomLimit:
			self.state = 0
			self.timeSpentWandering = 0


	def mate(self,parent1,parent2):
		mutationRate = abs(((parent1.mutationRate + parent2.mutationRate) / 2) + random.uniform(-1,1))

		self.speed = (parent1.speed + (parent2.speed)/2) * mutationRate
		self.setSpeed(self.speed)
		self.energy = (parent1.energy * parent1.energyTransferToChild) + (parent2.energy * parent2.energyTransferToChild) * mutationRate
		self.matingEnergyThreshold = round(((parent1.matingEnergyThreshold + parent2.matingEnergyThreshold) / 2) * mutationRate,2)
		self.energyTransferToChild = round(((parent1.energyTransferToChild + parent2.energyTransferToChild) / 2) * mutationRate,2)
		self.sightRange = ((parent1.sightRange + parent2.sightRange)/2)*mutationRate
		self.boredomLimit = ((parent1.boredomLimit + parent2.boredomLimit)/2)*mutationRate
		self.mutationRate = round(mutationRate,2)

	def creatureInfo(self):
		print("Speed:",self.speed)
		print("Energy:",self.energy)
		print("Mating Threshold:",self.matingEnergyThreshold)
		print("Energy Transfer to Offspring:",self.energyTransferToChild)
		print("Sight Range:",self.sightRange)
		print("Boredom Limit:",self.boredomLimit)
		print("Mutation Rate:",self.mutationRate)
		print("\n\n")


def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))
