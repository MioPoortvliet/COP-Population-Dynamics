# -*- coding: utf-8 -*-

from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot, predator_prey
from examples.graphs import settings, fox_inits, rabbit_inits, food_objects, animal_objects
from src.IO_utils import load_and_concat
import numpy as np
import matplotlib.pyplot as plt
import os

        
def fourier_analysis(stats: dict, ax: plt.Axes, N_ignore=100, freq_cut=(1, 40), **kwargs) -> None:
    """Plot the Fourier analysis on the given ax"""
    ft_stats = np.fft.rfft(stats[N_ignore:])
    ft_freqs = np.fft.rfftfreq(stats[N_ignore:].shape[0],1)
    ax.plot(ft_freqs[freq_cut[0]:freq_cut[1]],np.abs(ft_stats[freq_cut[0]:freq_cut[1]]), **kwargs)

def analyse_single(path:str, skipdata=0) -> None:
    # Load the data
    stats = np.load(f"{path}/stats.npy")
    genes = np.load(f"{path}/genes.npy")

    # Plot a bunch of crap
    population_stats_plot(stats[skipdata:], food_objects, animal_objects, title=path)

    predator_prey(stats[skipdata:,2], stats[skipdata:,1])
    predator_prey(stats[skipdata:,1], stats[skipdata:,0])

    for i, animal in enumerate(animal_objects.keys()):
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(0, 3))
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(3, 8))

    fig, ax = plt.subplots()

    # Carrot, Fox, Rabbit population Fourier analysis
    fourier_analysis(stats[::, 0], ax, skipdata, label="carrots", color="orange")
    fourier_analysis(stats[::, 1], ax, skipdata, label="fox", color="red")
    fourier_analysis(stats[::, 2], ax, skipdata, label="rabbit", color="grey")

    ax.legend()
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Units")
    fig.show()


if __name__ == "__main__":
    #analyse_single(path="generated/finding_parameters/2021-05-20t154250699648-possiblestable-std0")
    analyse_single("generated/finding_parameters/2021-05-20t161815999948-seriousRun-0-std0.0")

    # Uncomment to batch process a folder
    """
    path = "generated/finding_parameters/"
    folders = os.listdir(path)
    for directory in folders:
        print(path+directory)
        analyse_single(path+directory)
    """