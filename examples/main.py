from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph

if __name__ == "__main__":
	foxes = []
	rabbits = []

	Ni_foxes = 5
	Ni_rabbits = 25

	settings = {
		"map_size":50,
		"animals": ["fox", "rabbit"],
		"foods": ["carrot", ],
		"fox":5,
		"rabbit":20,
		"carrot":5
	}
	animal_objects = {"fox": Fox, "rabbit": Rabbit}
	food_objects = {"carrot": Carrot}

	ae = AnimalEvolution(settings, food_objects, animal_objects)

	ae.run_cycles()