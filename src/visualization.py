import matplotlib.pyplot as plt


def map_graph(map):
	cb = plt.imshow(map)
	cbar = plt.colorbar(cb)
	cbar.set_ticks(range(1, 4))
	cbar.set_ticklabels(["Carrot", "Rabbit", "Fox"])
	plt.show()


def stats_plot(stats, food_objects, animal_objects):
	names = list(food_objects.keys())+list(animal_objects.keys())
	for i in range(stats.shape[1]):
		plt.plot(stats[::,i], label=names[i])
	plt.legend()
	plt.show()