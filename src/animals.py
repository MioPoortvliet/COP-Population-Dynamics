import numpy as np
from random import choice, normalvariate, randint

directions = ["up","down","left","right"]
class Animal:

	def __init__(self, map_size, mean=2, std=1):
		# Animal Properties
		self.speed = normalvariate(mean, std).astype(int)
		self.reproductive_drive = normalvariate(mean, std).astype(int)
		self.sight_radius = normalvariate(mean, std).astype(int)
		self.hunger = 0
		self.last_direction = choice(directions)

		# Spatial properties
		self.position = randint(map_size)

class Fox(Animal):
	pass

class Rabit(Animal):
	pass