import random
import turtle

from helpers import findMidpoint, mapRange, randomPosition, getDeadPopulation, getLivingPopulation

myscreen = turtle.Screen()
myscreen.bgcolor('light green')
myscreen.setup(0.8,0.8)
myscreen.title('Schmoobles')

from foodlist import foodList
from schmooble import Census

def mainLoop(initialPopulation):
	census = Census(initialPopulation)
	running = True
	while running: 
		running = census.step()




mainLoop(1)
turtle.done()