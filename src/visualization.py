import matplotlib.pyplot as plt


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
	for i in range(len(food_names)):
		plt.plot(stats[::,i], label=food_names[i])
	for j in range(len(animal_names)):
		#print(j, i+j*len(stat_labels)+1)
		plt.plot(stats[::,i+j*(len(stat_labels)+1)+1], label=animal_names[j])

	plt.legend()
	plt.show()

def animal_stats_plot(stats, relative_idx, title="", labels=(0, -1)):
	stat_labels = [		"speed",
						"reproductive_drive",
						"sight_radius",
						"max_hunger",
						"max_age",
						"age",
						"hunger",
						"libido"
		]
	for i in range(len(stat_labels[labels[0]:labels[-1]])):
		plt.plot(stats[::,i+relative_idx+labels[0]], label=stat_labels[i+labels[0]])

	plt.legend()
	plt.title(title)
	plt.show()