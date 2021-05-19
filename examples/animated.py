from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot, MapPlot
from src.animation import MapAnimation
from examples.graphs import settings, fox_inits, rabbit_inits
import numpy as np

if __name__ == "__main__":
    animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    food_objects = {"carrot": Carrot}

    ae = AnimalEvolution(settings, food_objects, animal_objects)
    simulation = MapAnimation(ae, frameskip=50)
    simulation.run()