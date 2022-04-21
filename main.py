import random
import turtle

myscreen = turtle.Screen()
myscreen.bgcolor('light green')
myscreen.setup(0.8,0.8)
myscreen.title('Schmoobles')

from foodlist import foodList
from census import Census

def mainLoop(initialPopulation):
	census = Census(initialPopulation)
	running = True
	while running: 
		running = census.step()




mainLoop(2)
turtle.done()