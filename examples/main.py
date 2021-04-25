from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, stats_plot

if __name__ == "__main__":
	settings = {
		"map_size":15,
		"animals": ["fox", "rabbit"],
		"foods": ["carrot", ],
		"fox":0,
		"rabbit":10,
		"carrot":30,
		"food_spawn_chance": {"carrot": 0.01},
		"stop_at_zero":False
	}

	fox_inits = {"mean_speed":5, "mean_reproductive_drive":10, "mean_sight_radius":1, "max_hunger":50}
	rabbit_inits = {"mean_speed":3, "mean_reproductive_drive":6, "mean_sight_radius":1, "max_hunger":6}

	animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
	food_objects = {"carrot": Carrot}


	ae = AnimalEvolution(settings, food_objects, animal_objects)
	#map_graph(ae.printable_map())
	# We need pathfinding to food because the rabbits don't eat

	stats = ae.run_cycles(maxcycles=150)
	map_graph(ae.printable_map())

	stats_plot(stats, food_objects, animal_objects)