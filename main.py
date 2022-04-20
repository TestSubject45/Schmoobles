import random
import turtle

myscreen = turtle.Screen()

myscreen.bgcolor('light green')
myscreen.setup(0.8,0.8)
myscreen.title('Schmoobles')

from foodlist import foodList

from schmooble import Schmooble

firstSchmooble = Schmooble(1,(-5,15))

tmp = input("...")

turtle.done()