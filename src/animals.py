import numpy as np
from random import choice, gauss, randint
from src.utils import minimum_int, direction_from_difference, nonzero_idx


class Entity():
	def __init__(self):
		self.position = (None, None)
		self.eaten = False
		self.nutritional_value = 15

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

	def eat(self, other):
		self.hunger = max((0, self.hunger-other.nutritional_value))
		#print("chomp")

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

	def pathfinding(self, entity_map):
		pass

	def interact(self, animal, food):
		# next to rabbit
		if isinstance(neighbour, Rabbit) and not neighbour.eaten:
			#print("Rabbit gets eaten")
			neighbour.gets_eaten()
			self.animal_deletion_list.add(neighbour)
			animal.eat(neighbour)
		elif isinstance(neighbour, Fox):
			self.birth(Fox, neighbour_id, animal, neighbour)



class Rabbit(Animal):
	def __init__(self, *args, **kwargs):
		self.identifier = 2
		super(Rabbit, self).__init__(*args, **kwargs)
		self.nutritional_value = 30

	def pathfinding(self, animal_map, food_map):
		animals_in_sight, sorted_animals_idx = pathfinding_check(self, animal_map)
		foods_in_sight, sorted_foods_idx = pathfinding_check(self, food_map)

		# Check if there are entities within sight radius
		if animals_in_sight > 0:
			# Yes, interact possibly?
			for other_idx in sorted_animals_idx:
				other = animal_map[tuple(other_idx)]

				if isinstance(other, Fox):
					difference = other_idx - np.array(self.position)
					# Fuck, run
					return direction_from_difference(-difference)

				elif isinstance(other, Rabbit) and not self.food_check() and self.libido_check():
					difference = other_idx - np.array(self.position)
					#print("let's fuck", animal.position, other.position)
					return direction_from_difference(difference)


			# Nothing in priorities?
			return round(gauss(self.last_direction, self.direction_randomness)) % 4
		if foods_in_sight > 0:
			for other_idx in sorted_foods_idx:
				other = food_map[tuple(other_idx)]
				if isinstance(other, Carrot) and self.food_check(tresh=0.95):
					difference = other_idx - np.array(self.position)
					#print("i'm hungry", animal.position, other.position)
					return direction_from_difference(difference)

		# No, move randomly
		return round(gauss(self.last_direction, self.direction_randomness)) % 4


	def interact(self, neighbour_animal):
		# animal is rabbit
		# next to fox
		if isinstance(neighbour_animal, Fox):
			# print("Rabit gets eaten")
			self.gets_eaten()
			neighbour_animal.eat(self)
			return self, False
		# next to rabbit
		elif isinstance(neighbour_animal, Rabbit) and (not self.food_check()) and (not neighbour_animal.food_check()) and self.libido_check():
			return None, True
		# next to carrot
		else:
			return None, False


class Carrot(Entity):
	def __init__(self, *args, **kwargs):
		self.identifier = 1
		super(Carrot, self).__init__()
		self.nutritional_value = 15


def pathfinding_check(animal, entity_map):
	other_idx = nonzero_idx(entity_map, *animal.position)
	if other_idx is None:
		return 0, None

	coordinates = animal.position

	#nearest = other_idx[((other_idx - [coordinates[0],coordinates[1]])**2).sum(1).argmin()]
	differences = np.sum((other_idx - np.array(animal.position))**2, axis=1) <= animal.sight_radius**2

	# Are there entities within range?
	n = np.sum(differences)
	if n > 0:
		if n < other_idx.shape[0]:
			# Only sort the first n
			nearest_sorted = other_idx[np.argpartition(((other_idx - [coordinates[0], coordinates[1]]) ** 2).sum(1), kth=n)][:n]
		elif n > 1:
			# Sort all n
			nearest_sorted = np.sort(other_idx)
		else:
			nearest_sorted = other_idx

		return n, nearest_sorted
	else:
		return 0, None

