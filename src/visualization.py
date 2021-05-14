import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def map_graph(simulation_map):
	figure, ax = plt.subplots(figsize=(8,6))
	colors= ["green","orange","white","white","red","red"]
	cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=6)
	norm = mpl.colors.Normalize(vmin=2, vmax=13)
	map_image = ax.imshow(simulation_map, norm=norm, cmap=cmap)
	cbar = figure.colorbar(map_image)
	cbar.set_ticks(np.array([1, 2, 3 , 4, 5])+.5)
	cbar.set_ticklabels(["Carrot", "Rabbit", "Rabbit+Carrot", "Fox", "Fox+Carrot"])
	plt.show()

def population_stats_plot(stats, food_objects, animal_objects):
	food_names = list(food_objects.keys())
	animal_names = list(animal_objects.keys())
	plt.figure()
	fig, ax1 = plt.subplots()
	ax1.set_ylabel("Animal units")


	ax2 = ax1.twinx()
	ax2.set_ylabel("Food units", color="r")
	ax2.tick_params(axis="y", labelcolor="r")

	for i in range(len(animal_names)):
		ax1.plot(stats[::,i+len(food_names)], label=animal_names[i])

	for i in range(len(food_names)):
		ax2.plot(stats[::,i], label=food_names[i], color='r')

	ax1.set_ylim(0)
	ax2.set_ylim(0)

	fig.legend()
	fig.show()


def animal_stats_plot(stats, title="", labels=(0, 8)):
	plt.figure()
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
		plt.errorbar(x=x, y=stats[::, i+labels[0], 0], label=label)
		plt.fill_between(
			x,
			stats[::, i+labels[0], 0]-stats[::, i+labels[0], 1],
			stats[::, i+labels[0], 0]+stats[::, i+labels[0], 1],
			alpha=0.2
		)

	plt.legend()
	plt.title(title)
	plt.show()

def stats_plot(stats, food_objects, animal_objects):
	plt.figure()
	names = list(food_objects.keys())+list(animal_objects.keys())
	for i in range(stats.shape[1]):
		plt.plot(stats[::,i], label=names[i])
	plt.legend()
	plt.show()

class MapPlot:
	def __init__(self, simulation_map, animal_evolution):
		self.figure, self.ax = plt.subplots(figsize=(8,6))
		self.map_image = self.ax.imshow(simulation_map)

	def update_map_plot(self, simulation_map):
		self.map_image.set_data(simulation_map)
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()


