import numpy as np
from random import choice, gauss, randint
from src.utils import minimum_int, direction_from_difference, nonzero_idx
from numba import njit


class Entity():
	def __init__(self, nutritional_value=15):
		self.position = (None, None)
		self.eaten = False # Flag variable
		self.nutritional_value = nutritional_value

	def gets_eaten(self):
		#print("got_eaten")
		self.eaten = True


class Animal(Entity):

	def __init__(self, mean_speed, mean_reproductive_drive, mean_sight_radius, std, mean_max_hunger, mean_max_age, *args, **kwargs):
		# Spatial properties
		super(Animal, self).__init__(*args, **kwargs)

		# Animal Properties
		self.speed = minimum_int(gauss(mean_speed, std))
		self.reproductive_drive = minimum_int(gauss(mean_reproductive_drive, std))
		self.sight_radius = minimum_int(gauss(mean_sight_radius, std))
		self.max_hunger = minimum_int(gauss(mean_max_hunger, std*3))
		self.last_direction = randint(0, 3)
		self.direction_randomness = 0.4
		self.max_age = minimum_int(gauss(mean_max_age, std*3))

		# For keeping track of stuff
		self.steps_taken = 0
		self.hunger = self.max_hunger / 2
		self.libido = 0
		self.age = 0

	def eat(self, other):
		self.hunger = max((0, self.hunger-other.nutritional_value))
		#print("chomp")

	def food_check(self, treshold=0.4):
		"""Returns true if the animal is hungry and false if the animal is not hungry"""
		if self.hunger > (self.max_hunger * treshold):
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
		self.identifier = 4
		super(Fox, self).__init__(*args, **kwargs)

	def pathfinding(self, animal_map, food_map):
		animals_in_sight, sorted_animals_idx = pathfinding_check(self.position, self.sight_radius, animal_map.astype(np.bool_))

		# Check if there are entities within sight radius
		if animals_in_sight > 0:
			# Yes, interact possibly?
			for other_idx in sorted_animals_idx:
				other = animal_map[tuple(other_idx)]

				if isinstance(other, Rabbit) and self.food_check():
					difference = other_idx - np.array(self.position)
					# yes, yummy
					return direction_from_difference(difference)

				elif isinstance(other, Fox) and not self.food_check() and self.libido_check():
					difference = other_idx - np.array(self.position)
					#print("let's fuck", animal.position, other.position)
					return direction_from_difference(difference)

		# No, move randomly
		return round(gauss(self.last_direction, self.direction_randomness)) % 4


	def interact(self, neighbour_animal):
		# animal is fox
		# next to rabbit
		if isinstance(neighbour_animal, Rabbit) and self.food_check():
			# print("Rabit gets eaten")
			neighbour_animal.gets_eaten()
			self.eat(neighbour_animal)
			return neighbour_animal, False # Deleted animal, Make baby?
		# next to Fox
		elif isinstance(neighbour_animal, Fox) and (not self.food_check()) and (not neighbour_animal.food_check()) and self.libido_check():
			return None, True # Deleted animal, Make baby?

		else:
			return None, False # Deleted animal, Make baby?

	def food_interaction(self, food_map):
		return False



class Rabbit(Animal):
	def __init__(self, *args, **kwargs):
		self.identifier = 2
		super(Rabbit, self).__init__(*args, **kwargs)

	def pathfinding(self, animal_map, food_map):
		#animals_in_sight, sorted_animals_idx = pathfinding_check(self, animal_map)
		#foods_in_sight, sorted_foods_idx = pathfinding_check(self, food_map)
		animals_in_sight, sorted_animals_idx = pathfinding_check(self.position, self.sight_radius, animal_map.astype(np.bool_))
		foods_in_sight, sorted_foods_idx = pathfinding_check(self.position, self.sight_radius, food_map.astype(np.bool_))

		# Check if there are entities within sight radius
		if animals_in_sight > 0:
			# Yes, interact possibly?
			for other_idx in sorted_animals_idx:
				other = animal_map[tuple(other_idx)]

				if isinstance(other, Fox):
					reverse_difference = np.array(self.position)- other_idx
					# Fuck, run
					return direction_from_difference(reverse_difference)

				elif isinstance(other, Rabbit) and not self.food_check() and self.libido_check():
					difference = other_idx - np.array(self.position)
					#print("let's fuck", animal.position, other.position)
					return direction_from_difference(difference)


			# Nothing in priorities?
			#return round(gauss(self.last_direction, self.direction_randomness)) % 4
		if foods_in_sight > 0 and self.food_check():
			for other_idx in sorted_foods_idx:
				other = food_map[tuple(other_idx)]
				if isinstance(other, Carrot):
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
			return self, False # Deleted animal, Make baby?
		# next to rabbit
		elif isinstance(neighbour_animal, Rabbit) and (not self.food_check()) and (not neighbour_animal.food_check()) and self.libido_check():
			return None, True # Deleted animal, Make baby?
		# next to carrot
		else:
			return None, False # Deleted animal, Make baby?

	def food_interaction(self, food_map):
		if not food_map[self.position] == 0:
			self.eat(food_map[self.position])
			return True
		else:
			return False

class Carrot(Entity):
	def __init__(self, *args, **kwargs):
		self.identifier = 1
		super(Carrot, self).__init__()
		self.nutritional_value = 15

#@njit
def pathfinding_check(animal_position, animal_sight_radius, entity_map):
	other_idx = nonzero_idx(entity_map.astype(np.bool_), *animal_position)
	if other_idx is None:
		return 0, None

	#nearest = other_idx[((other_idx - [coordinates[0],coordinates[1]])**2).sum(1).argmin()]
	differences = np.sum((other_idx - np.array(animal_position))**2, axis=1) <= animal_sight_radius**2

	# Are there entities within range?
	n = np.sum(differences)
	if n > 0:
		if n < other_idx.shape[0]:
			# Only sort the first n
			nearest_sorted = other_idx[np.argpartition(((other_idx - [animal_position[0], animal_position[1]]) ** 2).sum(1), kth=n)][:n]
		elif n > 1:
			# Sort all n
			nearest_sorted = np.sort(other_idx)
		else:
			nearest_sorted = other_idx

		return n, nearest_sorted
	else:
		return 0, None

