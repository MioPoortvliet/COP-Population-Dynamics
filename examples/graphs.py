from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot
import numpy as np

fox_density = 0.005
rabbit_density = 0.11
carrot_density = 0.2
map_size = 50
settings = {
    "map_size": map_size,
    "animals": ["fox", "rabbit"],
    "foods": ["carrot", ],
    "fox": int(fox_density * map_size ** 2),
    "rabbit": int(rabbit_density * map_size ** 2),
    "carrot": int(carrot_density * map_size ** 2),
    "food_spawn_chance": {"carrot": 0.05},
    "stop_at_zero": False,
    "animal_std": 3
}

fox_inits = {
    "mean_speed": 3,
    "mean_reproductive_drive": 10,
    "mean_sight_radius": 5,
    "mean_max_hunger": 60,
    "mean_max_age": 100
}
rabbit_inits = {
    "mean_speed": 3,
    "mean_reproductive_drive": 5,
    "mean_sight_radius": 3,
    "mean_max_hunger": 40,
    "mean_max_age": 100,
    "nutritional_value": 20
}

if __name__ == "__main__":


    animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    food_objects = {"carrot": Carrot}

    ae = AnimalEvolution(settings, food_objects, animal_objects)
    #map_graph(ae.printable_map())
    # We need pathfinding to food because the rabbits don't eat

    stats, genes = ae.run_cycles(maxcycles=500)
    #map_graph(ae.printable_map())
    #for i in range(7):
    #    stats_, genes_ = ae.run_cycles(maxcycles=10)
    #    stats = np.append(stats,stats_, axis=0)
    #    genes = np.append(genes,genes_, axis=0)
        #map_graph(ae.printable_map())

    #stats = np.append(stats,, axis=0)
    #map_graph(ae.printable_map())

    population_stats_plot(stats, food_objects, animal_objects)

    for i, animal in enumerate(animal_objects.keys()):
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(0, 3))
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(3, 8))
