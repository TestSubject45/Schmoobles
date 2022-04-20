import random
import turtle

from helpers import findMidpoint, mapRange, randomPosition, getDeadPopulation, getLivingPopulation

myscreen = turtle.Screen()
myscreen.bgcolor('light green')
myscreen.setup(0.8,0.8)
myscreen.title('Schmoobles')

from foodlist import foodList
from schmooble import Schmooble

def mainLoop(initialPopulation):
	population = {}
	while len(population) < initialPopulation:
		population[len(population)+1] = Schmooble(len(population)+1,randomPosition(100))

	running = True
	while running:
		deadPop = getDeadPopulation(population)
		livingPop = getLivingPopulation(population)
		if len(deadPop) == len(population):
			print("Everyone's dead!")
			running = False
		else:
			for schmoobleID in livingPop:
				population[schmoobleID].tick()




mainLoop(3)
turtle.done()