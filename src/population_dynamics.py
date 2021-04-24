import numpy as np
from random import sample, gauss, choice
from src.visualization import map_graph
from src.animals import Fox, Rabbit, Carrot

class AnimalEvolution():
	def __init__(self, settings, food_objects, animal_objects):
		self.settings = settings
		self.animal_objects = animal_objects
		self.food_objects = food_objects

		# Split these because food does not update
		self.animals = []
		self.foods = []
		self.map = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=object)

		self.spawn_entities()
		self.position_entities(self.animals+self.foods)

		self.exhausted_animals = 0

		self.nn_array = np.concatenate([np.eye(2, dtype=int), -np.eye(2, dtype=int)])


	def spawn_entities(self):
		for animal in self.settings["animals"]:
			for i in range(self.settings[animal]):
				self.animals.append(self.animal_objects[animal]())

		for food in self.settings["foods"]:
			for i in range(self.settings[food]):
				self.foods.append(self.food_objects[food]())


	def position_entities(self, entities, positions=None):
		N_entities = len(entities)

		if positions == None:
			# Generate coordinates
			positions = list(zip(sample(range(self.settings["map_size"]), N_entities), sample(range(self.settings["map_size"]), N_entities)))

		for entity, position in zip(entities, positions):
			entity.position = position
			self.map[entity.position] = entity


	def printable_map(self):
		map_identifier = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=np.int)

		for entity in self.animals+self.foods:
			map_identifier[entity.position] = entity.identifier

		return map_identifier


	def step_forward(self):
		self.animal_deletion_list = set()
		self.food_deletion_list = set()
		for animal in self.animals:
			# Animal starves?
			if animal.hunger > animal.max_hunger:
				self.animal_deletion_list.add(animal)
				print("Animal starves")

			else:
				# May animal move?
				if animal.steps_taken < animal.speed:
					# Check for interactions
					if not self.nearest_neighbour_intereactions(animal):
						# If not, move animal
						direction = round(gauss(animal.last_direction, animal.direction_randomness)) % 4
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
			print(step)
			if self.exhausted_animals == len(self.animals):
				break
			else:
				self.step_forward()
				self.delete_animals()

	def run_cycles(self, maxcycles=50):
		map_graph(self.printable_map())
		for cycle in range(maxcycles):
			if len(self.animals) == 0 or len(self.animals)+len(self.foods) == self.settings["map_size"]**2:
				break
			else:
				self.cycle()
				self.reset_animals()
				map_graph(self.printable_map())

	def reset_animals(self):
		for animal in self.animals:
			animal.steps_taken = 0
			animal.libido += 1

		self.exhausted_animals = 0


	def delete_animals(self):
		for id in self.animal_deletion_list:
			# Make sure to remove it from the map too!
			self.map[id.position] = 0
			self.animals.remove(id)

		for id in self.food_deletion_list:
			# Make sure to remove it from the map too!
			self.map[id.position] = 0
			self.foods.remove(id)



	def nearest_neighbour_intereactions(self, animal):
		neighbours = np.mod(np.array(animal.position) + self.nn_array, self.settings["map_size"])

		for neighbour_id in neighbours:
			neighbour_id = tuple(neighbour_id)
			neighbour = self.map[neighbour_id]

			if neighbour == 0:
				# Nothing on the next tile
				pass

			# animal is fox
			if isinstance(animal, Fox):
				# next to rabbit
				if isinstance(neighbour, Rabbit):
					print("Rabbit gets eaten")
					self.animal_deletion_list.add(neighbour)
					animal.eat()
				elif isinstance(neighbour, Fox):
					if animal.reproductive_drive > neighbour.reproductive_drive:
						self.birth(Fox, neighbour_id, animal, neighbour)
						animal.libido = 0
						neighbour.libido = 0

			# animal is rabbit
			elif isinstance(animal, Rabbit):
				# next to carrot
				if isinstance(neighbour, Carrot):
					print("Carrot gets eaten")
					self.food_deletion_list.add(neighbour) # carrot is food
					animal.eat()
				# next to fox
				elif isinstance(neighbour, Fox):
					print("Rabit gets eaten")
					self.animal_deletion_list.add(animal)
					neighbour.eat()
				# next to rabbit
				elif isinstance(neighbour, Rabbit):
					if animal.libido > animal.reproductive_drive and neighbour.libido > neighbour.reproductive_drive:
						self.birth(Rabbit, neighbour_id, animal, neighbour)
						animal.libido = 0
						neighbour.libido = 0


	def birth(self, animal, postion, mom, dad):
		for direction in range(4):
			coords = self.new_coords(postion, direction)
			if self.map[coords] == 0:
				print("Baby rabbit is born!")
				mean_speed = (mom.speed + dad.speed ) / 2
				mean_reproductive_drive = (mom.reproductive_drive + dad.reproductive_drive ) / 2
				newanimal = animal(mean_speed, mean_reproductive_drive)
				self.position_entities([newanimal], [coords])
				self.animals.append(newanimal)
				break





	def move_animal(self, animal, direction, recursions = 0):
		new_pos = self.new_coords(animal.position, direction)
		if not self.map[new_pos]:
			# Walking costs food
			animal.hunger += 1

			animal.last_direction = direction

			# Update map
			self.map[animal.position] = 0
			self.map[new_pos] = animal

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