import matplotlib.pyplot as plt
import matplotlib as mpl

def map_graph(simulation_map):
    figure, ax = plt.subplots(figsize=(8,6))
    colors= ["green","orange","white","white","red","red"]
    cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=6)
    norm = mpl.colors.Normalize(vmin=2, vmax=13)
    map_image = ax.imshow(simulation_map, norm=norm, cmap=cmap)
    cbar = figure.colorbar(map_image)
        self.cbar.set_ticks(np.array([1, 2, 3 , 4, 5])+.5)
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
	for i in range(len(food_names)):
		plt.plot(stats[::,i], label=food_names[i])
	for j in range(len(animal_names)):
		#print(j, i+j*len(stat_labels)+1)
		plt.plot(stats[::,i+j*(len(stat_labels)+1)+1], label=animal_names[j])

	plt.legend()
	plt.show()

def animal_stats_plot(stats, relative_idx, title=""):
	stat_labels = [		"speed",
						"reproductive_drive",
						"sight_radius",
						"max_hunger",
						"max_age",
						"age",
						"hunger"#,
						#"libido"
		]
	for i in range(len(stat_labels)):
		plt.plot(stats[::,i+relative_idx], label=stat_labels[i])

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


