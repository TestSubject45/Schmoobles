import random
import turtle
from schmooble import Schmooble, foodList, mapRange

startPop = 5

myscreen = turtle.Screen()

myscreen.bgcolor('light green')
myscreen.setup(0.7,0.7)
myscreen.title('Turtle Game')


turtleList = []
schmoobleList = []
for i in range(0,startPop):
	schmoobleList.append(Schmooble())


running = True
while running:
	deadPop = 0
	for i in range(0,startPop):
		print("\n\nSchmooble #",i)
		schmoobleList[i].update()
		if schmoobleList[i].state == 4:
			deadPop = deadPop + 1
	print("len of schmoobleList",len(schmoobleList))
	if deadPop == len(schmoobleList):
		running = False
	print("Total dead population:",deadPop)		

input("All population has died...")

turtle.done()