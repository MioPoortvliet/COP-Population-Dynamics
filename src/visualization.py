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

def stats_plot(stats, food_objects, animal_objects):
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


