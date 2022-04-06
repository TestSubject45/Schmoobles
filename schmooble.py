import random
import turtle

foodDistanceLimit = 400
foodLimit = 20

class FoodList:
	def __init__(self,foodDistanceLimit,foodLimit):
		self.list = []
		self.distanceLimit = foodDistanceLimit
		self.pointLimit = foodLimit
		self.makeFoodList()

		self.turtle = turtle.Turtle()
		self.turtle.speed(0)
		self.turtle.pencolor('red')
		self.sinceReset = 0
		self.drawPoints()

	def makeFoodList(self):
		for i in range(0,self.pointLimit):
			self.addPoint()

	def addPoint(self):
		self.list.append((random.randint(-self.distanceLimit,self.distanceLimit),random.randint(-self.distanceLimit,self.distanceLimit)))

	def removePoint(self,point):
		self.sinceReset = self.sinceReset + 1
		# print(self.list)
		# print(point)
		self.turtle.penup()
		self.turtle.goto(point)
		self.turtle.dot(10,'light green')
		self.turtle.goto(-2000,-2000)
		self.list.remove(point)
		self.addPoint()
		if self.sinceReset > self.pointLimit:
			self.drawPoints()
			self.sinceReset = 0
		else:
			self.drawPoint(self.list[-1])

	def drawPoint(self,point):
		self.turtle.penup()
		self.turtle.goto(point)
		self.turtle.dot(10,'dark green')
		self.turtle.goto(-2000,-2000)

	def drawPoints(self):
		self.turtle.clear()
		for i in range(0,len(self.list)):
			self.turtle.penup()
			self.turtle.goto(self.list[i])
			self.turtle.dot(10,'dark green')
			self.turtle.goto(-2000,-2000)

foodList = FoodList(foodDistanceLimit,foodLimit)

class MatingRegister:
	def __init__(self):
		self.dict = {}

	def addTurtle(self, turtleID, position):
		if turtleID not in self.dict.keys():
			self.dict[str(turtleID)] = position
			print("Added turtle:",turtleID)

	def removeTurtle(self,turtleID):
		self.dict.pop(str(turtleID))

	def getMatePositions(self):
		outputList = []
		for key in self.dict.keys():
			outputList.append(self.dict[key])
		return outputList

matingRegister = MatingRegister()

def findMidpoint(p1,p2):
	p1x = p1[0]
	p1y = p1[1]

	p2x = p2[0]
	p2y = p2[1]

	midpointX = (p1x + p2x) / 2
	midpointY = (p1y + p2y) / 2

	return (midpointX,midpointY)

class Schmooble:
	def __init__(self,idnum):
		self.speed = random.randint(1,10)
		self.energy = random.randint(5,200)
		self.matingEnergyThreshold = random.randint(50,200)
		self.energyTransferToChild = round(random.uniform(0,1),2)
		self.sightRange = random.randint(10,200)
		self.boredomLimit = random.randint(1,21)
		self.mutationRate = round(random.uniform(0,1),2)


		self.turtle = turtle.Turtle()
		self.turtle.speed = self.speed
		self.state = 0 #States: 0 = search, 1 = move, 2 = wander, 3 = mate, 4 = dead
		self.destination = self.turtle.pos()
		self.timeSpentWandering = 0
		self.id = idnum
		self.turtle.onclick(self.creatureInfoClickHelper)

	def creatureInfoClickHelper(self,x,y):
		print("Location:",x,y)
		self.creatureInfo()

	def spendEnergy(self,energy):
		self.energy = self.energy - energy
		if self.energy <= 0:
			self.starve()
#		print("Energy Remaining:",self.energy)

	def starve(self):
		print("No energy!")
		print("This Schmooble has died.")
		self.creatureInfo()
		self.state = 4

	def setSpeed(self,speed):
		if speed > 10:
			self.speed = mapRange(speed,0,speed,0,10)
			self.turtle.speed = mapRange(speed,0,speed,0,10)
		else:
			self.speed = speed
			self.turtle.speed = speed

	def update(self):
		if self.energy >= self.matingEnergyThreshold:
			self.state = 3
#		print("State:",self.state)
		global foodList
		if self.state == 0: #Search for Food
			self.destination = self.searchForFood(foodList.list)
		elif self.state == 1: #Move towards food
			self.move(self.destination)
		elif self.state == 2: #Wander
			self.wander()
		elif self.state == 3: #Search for mate
			self.searchForMate()
		elif self.state == 4: #RIP
			pass

	def searchForFood(self,foodList):
#		print("Searching for food...")
		closestPoint = (-500000,-500000)
		for foodSpot in foodList:
			if self.turtle.distance(foodSpot) <= self.sightRange:
#				print("Found food in range! at",foodSpot)
				if self.turtle.distance(foodSpot) < self.turtle.distance(closestPoint):
					closestPoint = foodSpot
#					print("Closest point of food:",closestPoint)
		self.state = 1
		if closestPoint == (-500000,-500000):
			self.state = 2
			return self.turtle.pos()
		return closestPoint

	def foodAtPoint(self,point):
		global foodList
		if point in foodList.list:
			return True
		else:
			return False

	def move(self,point):
		# print("Moving to",point)
		# print("Current Point",self.turtle.pos())
		self.spendEnergy(1)
		self.turtle.setheading(self.turtle.towards(point))
		self.turtle.forward(self.speed)
		if self.foodAtPoint(point) == False:
#			print("Food at point has dissapeared!")
			self.state = 0
		if self.turtle.distance(point) < 5:
			if self.foodAtPoint(point):
#				print("Yum!")
				self.eat(50)
				foodList.removePoint(point)
				self.state = 0
			else:
#				print("No food here now!")
				self.state = 0

	def moveToMate(self,point):
		self.spendEnergy(1)
		self.turtle.setheading(self.turtle.towards(point))
		self.turtle.forward(self.speed)
		if self.turtle.distance(point) < 5:
			if self.mateAtPoint(point):
				self.mate()
				foodList.removePoint(point)
				self.state = 0
			else:
#				print("No food here now!")
				self.state = 0

	def eat(self,energy):
		self.energy = self.energy + energy
#		print("Current Energy:",self.energy)
		if self.energy >= self.matingEnergyThreshold:
			self.state = 3

	def searchForMate(self):
		global matingRegister
		matingOptions = matingRegister.getMatePositions()
		if len(matingOptions) < 1:
			matingRegister.addTurtle(self.id,self.turtle.pos())
		elif len(matingOptions) == 1:
			pass
		elif len(matingOptions) >= 2:
			for point in matingOptions:
				if self.turtle.distance(point) < self.sightRange and self.turtle.distance(point) != 0:
					print("Mate found!!")
					destination = findMidpoint(self.turtle.pos(),point)
					self.state = 1
					self.move(destination)


	def wander(self):
	#	print("Wandering!")
	#	print("Been wandering for:",self.timeSpentWandering)
		self.spendEnergy(1)
		if self.timeSpentWandering == 0:
			randomDirection = random.randint(0,360)
			self.turtle.setheading(randomDirection)
		if self.timeSpentWandering % round(self.boredomLimit)/11 == 0:
			randomDirection = random.randint(0,360)
			self.turtle.setheading(randomDirection)
		if self.timeSpentWandering < self.boredomLimit:
			self.turtle.forward(self.speed)
			self.timeSpentWandering = self.timeSpentWandering + 1
		elif self.timeSpentWandering >= self.boredomLimit:
			self.state = 0
			self.timeSpentWandering = 0


	def mate(self,mate):
		outputSchmooble = Schmooble()

		mutationRate = abs(((self.mutationRate + mate.mutationRate) / 2) + random.uniform(-1,1))

		outputSchmooble.speed = (self.speed + (mate.speed)/2) * mutationRate
		outputSchmooble.setSpeed(self.speed)
		outputSchmooble.energy = (self.energy * self.energyTransferToChild) + (mate.energy * mate.energyTransferToChild) * mutationRate
		outputSchmooble.matingEnergyThreshold = round(((self.matingEnergyThreshold + mate.matingEnergyThreshold) / 2) * mutationRate,2)
		outputSchmooble.energyTransferToChild = round(((self.energyTransferToChild + mate.energyTransferToChild) / 2) * mutationRate,2)
		outputSchmooble.sightRange = ((self.sightRange + mate.sightRange)/2)*mutationRate
		outputSchmooble.boredomLimit = ((self.boredomLimit + mate.boredomLimit)/2)*mutationRate
		outputSchmooble.mutationRate = round(mutationRate,2)

		return outputSchmooble

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


def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))
