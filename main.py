import random
import turtle
import logging

logging.basicConfig(level=logging.INFO)

myscreen = turtle.Screen()
myscreen.bgcolor('light green')
myscreen.setup(0.8,0.8)
myscreen.title('Schmoobles')

from foodlist import foodList
from census import Census

def mainLoop(initialPopulation):
	logging.error("Starting")
	tickNumber = 0
	census = Census(initialPopulation)
	running = True
	while running:
		tickNumber = tickNumber + 1
		logging.error("Tick: "+str(tickNumber)+" Living population: "+str(len(census.livingPop))+" Total Offspring: "+str(len(census.population.keys())-initialPopulation))
		running = census.step()




mainLoop(8)
turtle.done()		