import random
import turtle
from helpers import randomPosition
foodDistanceLimit = 400
foodLimit = 15

class FoodList:
	def __init__(self,maxFoodDistanceLimit,foodLimit):
		self.list = []
		self.distanceLimit = maxFoodDistanceLimit
		self.pointLimit = foodLimit
		self.makeFoodList()

		self.turtle = turtle.Turtle()
		self.turtle.speed(0)
		self.turtle.ht()
		self.turtle.
		self.sinceReset = 0
		self.drawPoints()

	def makeFoodList(self):
		for i in range(0,self.pointLimit-1):
			self.addPoint()

	def addPoint(self):
		self.list.append(randomPosition(self.distanceLimit))

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