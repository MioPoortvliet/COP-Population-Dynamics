import matplotlib.pyplot as plt
import numpy as np


def map_graph(map):
	cb = plt.imshow(map)
	cbar = plt.colorbar(cb)
	cbar.set_ticks([2, 3, 10, 12, 13])
	cbar.set_ticklabels(["Rabbit", "Fox", "Food", "Rabbit+Food", "Fox+Food"])
	plt.show()


def population_stats_plot(stats, food_objects, animal_objects):
	stat_labels = [		"speed",
						"reproductive_drive",
						"sight_radius",
						"max_hunger",
						"max_age",
						"age",
						"hunger",
						"libido"
		]
	food_names = list(food_objects.keys())
	animal_names = list(animal_objects.keys())
	names = food_names+animal_names
	for i in range(len(names)):
		plt.plot(stats[::,i], label=names[i])

	plt.legend()
	plt.show()

def animal_stats_plot(stats, title="", labels=(0, 8)):
	x = np.arange(stats.shape[0])
	stat_labels = [		"speed",
						"reproductive_drive",
						"sight_radius",
						"max_hunger",
						"max_age",
						"age",
						"hunger",
						"libido"
		]
	for i, label in enumerate(stat_labels[labels[0]:labels[1]]):
		plt.errorbar(x=x, y=stats[::, i+labels[0], 0], label=label, yerr=stats[::, i+labels[0], 1])

	plt.legend()
	plt.title(title)
	plt.show()