from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot, MapPlot
import numpy as np

if __name__ == "__main__":
    settings = {
        "map_size":50,
        "animals": ["fox", "rabbit"],
        "foods": ["carrot", ],
        "fox":0,
        "rabbit":80,
        "carrot":800,
        "food_spawn_chance": {"carrot": 0.02},
        "stop_at_zero":False,
        "animal_std" : 3
    }

    fox_inits = {"mean_speed":5, "mean_reproductive_drive":10, "mean_sight_radius":1, "mean_max_hunger":50}
    rabbit_inits = {"mean_speed":3, "mean_reproductive_drive":2, "mean_sight_radius":5, "mean_max_hunger":150, "mean_max_age":100}

    animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    food_objects = {"carrot": Carrot}

    ae = AnimalEvolution(settings, food_objects, animal_objects)
    #map_graph(ae.printable_map())
    # We need pathfinding to food because the rabbits don't eat

    stats = ae.run_cycles(maxcycles=500)
    #map_graph(ae.printable_map())
    #for i in range(7):
    #    stats = np.append(stats,ae.run_cycles(maxcycles=3), axis=0)
        #map_graph(ae.printable_map())

    #stats = np.append(stats,ae.run_cycles(maxcycles=1000), axis=0)
    #map_graph(ae.printable_map())
    population_stats_plot(stats, food_objects, animal_objects)
    animal_stats_plot(stats, len(food_objects)+9*1+1, title="Rabbits")
