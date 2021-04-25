from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, stats_plot
from src.animation import Animation
import matplotlib.pyplot as plt

if __name__ == "__main__":
	settings = {
		"map_size":50,
		"animals": ["fox", "rabbit"],
		"foods": ["carrot", ],
		"fox":0,
		"rabbit":100,
		"carrot":100,
		"food_spawn_chance": {"carrot": 0.05},
		"stop_at_zero":False
	}

	fox_inits = {"mean_speed":5, "mean_reproductive_drive":10, "mean_sight_radius":1, "max_hunger":50}
	rabbit_inits = {"mean_speed":3, "mean_reproductive_drive":4, "mean_sight_radius":1, "max_hunger":20}

	animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
	food_objects = {"carrot": Carrot}


	ae = AnimalEvolution(settings, food_objects, animal_objects)
	#map_graph(ae.printable_map())
	# We need pathfinding to food because the rabbits don't eat

	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)

	def animate(i):
		pullData

	stats = ae.run_cycles(maxcycles=100)
	map_graph(ae.printable_map())

	stats_plot(stats, food_objects, animal_objects)