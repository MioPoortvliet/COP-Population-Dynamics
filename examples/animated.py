from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot, MapPlot
from src.animation import MapAnimation
from examples.graphs import settings, animal_objects, food_objects
import numpy as np

if __name__ == "__main__":
    """Runs simulation while generating the animation. The settings are imported from examples/graphs.py. Change the 
    frame skip parameter to animate a frame only every so many cycles. This can speed up the simulation quite a bit. """
    ae = AnimalEvolution(settings, food_objects, animal_objects)
    simulation = MapAnimation(ae, frameskip=1)
    simulation.run()
