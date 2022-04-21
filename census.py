from schmooble import Schmooble
from helpers import randomPosition, mapRange, findMidpoint
import random

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
							self.population[critter1].creatureInfo()
							self.population[critter2].creatureInfo()
							self.mate(critter1,critter2)
							print("Schmoobles #",critter1,critter2,"have mated.")
						else:
							print("Schmoobles #",critter1,critter2,"are trying to mate...")
							self.population[critter1].state = 2
							self.population[critter1].destinationType = "mate"
							self.population[critter2].state = 2
							self.population[critter2].destinationType = "mate"
							midpoint = findMidpoint(self.population[critter1].turtle.pos(),self.population[critter2].turtle.pos())
							self.population[critter1].destination = midpoint
							self.population[critter2].destination = midpoint


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

	def mate(self,parent1ID,parent2ID):
		parent1 = self.population[parent1ID]
		parent2 = self.population[parent2ID]

		outputSchmooble = Schmooble(len(self.population)+1,parent1.turtle.pos())

		mutationRate = abs(((parent1.mutationRate + parent2.mutationRate) / 2) + random.uniform(-1,1))

		outputSchmooble.speed = (parent1.speed + (parent2.speed)/2) * mutationRate
		outputSchmooble.turtle.speed = mapRange(outputSchmooble.speed,1,100,0,10)
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

		print("Offspring creature info")
		outputSchmooble.creatureInfo()

		self.population[outputSchmooble.id] = outputSchmooble
