"""
Authors: Jonah Post, Mio Poortvliet

Simulate a population of static food and animals. An example of valid settings:
============================================================================
settings = {
    "map_size": map_size,
    "animals": ["fox", "rabbit"],
    "foods": ["carrot", ],
    "fox": int(fox_density * map_size ** 2),
    "rabbit": int(rabbit_density * map_size ** 2),
    "carrot": int(carrot_density * map_size ** 2),
    "food_spawn_chance": {"carrot": 0.0004},
    "stop_at_zero": True,
    "animal_std": 0.2,
    "avoid_extinction": False
}
============================================================================

Now the animals need to be initialized with some values too. Looks like:
============================================================================
fox_inits = {
    "mean_speed": 3,
    "mean_reproductive_drive": 200,
    "mean_sight_radius": 5,
    "mean_max_hunger": 1900,
    "mean_max_age": 10000
}
rabbit_inits = {
    "mean_speed": 2,
    "mean_reproductive_drive": 30,
    "mean_sight_radius": 10,
    "mean_max_hunger": 400,
    "mean_max_age": 4000,
    "nutritional_value": 500
}
============================================================================

Finally, we need to pass all animals and food to the simulation. Do so by creating dicts
============================================================================

animal_objects = {
		"fox": {"object": Fox, "init": fox_inits},
		"rabbit": {"object": Rabbit, "init": rabbit_inits}
	}
food_objects = {
		"carrot": Carrot
	}
============================================================================
"""

import numpy as np
from random import randint, sample
from itertools import product
from src.utils import nn_array, process_statistics
from src.utils_ising_model import choice as fastchoice
from typing import Union, Tuple


class AnimalEvolution:
	def __init__(self, settings: dict, food_objects: dict, animal_objects: dict) -> None:
		self.settings = settings
		self.animal_objects = animal_objects
		self.food_objects = food_objects

		# Split these because food does not update
		self.animal_map = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=object)
		self.food_map = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=object)

		animals, foods = self.spawn_entities()

		# Generate all possible coordinates
		all_coordinates = list(product(range(self.settings["map_size"]), range(self.settings["map_size"])))

		# Position animals
		positions = sample(all_coordinates,len(animals))
		self.position_entities_on_map(animals, self.animal_map, positions=positions)

		# Position food
		positions = sample(all_coordinates,len(foods))
		self.position_entities_on_map(foods, self.food_map, positions=positions)

	def spawn_entities(self) -> Tuple[list, list]:
		"""Call this in the init to create the entities to place in the field."""
		animals = []
		foods = []

		for animal in self.settings["animals"]:
			# self.settings[animal] is the number of animals of that type to be initialized
			for i in range(self.settings[animal]):
				# add them to the list to place later
				animals.append(
					self.animal_objects[animal]["object"]( # Find the right object in the dict.
						std=self.settings["animal_std"],
						**self.animal_objects[animal]["init"] # How to initialize this animal? In animal objects.
					)
				)
				# Randomly distribute the age, pick the previously appended animal.
				animals[-1].age = randint(0, animals[-1].max_age - 1) # -1 so it does not instantly die

		# Same but food
		for food in self.settings["foods"]:
			for i in range(self.settings[food]):
				foods.append(self.food_objects[food]())

		return animals, foods

	def spawn_food(self) -> None:
		"""Spawn food on random empty spots"""
		for food_id in self.food_objects.keys():
			zero_idx = np.argwhere(self.food_map == 0)
			for coords in zero_idx:
				if fastchoice(self.settings["food_spawn_chance"][food_id]):
					coords = tuple(coords)

					# print(self.foods[-1], self.map[coords])
					self.food_map[coords] = self.food_objects[food_id]()
					self.food_map[coords].position = coords
			# print(self.map[coords])

	def position_entities_on_map(self, entities: list, map: np.ndarray, positions: list) -> None:
		"""Position entities at positions. If no position is given, randomly distributed positions will be chosen"""
		for entity, position in zip(entities, positions):
			# Give the entity a position and place it on the grid at that position.
			# This can go very wrong if we're not careful!
			entity.position = position
			map[entity.position] = entity

	def move_animal(self, animal, new_pos: tuple, direction: int) -> None:
		"""Update map and animal to reflect the movement to new position.
		Does not check if spot is available."""
		# Update map
		# Remove animal from old position
		self.animal_map[animal.position] = 0
		# Move it to new position
		animal.position = new_pos
		self.animal_map[animal.position] = animal

		# Update animal properties
		animal.last_direction = direction
		animal.hunger += 1
		animal.steps_taken += 1

	def check_occupation_at_position(self, pos) -> bool:
		"""Is pos occupied?"""
		if self.animal_map[pos] == 0:
			return True
		else:
			return False

	def new_coords(self, position: tuple, direction: int) -> Tuple[int, int]:
		"""Given a position and direction, return the coordinates of the position in the direction."""
		if direction == 0:  # up
			return position[0], (position[1] + 1) % self.settings["map_size"]
		elif direction == 1:  # right
			return (position[0] + 1) % self.settings["map_size"], position[1]
		elif direction == 2:  # down
			return position[0], (position[1] - 1) % self.settings["map_size"]
		elif direction == 3:  # left
			return (position[0] - 1) % self.settings["map_size"], position[1]
		else:
			print("direction = ", direction)

	def attempt_to_move_animal(self, animal) -> None:
		"""Move the animal if possible, eat animal in tile where it wants to move to if that is allowed."""
		preferred_direction = animal.pathfinding(self.animal_map, self.food_map)  # where does animal want to go

		for direction in np.mod(preferred_direction + np.array([0, 1, 3, 2]), 4):
			new_pos = self.new_coords(animal.position, direction)

			# Can we eat a juicy rabbit?
			if animal.eat_possible(self.animal_map[new_pos]):
				#print(f"{animal} is eating {self.animal_map[new_pos]}")
				animal.eat(self.animal_map[new_pos])
				#print(f"{animal} just ate")
				#print(f"removing {self.animal_map[new_pos]}")
				self.delete_entity(self.animal_map[new_pos], self.animal_map)
			# Now the move will be valid!

			if self.check_occupation_at_position(new_pos):
				#print(f"moving this guy: {animal}")
				self.move_animal(animal, new_pos, direction)
				#print(self.animal_map[new_pos])
				# break from the direction loop
				break

	def adjacent_interactions(self, animal) -> None:
		"""Check for interactions with neighbouring animals, leading to a sex attempt"""
		neighbours_idx = np.mod(np.array(animal.position) + nn_array, self.settings["map_size"])

		for neighbour_idx in neighbours_idx:
			neighbour_pos = tuple(neighbour_idx) # there is a difference between a tuple and an array when slicing/indexing
			neighbour_animal = self.animal_map[neighbour_pos]

			if neighbour_animal == 0:
				# Nothing on the next tile
				pass

			else:
				if animal.interact(neighbour_animal):
					self.sex_attempt(type(animal), animal.position, animal, neighbour_animal)

	def sex_attempt(self, animal_type, parent_postion: tuple, parent1, parent2) -> None:
		"""Attempt to place a new animal of animal_type on the map if appropriate.
		Animals are genderless."""
		if not (parent1.libido_check() and parent2.libido_check()):
			# Consent is important
			parent1.libido -= 5
			return

		else:
			for direction in range(4):
				# print(direction)
				baby_position = self.new_coords(parent_postion, direction)

				if self.animal_map[baby_position] == 0:
					# print("Baby is born!", mom.position, dad.position)

					# We need this because not everything is inherited.
					# We check if self.animal_objects[animal_name]["object"] is of type animal_type
					# Using this we can access self.animal_objects[animal_name]["init"]["mean_max_hunger"]
					for animal_name in self.animal_objects.keys(): # [rabbit, fox]
						if self.animal_objects[animal_name]["object"].__name__ == animal_type.__name__:
							break # break to lock in the correct animal_name

					# Give child mean of parents (with noise controlled by std)
					newanimal = animal_type(
						mean_speed=(parent1.speed + parent2.speed) / 2,
						mean_reproductive_drive=(parent1.reproductive_drive + parent2.reproductive_drive) / 2,
						mean_sight_radius=(parent1.sight_radius + parent2.sight_radius) / 2,
						mean_max_hunger=self.animal_objects[animal_name]["init"]["mean_max_hunger"], # mean_max_hunger just diverges but that is unrealistic
						mean_max_age=(parent1.max_age + parent2.max_age) / 2,
						std=self.settings["animal_std"],
						nutritional_value=(parent1.nutritional_value + parent2.nutritional_value) / 2
					)

					self.position_entities_on_map(entities=[newanimal], map=self.animal_map, positions=[baby_position])

					# Food is conserved in an interaction
					for parent in (parent1, parent2):
						parent.hunger += int((newanimal.max_hunger - newanimal.hunger) / 2)
						parent.libido = 0

					# Animals had fun, break is over
					break


	def step(self) -> bool:
		"""One step in a cycle, a step is a turn for every animal. Animals can have multiple steps in a cycle"""
		animals = self.animals()
		exhausted_animals = 0

		for animal in animals:
			if animal.exists:
				# Animal is still alive and may move
				if animal.steps_taken < animal.speed:
					self.attempt_to_move_animal(animal)

					# See if there is interaction with neighbours
					self.adjacent_interactions(animal)

					# not elif, animal can move and eat in the same step
					if not self.food_map[animal.position] == 0:
						if animal.eat_possible(self.food_map[animal.position]):
							animal.eat(self.food_map[animal.position])
							self.delete_entity(self.food_map[animal.position], self.food_map)

					if animal.hunger >= animal.max_hunger:
						self.delete_entity(animal, self.animal_map)
						exhausted_animals-=1


				else:
					#animal is out of steps
					exhausted_animals+=1

		return len(animals) == exhausted_animals

	def cycle(self, maxsteps=50) -> None:
		"""One larger unit of interactions. Letting all animals take all their available steps."""
		for step in range(maxsteps):
			if self.step():
				break

		self.cycle_reset()

	def cycle_reset(self) -> None:
		"""Increment and reset internal counters"""
		for animal in self.animals():
			animal.hunger += 1
			animal.steps_taken = 0
			animal.libido += 1
			animal.age += 1
			# animal old?
			if animal.age > animal.max_age:
				self.delete_entity(animal, self.animal_map)

		self.spawn_food()

	def run_cycles(self, maxcycles=10, printskip=15) -> Tuple[np.ndarray, np.ndarray]:
		""""""
		# Initialize statistics arrays
		self.population = np.zeros(shape=(maxcycles, len(self.animal_objects) + len(self.food_objects)))
		self.animal_genes = np.zeros((maxcycles, len(self.animal_objects), 9, 2))

		for cycle in range(maxcycles):
			# cycle is the previous cycle, we started at 0
			if cycle % printskip == 0: # Print what cycle we are calculating
				print(cycle)

			if np.any(self.population[cycle-1, 1::] <= 0) and cycle != 0: # check if there are less than two animals of any kind.
				# break simulation if there is no future
				if self.settings["stop_at_zero"]:
					# There are not enough animals alive
					print("Premature ending")
					break

				# Otherwise force at least two animals of every kind
				elif self.settings["avoid_extinction"]:
					for i, animal_key in enumerate(self.animal_objects.keys()):
						# population[::,0] are carrots
						# self.settings[animal_key] are the initial number of animals
						# This allows you to initialize with 0 of an animal.
						# The i+1 comes from the fact that there are carrot stats at 0
						if self.population[cycle-1, i+1] <= 1 and self.settings[animal_key] > self.population[cycle-1, i+1]:
							print(f"{animal_key} is spawned!")
							animal = self.animal_objects[animal_key]["object"](
								**self.animal_objects[animal_key]["init"],
								std=self.settings["animal_std"]
							)
							zero_idx = np.argwhere(self.animal_map == 0)
							position = zero_idx[randint(0, zero_idx.shape[0] - 1), ::]
							self.position_entities_on_map(entities=[animal], positions=[tuple(position)], map=self.animal_map)

			self.cycle()
			self.write_stats(cycle)

		return self.population[:cycle-1, ::], self.animal_genes[:cycle-1, ::, ::, ::]

	def delete_entity(self, entity, map:np.ndarray) -> None:
		"""Remove entity from the map and flag it to not be interacted with."""
		map[entity.position] = 0
		entity.exists = False
		# del entity # this can be commented out because it is not in the array.

	def animals(self) -> np.ndarray:
		"""Return a list of all animals on the board"""
		return self.animal_map[self.animal_map.nonzero()]

	def foods(self) -> np.ndarray:
		"""Return a list of all foods on the board"""
		return self.food_map[self.food_map.nonzero()]

	def write_stats(self, cycle: int) -> None:
		"""Write the statistics of the current board to the statistics array at index cycle"""
		all_animals_on_map = self.animals()
		# Animal ID, properties+Animal number,
		animal_genes = np.zeros((len(all_animals_on_map), 10))

		for food in self.foods():
			for i, obj in enumerate(self.food_objects.values()):
				if isinstance(food, obj):
					self.population[cycle, i] += 1

		for k, animal in enumerate(all_animals_on_map):
			for j, animal_id in enumerate(self.animal_objects.values()):
				if isinstance(animal, animal_id["object"]):
					animal_properties = np.array([
						animal.speed,
						animal.sight_radius,
						animal.reproductive_drive,
						animal.max_hunger,
						animal.max_age,
						animal.age,
						animal.hunger,
						animal.libido,
						animal.steps_taken
					])

					# i is position of last food stat, not a bug but yes sloppy programming.
					self.population[cycle, len(self.food_objects) + j] += 1
					animal_genes[k, :-1:] = animal_properties
					animal_genes[k, -1] = j

					break  # We found the right animal, break inner loop

		process_statistics(self.animal_genes[cycle, ::, ::, ::], animal_genes, len(self.animal_objects))

	def printable_map(self) -> np.ndarray:
		"""Returns a printable map of the field. Can be used directly in np.imshow()"""
		map_identifier = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=np.int)

		for entity in self.animals():
			map_identifier[entity.position] += entity.identifier

		for entity in self.foods():
			map_identifier[entity.position] += entity.identifier

		return map_identifier