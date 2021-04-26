import numpy as np
from random import sample, gauss, choice, randint
from src.visualization import map_graph
from src.animals import Fox, Rabbit, Carrot, Animal
from itertools import product
from src.utils import nearest_nonzero_idx, nonzero_idx

"""----NOTES----
It seems like it is a problem that carrots take up a tile
We should separate food from animals
Write program again lol more structured pathfinding algorithm, etc

Bunnies keep dying or exploding in population size! No equilibrium to be found :(
Why? Map seems to be too large and rabbits don't run into each other -> no kids
Maybe even separated by carrots! Carrots should be transparent.

Pathfinding should be better. 
Priorities:
Run from foxes (implement later)
If hunger within 20% of max hunger, search for food
Else search for mate
"""



class AnimalEvolution():
	def __init__(self, settings, food_objects, animal_objects):
		self.settings = settings
		self.animal_objects = animal_objects
		self.food_objects = food_objects

		# Split these because food does not update
		self.animal_map = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=object)
		self.food_map = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=object)


		self.position_entities(self.spawn_entities())

		self.exhausted_animals = 0

		self.nn_array = np.concatenate([np.eye(2, dtype=int), -np.eye(2, dtype=int)])


	def animals(self):
		return self.animal_map[self.animal_map.nonzero()]

	def foods(self):
		return self.food_map[self.food_map.nonzero()]


	def spawn_entities(self):
		animals = []
		foods = []
		for animal in self.settings["animals"]:
			for i in range(self.settings[animal]):
				animals.append(self.animal_objects[animal]["object"](**self.animal_objects[animal]["init"]))
				animals[-1].age = randint(0, animals[-1].max_age-1)
				print(animals[-1].age)

		for food in self.settings["foods"]:
			for i in range(self.settings[food]):
				foods.append(self.food_objects[food]())

		return animals + foods


	def position_entities(self, entities, positions=None):
		N_entities = len(entities)

		if positions == None:
			# Generate coordinates
			positions = sample(list(product(range(self.settings["map_size"]), range(self.settings["map_size"]))), N_entities)

		for entity, position in zip(entities, positions):
			entity.position = position

			if isinstance(entity, Animal):
				self.animal_map[entity.position] = entity
			else:
				self.food_map[entity.position] = entity



	def printable_map(self):
		map_identifier = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=np.int)

		for entity in self.animals():
			map_identifier[entity.position] += entity.identifier

		for entity in self.foods():
			map_identifier[entity.position] += entity.identifier*10

		return map_identifier


	def step_forward(self):
		self.animal_deletion_list = set()
		self.food_deletion_list = set()
		for animal in self.animals():
			# Animal old?
			if animal.age > animal.max_age:
				self.animal_deletion_list.add(animal)
				#print("Animal dies of age")
			# Animal starves?
			elif animal.hunger > animal.max_hunger:
				self.animal_deletion_list.add(animal)
				#print("Animal starves")
			else:
				# May animal move?
				if animal.steps_taken < animal.speed:
					# Check for interactions
					if not self.food_map[animal.position] == 0:
						animal.eat(self.food_map[animal.position])
						self.food_map[animal.position] = 0
					if not self.nearest_neighbour_intereactions(animal):
						# If the animal had an interaction it is not allowed to play a turn
						direction = animal.pathfinding(self.animal_map, self.food_map)#self.pathfinding(animal)
						self.move_animal(animal, direction)

				# If we have flagged the animal before do nothing
				elif animal.steps_taken > animal.speed:
					pass

				else:
					# Use steps taken as flag that we added it to the exhausted animals list
					animal.steps_taken += 1
					self.exhausted_animals += 1

	def cycle(self, maxstep = 50):
		"""A cycle is moving all animals until they can't anymore."""
		for step in range(maxstep):
			if self.exhausted_animals == self.animal_map.nonzero()[0].size:
				break
			else:
				self.step_forward()
				self.delete_animals()

	def run_cycles(self, maxcycles=10):
		self.stats = np.zeros(shape=(maxcycles+1, len(self.animal_objects)+len(self.food_objects)))
		self.write_stats(0)

		#map_graph(self.printable_map())
		for cycle in range(maxcycles):
			print(cycle)
			#print(len(self.animals), len(self.foods))
			if (
					self.animal_map.nonzero()[0].size <= 1
					or (np.any(self.stats[cycle-1,1::] == 0)
						and cycle != 0
						and self.settings["stop_at_zero"])
			):
				print("Premature ending")
				break
			self.cycle()
			self.reset_animals()
			self.spawn_food()
			self.write_stats(cycle+1)

			assert np.sum(self.stats[cycle, ::]) <= self.settings["map_size"]**2

		return self.stats[:cycle+1,::]

	def write_stats(self, cycle):
		N_foods = len(self.food_objects)

		for food in self.foods():
			for i, obj in enumerate(self.food_objects.values()):
				if isinstance(food, obj):
					self.stats[cycle, i] += 1

		for animal in self.animals():
			for i, animal_id in enumerate(self.animal_objects.values()):
				if isinstance(animal, animal_id["object"]):
					self.stats[cycle, i+N_foods] += 1


	def spawn_food(self):
		for food_id in self.food_objects.keys():
			zero_idx = np.argwhere(self.food_map == 0)
			for coords in zero_idx:
				if np.random.choice(
						[False, True],
						p=[1-self.settings["food_spawn_chance"][food_id],
						   self.settings["food_spawn_chance"][food_id]]
				):
					coords = tuple(coords)

					#print(self.foods[-1], self.map[coords])
					self.food_map[coords] = self.food_objects[food_id]()
					self.food_map[coords].position = coords
					#print(self.map[coords])


	def reset_animals(self):
		for animal in self.animals():
			animal.steps_taken = 0
			animal.libido += 1
			animal.hunger += 1
			animal.age += 1

		self.exhausted_animals = 0


	def delete_animals(self):
		for id in self.animal_deletion_list:
			# Make sure to remove it from the map too!
			self.animal_map[id.position] = 0

		for id in self.food_deletion_list:
			# Make sure to remove it from the map too!
			self.food_map[id.position] = 0


	def nearest_neighbour_intereactions(self, animal):
		neighbours = np.mod(np.array(animal.position) + self.nn_array, self.settings["map_size"])

		for neighbour_id in neighbours:
			neighbour_id = tuple(neighbour_id)
			neighbour_animal = self.animal_map[neighbour_id]

			if neighbour_animal == 0:
				# Nothing on the next tile
				pass

			else:
				animal_deletion, birth = animal.interact(neighbour_animal)

				if not animal_deletion is None:
					self.animal_deletion_list.add(animal_deletion)

				if birth:
					self.birth(type(animal), animal.position, animal, neighbour_animal)


	def birth(self, animal, postion, mom, dad):
		#print("attempting to fuck")
		if not (mom.libido_check() and dad.libido_check()):
			# Consent is important
			print("not horny", dad.libido, dad.reproductive_drive)
			mom.libido -= 5
			return
		else:
			for direction in range(4):
				#print(direction)
				coords = self.new_coords(postion, direction)

				if self.animal_map[coords] == 0:

					print("Baby is born!", mom.position, dad.position)
					mean_speed = (mom.speed + dad.speed ) / 2
					mean_reproductive_drive = (mom.reproductive_drive + dad.reproductive_drive ) / 2

					newanimal = animal(mean_speed, mean_reproductive_drive)

					self.position_entities([newanimal], [coords])

					#print(mom.hunger)
					mom.hunger += int(newanimal.max_hunger / 2)
					dad.hunger += int(newanimal.max_hunger / 2)
					mom.libido = 0
					dad.libido = 0
					#print(mom.hunger)
					#print("breaking")
					break


	def move_animal(self, animal, direction, recursions = 0):
		new_pos = self.new_coords(animal.position, direction)
		if not self.animal_map[new_pos]:
			# Walking costs food
			animal.hunger += 1

			animal.last_direction = direction

			# Update map
			self.animal_map[animal.position] = 0
			self.animal_map[new_pos] = animal

			animal.position = new_pos
			animal.steps_taken += 1

		elif recursions < 4:
			animal.last_direction += choice([-1, 1])
			self.move_animal(animal, direction, recursions+1)

		else:
			pass

	def new_coords(self, position, direction):
		if direction == 0:
			return position[0] % self.settings["map_size"], (position[1] + 1) % self.settings["map_size"]
		elif direction == 1:
			return (position[0] + 1) % self.settings["map_size"], position[1] % self.settings["map_size"]
		elif direction == 2:
			return position[0] % self.settings["map_size"], (position[1] - 1) % self.settings["map_size"]
		elif direction == 3:
			return (position[0] - 1) % self.settings["map_size"], position[1] % self.settings["map_size"]