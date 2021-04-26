from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, stats_plot
import numpy as np

if __name__ == "__main__":
	settings = {
		"map_size":50,
		"animals": ["fox", "rabbit"],
		"foods": ["carrot", ],
		"fox":0,
		"rabbit":80,
		"carrot":800,
		"food_spawn_chance": {"carrot": 0.01},
		"stop_at_zero":False
	}

	fox_inits = {"mean_speed":5, "mean_reproductive_drive":10, "mean_sight_radius":1, "max_hunger":50}
	rabbit_inits = {"mean_speed":3, "mean_reproductive_drive":3, "mean_sight_radius":5, "max_hunger":150, "max_age":100}

	animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
	food_objects = {"carrot": Carrot}


	ae = AnimalEvolution(settings, food_objects, animal_objects)
	#map_graph(ae.printable_map())
	# We need pathfinding to food because the rabbits don't eat

	stats = ae.run_cycles(maxcycles=25)
	map_graph(ae.printable_map())
	for i in range(7):
		stats = np.append(stats,ae.run_cycles(maxcycles=3), axis=0)
		map_graph(ae.printable_map())

	stats = np.append(stats,ae.run_cycles(maxcycles=1000), axis=0)
	map_graph(ae.printable_map())
	stats_plot(stats, food_objects, animal_objects)
