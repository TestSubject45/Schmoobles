import random
import turtle
from schmooble import Schmooble, foodList, mapRange

popLimit = 2

myscreen = turtle.Screen()

myscreen.bgcolor('light green')
myscreen.setup(0.7,0.7)
myscreen.title('Turtle Game')


turtleList = []
schmoobleList = []
for i in range(0,popLimit):
	schmoobleList.append(Schmooble())

running = True
while running:
	for i in range(0,popLimit):
		schmoobleList[i].update()


turtle.done()