import numpy as np
from random import choice, gauss, randint
from src.utils import minimum_int, direction_from_difference


class Entity():
	def __init__(self):
		self.position = (None, None)
		self.eaten = False

	def gets_eaten(self):
		#print("got_eaten")
		self.eaten = True


class Animal(Entity):

	def __init__(self, mean_speed=2, mean_reproductive_drive=4, mean_sight_radius=1, std=1, max_hunger=25):
		# Spatial properties
		super(Animal, self).__init__()

		# Animal Properties
		self.speed = minimum_int(gauss(mean_speed, std))
		self.reproductive_drive = minimum_int(gauss(mean_reproductive_drive, std))
		self.sight_radius = minimum_int(gauss(mean_sight_radius, std))
		self.max_hunger = minimum_int(gauss(max_hunger, std*3))
		self.last_direction = randint(0, 3)
		self.direction_randomness = 0.4

		# For keeping track of stuff
		self.steps_taken = 0
		self.hunger = 0
		self.libido = 0

	def eat(self):
		self.hunger = 0


class Fox(Animal):
	def __init__(self, *args, **kwargs):
		self.identifier = 3
		super(Fox, self).__init__(*args, **kwargs)

class Rabbit(Animal):
	def __init__(self, *args, **kwargs):
		self.identifier = 2
		super(Rabbit, self).__init__(*args, **kwargs)


class Carrot(Entity):
	def __init__(self, *args, **kwargs):
		self.identifier = 1
		super(Carrot, self).__init__()



def pathfinding(animal, other, difference):
	# We are a rabbit
	if isinstance(animal, Rabbit):
		if isinstance(other, Rabbit):
			return direction_from_difference(difference)
		elif isinstance(other, Fox):
			return direction_from_difference(-difference)
		elif isinstance(other, Carrot):
			return direction_from_difference(difference)

	# We are a fox
	elif isinstance(animal, Fox):
		if isinstance(other, Rabbit):
			return direction_from_difference(difference)
		elif isinstance(other, Fox):
			return direction_from_difference(difference)

	else:
		return None



