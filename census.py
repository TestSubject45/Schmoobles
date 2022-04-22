from schmooble import Schmooble
from helpers import randomPosition, mapRange, findMidpoint
import random
import logging

class Census:
	def __init__(self,startingPopulation):
		self.population = {}
		self.livingPop = []
		self.deadPop = []
		self.possibleMates = []
		while len(self.population) < startingPopulation:
			self.population[len(self.population)+1] = Schmooble(len(self.population)+1,randomPosition(200))

	def step(self):
		self.getDeadPopulation()
		self.getLivingPopulation()
		self.getEligableMates()

		if len(self.deadPop) == len(self.population):
			logging.critical("Everyone's dead!")
			return False
		else:
			for schmoobleID in self.livingPop:
				self.population[schmoobleID].tick()

		if len(self.possibleMates) >= 2:
			for i in range(0,len(self.possibleMates)):
				for j in range(i+1,len(self.possibleMates)):
					critter1 = self.possibleMates[i]
					critter2 = self.possibleMates[j]
					if self.population[critter1].canSee(self.population[critter2].turtle.pos()) and self.population[critter2].canSee(self.population[critter1].turtle.pos()):
						if self.population[critter1].destinationType != "mate" and self.population[critter2].destinationType != "mate":
							logging.info("Schmoobles #"+str(critter1)+" & "+str(critter2)+" have noticed each other!")
							midpoint = findMidpoint(self.population[critter1].turtle.pos(),self.population[critter2].turtle.pos())
							self.population[critter1].destination = midpoint
							self.population[critter2].destination = midpoint
							self.population[critter1].state = 2
							self.population[critter2].state = 2
							self.population[critter1].destinationType = "mate"
							self.population[critter2].destinationType = "mate"


		waitingSchmoobles = self.getWaitingToMate()
		if len(waitingSchmoobles) >= 2:
			for i in range(len(waitingSchmoobles)):
				for j in range(i+1,len(waitingSchmoobles)):
					critter1 = self.population[waitingSchmoobles[i]]
					critter2 = self.population[waitingSchmoobles[j]]
					if critter1.turtle.distance(critter2.turtle.pos()) < 5:
						self.mate(critter1.id,critter2.id)


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
			if self.population[popID].mateable == True and self.population[popID].cooldownCounter == 0:
				self.possibleMates.append(popID)

	def getWaitingToMate(self):
		waitingToMate = []
		for popID in self.population.keys():
			if self.population[popID].state == 4:
				waitingToMate.append(popID)
		return waitingToMate

	def mate(self,parent1ID,parent2ID):
		parent1 = self.population[parent1ID]
		parent2 = self.population[parent2ID]

		parent1.creatureInfo()
		parent2.creatureInfo()

		outputSchmooble = Schmooble(len(self.population)+1,parent1.turtle.pos())

		mutationRate = abs(((parent1.mutationRate + parent2.mutationRate) / 2) + random.uniform(-0.1,0.1))

		outputSchmooble.speed = round((parent1.speed + (parent2.speed)/2) * mutationRate)
		outputSchmooble.turtle.speed = mapRange(outputSchmooble.speed,1,100,0,10)
		outputSchmooble.energy = round((parent1.energy * parent1.energyTransferToChild) + (parent2.energy * parent2.energyTransferToChild) * mutationRate)
		parent1.energy = round(parent1.energy - (parent1.energy * parent1.energyTransferToChild))
		parent2.energy = round(parent2.energy - (parent2.energy * parent2.energyTransferToChild))
		outputSchmooble.matingEnergyThreshold = round(((parent1.matingEnergyThreshold + parent2.matingEnergyThreshold) / 2) * mutationRate)
		outputSchmooble.energyTransferToChild = round(((parent1.energyTransferToChild + parent2.energyTransferToChild) / 2) * mutationRate,2)
		if outputSchmooble.energyTransferToChild > 1:
			outputSchmooble.energyTransferToChild = 1
		outputSchmooble.sightRange = round(((parent1.sightRange + parent2.sightRange)/2)*mutationRate)
		outputSchmooble.boredomLimit = round(((parent1.boredomLimit + parent2.boredomLimit)/2)*mutationRate)+1
		outputSchmooble.mutationRate = round(mutationRate,2)

		parent1.state = 1
		parent2.state = 1
		parent1.destinationType = None
		parent2.destinationType = None

		parent1.cooldownCounter = parent1.matingCooldown
		parent2.cooldownCounter = parent2.matingCooldown

		print("\nOffspring creature info")
		outputSchmooble.creatureInfo()
		# tmp = input("\n\nGeneration complete...")

		self.population[outputSchmooble.id] = outputSchmooble
