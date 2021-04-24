import numpy as np
from random import sample

class AnimalEvolution():
	def __init__(self, settings, animal_objects):
		self.settings = settings
		self.animal_objects = animal_objects

		self.entities = []

		self.spawn_entities()

	def spawn_entities(self):

		for entity in self.settings["entities"]:
			for i in range(self.settings[entity]):
				self.entities.append(self.animal_objects[entity]())

		self.position_entities()


	def position_entities(self):
		N_entities = len(self.entities)
		# Generate coordinates
		positions = list(zip(sample(range(self.settings["map_size"]), N_entities), sample(range(self.settings["map_size"]), N_entities)))

		for i, entity in enumerate(self.entities):
			entity.position = positions[i]

	def printable_map(self):
		map_identifier = np.zeros(shape=(self.settings["map_size"], self.settings["map_size"]), dtype=np.int)

		for entity in self.entities:
			map_identifier[entity.position] = entity.identifier
			print(entity.position)

		return map_identifier