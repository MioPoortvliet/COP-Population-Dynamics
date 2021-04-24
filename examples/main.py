from src.animals import Fox, Rabbit
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph

if __name__ == "__main__":
	foxes = []
	rabbits = []

	Ni_foxes = 5
	Ni_rabbits = 25

	settings = {
		"map_size":50,
		"entities": ["fox", "rabbit"],
		"fox":5,
		"rabbit":25,
		"carrots":20
	}
	animal_objects = {"fox": Fox, "rabbit": Rabbit}

	ae = AnimalEvolution(settings, animal_objects)

	# Plot the map
	map = ae.printable_map()
	print(map)
	map_graph(map)