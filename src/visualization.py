import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def map_graph(simulation_map: np.ndarray) -> None:
    """Plot the board"""
    figure, ax = plt.subplots(figsize=(8, 6))
    colors = ["green", "orange", "white", "white", "red", "red"]
    cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=6)
    norm = mpl.colors.Normalize(vmin=2, vmax=13)
    map_image = ax.imshow(simulation_map, norm=norm, cmap=cmap)
    cbar = figure.colorbar(map_image)
    cbar.set_ticks(np.array([1, 2, 3, 4, 5]) + .5)
    cbar.set_ticklabels(["Carrot", "Rabbit", "Rabbit+Carrot", "Fox", "Fox+Carrot"])
    plt.show()


def population_stats_plot(stats: np.ndarray, food_objects: dict, animal_objects: dict, title="") -> None:
    """A graph of population size over time"""
    food_names = list(food_objects.keys())
    animal_names = list(animal_objects.keys())
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_ylabel("Food units", color="r")
    ax1.tick_params(axis="y", labelcolor="r")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Animal units")

    color = ["red", "grey"]
    for i in range(len(food_names)):
        ax1.plot(stats[::, i], label=food_names[i], color='orange')

    for i in range(len(animal_names)):
        ax2.plot(stats[::, i + len(food_names)], label=animal_names[i], color=color[i])

    ax2.set_ylim(0)
    ax1.set_ylim(0)

    fig.legend()
    fig.suptitle(title)
    fig.show()


def animal_stats_plot(stats: np.ndarray, title="", labels=(0, 8)) -> None:
	"""A graph of animal property statistics over time."""
	plt.figure()
	x = np.arange(stats.shape[0])
	stat_labels = [		"speed",
						"sight_radius",
						"reproductive_drive",
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


def predator_prey(predator, prey):
    """Population size of predator on the x axis and of the prey on y axis"""
    plt.figure()
    plt.plot(predator, prey)
    plt.xlabel("Predator")
    plt.ylabel("Prey")
    plt.show()


class MapPlot:
    """Used by the animation engine to plot. Functions speak for themselves."""

    def __init__(self, simulation_map: np.ndarray, animal_evolution: np.ndarray) -> None:
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.map_image = self.ax.imshow(simulation_map)

    def update_map_plot(self, simulation_map: np.ndarray) -> None:
        self.map_image.set_data(simulation_map)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
