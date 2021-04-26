import numpy as np
from random import choice, gauss, randint
from src.utils import minimum_int, direction_from_difference, nonzero_idx


class Entity():
	def __init__(self):
		self.position = (None, None)
		self.eaten = False

	def gets_eaten(self):
		#print("got_eaten")
		self.eaten = True


class Animal(Entity):

	def __init__(self, mean_speed=2, mean_reproductive_drive=4, mean_sight_radius=1, std=1, max_hunger=25, max_age=20):
		# Spatial properties
		super(Animal, self).__init__()

		# Animal Properties
		self.speed = minimum_int(gauss(mean_speed, std))
		self.reproductive_drive = minimum_int(gauss(mean_reproductive_drive, std))
		self.sight_radius = minimum_int(gauss(mean_sight_radius, std))
		self.max_hunger = minimum_int(gauss(max_hunger, std*3))
		self.last_direction = randint(0, 3)
		self.direction_randomness = 0.4
		self.max_age = minimum_int(gauss(max_age, std*3))

		# For keeping track of stuff
		self.steps_taken = 0
		self.hunger = self.max_hunger / 2
		self.libido = 0
		self.age = 0

	def eat(self, nutritional_value=10):
		self.hunger = max((0, self.hunger-nutritional_value))
		print("chomp")

	def food_check(self, tresh=0.4):
		"""Returns true if the animal is hungry and false if the animal is not hungry"""
		if self.hunger > (self.max_hunger * tresh):
			return True
		else:
			return False

	def libido_check(self):
		if self.libido >= self.reproductive_drive:
			return True
		else:
			return False


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



def pathfinding(animal, map, other_idx, n = 0):

	coordinates = animal.position

	#nearest = other_idx[((other_idx - [coordinates[0],coordinates[1]])**2).sum(1).argmin()]
	nearest = other_idx[np.argpartition(((other_idx - [coordinates[0], coordinates[1]]) ** 2).sum(1), 2)[n]]
	difference = nearest - np.array(animal.position)

	if np.sum(difference ** 2) <= animal.sight_radius:

		# we see something!
		other = map[tuple(nearest)]
		# We are a rabbit
		if isinstance(animal, Rabbit):

			if isinstance(other, Fox):
				return direction_from_difference(-difference)

			elif isinstance(other, Rabbit) and not animal.food_check() and animal.libido_check():
				#print("let's fuck", animal.position, other.position)
				return direction_from_difference(difference)

			elif isinstance(other, Carrot) and animal.food_check(tresh=0.7):
				#print("i'm hungry", animal.position, other.position)
				return direction_from_difference(difference)

			else:
				return pathfinding(animal, map, other_idx, n = n + 1)

		# We are a fox
		elif isinstance(animal, Fox):
			if isinstance(other, Rabbit):
				return direction_from_difference(difference)

			elif isinstance(other, Fox) and animal.food_check():
				return direction_from_difference(difference)

			else:
				print("recursion fails?")
				return pathfinding(animal, map, other_idx, n = n + 1)

	else:
		return round(gauss(animal.last_direction, animal.direction_randomness)) % 4

