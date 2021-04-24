import numpy as np
from random import choice, normalvariate, randint

directions = ["up","down","left","right"]

class Entity():
	def __init__(self):
		self.position = (None, None)

class Animal(Entity):

	def __init__(self, mean=2, std=1):
		# Animal Properties
		self.speed = normalvariate(mean, std)
		self.reproductive_drive = normalvariate(mean, std)
		self.sight_radius = normalvariate(mean, std)
		self.hunger = 0
		self.last_direction = choice(directions)

		# Spatial properties
		super(Entity, self).__init__()

class Fox(Animal):
	def __init__(self, *args, **kwargs):
		self.identifier = 3
		super(Animal, self).__init__(*args, **kwargs)

class Rabbit(Animal):
	def __init__(self, *args, **kwargs):
		self.identifier = 2
		super(Animal, self).__init__(*args, **kwargs)

class Carrot(Entity):
	def __init__(self, *args, **kwargs):
		self.identifier = 1
		super(Entity, self).__init__()
