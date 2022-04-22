import random
import turtle
import logging

logging.basicConfig(level=logging.WARNING)

myscreen = turtle.Screen()
myscreen.bgcolor('light green')
myscreen.setup(0.8,0.8)
myscreen.title('Schmoobles')

from foodlist import foodList
from census import Census

def mainLoop(initialPopulation):
	logging.error("Starting")
	tickNumber = 0
	highestPopulation = initialPopulation
	census = Census(initialPopulation)
	running = True
	while running:
		tickNumber = tickNumber + 1
		logging.error("Tick: "+str(tickNumber)+" Living population: "+str(len(census.livingPop))+" Total Offspring: "+str(len(census.population.keys())-initialPopulation))
		running = census.step()
		if len(census.livingPop) > highestPopulation:
			highestPopulation = len(census.livingPop)
		if running == False:
			print("\n\nSummary\nTick #: "+str(tickNumber)+" Highest population: "+str(len(census.livingPop))+" Total Offspring: "+str(len(census.population.keys())-initialPopulation))




mainLoop(8)
turtle.done()		