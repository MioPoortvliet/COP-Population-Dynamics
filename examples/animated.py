from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot, MapPlot
from src.animation import MapAnimation
import numpy as np

if __name__ == "__main__":
    settings = {
        "map_size":50,
        "animals": ["fox", "rabbit"],
        "foods": ["carrot", ],
        "fox":10,
        "rabbit":200,
        "carrot":1200,
        "food_spawn_chance": {"carrot": 0.05},
        "stop_at_zero":True,
        "animal_std" : 3
    }

    fox_inits = {
        "mean_speed":3,
        "mean_reproductive_drive":10,
        "mean_sight_radius":1,
        "mean_max_hunger":120,
        "mean_max_age":300
    }
    rabbit_inits = {
        "mean_speed":3,
        "mean_reproductive_drive":5,
        "mean_sight_radius":1,
        "mean_max_hunger":60,
        "mean_max_age":100,
        "nutritional_value":100
    }

    animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    food_objects = {"carrot": Carrot}

    ae = AnimalEvolution(settings, food_objects, animal_objects)
    simulation = MapAnimation(ae)
    simulation.run()