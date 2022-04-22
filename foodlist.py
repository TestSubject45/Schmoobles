import random
import turtle
from helpers import randomPosition
import logging
foodDistanceLimit = 400
foodLimit = 75

class FoodList:
	def __init__(self,maxFoodDistanceLimit,foodLimit):
		self.list = []
		self.distanceLimit = maxFoodDistanceLimit
		self.pointLimit = foodLimit
		self.makeFoodList()

		self.turtle = turtle.Turtle()
		self.backgroundTurtle = turtle.Turtle()
		self.turtle.speed(0)
		self.turtle.ht()
		self.sinceReset = 0

		self.backgroundTurtle.ht()
		self.backgroundTurtle.speed(10)
		self.backgroundTurtle.penup()
		self.backgroundTurtle.goto(maxFoodDistanceLimit+75,maxFoodDistanceLimit+75)
		self.backgroundTurtle.pendown()
		self.backgroundTurtle.fillcolor("light goldenrod")
		self.backgroundTurtle.begin_fill()
		self.backgroundTurtle.setheading(270)
		self.backgroundTurtle.forward((maxFoodDistanceLimit * 2) + 150)
		self.backgroundTurtle.setheading(180)
		self.backgroundTurtle.forward((maxFoodDistanceLimit * 2) + 150)
		self.backgroundTurtle.setheading(90)
		self.backgroundTurtle.forward((maxFoodDistanceLimit * 2) + 150)
		self.backgroundTurtle.setheading(0)
		self.backgroundTurtle.forward((maxFoodDistanceLimit * 2) + 150)
		self.backgroundTurtle.end_fill()

		self.drawPoints()

	def makeFoodList(self):
		for i in range(0,self.pointLimit):
			self.addPoint()

	def addPoint(self):
		self.list.append(randomPosition(self.distanceLimit))

	def removePoint(self,point):
		self.sinceReset = self.sinceReset + 1
		# print(self.list)
		# print(point)
		self.turtle.penup()
		self.turtle.goto(point)
		self.turtle.dot(8,'light green')
		try:
			self.list.remove(point)
			self.addPoint()
		except ValueError:
			logging.debug("Point was already removed")

		if self.sinceReset > self.pointLimit:
			self.drawPoints()
			self.sinceReset = 0
		else:
			self.drawPoint(self.list[-1])

	def drawPoint(self,point):
		self.turtle.penup()
		self.turtle.goto(point)
		self.turtle.dot(10,'dark green')

	def drawPoints(self):
		self.turtle.clear()
		for i in range(0,len(self.list)):
			self.turtle.penup()
			self.turtle.goto(self.list[i])
			self.turtle.dot(10,'dark green')

foodList = FoodList(foodDistanceLimit,foodLimit)