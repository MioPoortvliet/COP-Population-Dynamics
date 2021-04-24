import numpy as np
from random import sample, normalvariate

class AnimalEvolution():
	def __init__(self, settings, food_objects, animal_objects):
		self.settings = settings
		self.animal_objects = animal_objects
		self.food_objects = food_objects

		# Split these because food does not update
		self.animals = []
		self.foods = []
		self.taken_positions = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=np.bool_)

		self.spawn_entities()
		self.position_entities(self.animals+self.foods)


	def spawn_entities(self):
		for animal in self.settings["animals"]:
			for i in range(self.settings[animal]):
				self.animals.append(self.animal_objects[animal]())

		for food in self.settings["foods"]:
			for i in range(self.settings[food]):
				self.foods.append(self.food_objects[food]())


	def position_entities(self, entities):
		N_entities = len(entities)
		# Generate coordinates
		positions = list(zip(sample(range(self.settings["map_size"]), N_entities), sample(range(self.settings["map_size"]), N_entities)))

		for i, entity in enumerate(entities):
			entity.position = positions[i]
			self.taken_positions[entity.position] = True


	def printable_map(self):
		map_identifier = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=np.int)

		for entity in self.animals+self.foods:
			map_identifier[entity.position] = entity.identifier
			print(entity.position)

		return map_identifier


	def step_forward(self):
		for entity in self.animals:
			direction = int(normalvariate(entity.d))