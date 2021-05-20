# -*- coding: utf-8 -*-

from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot
from examples.graphs import settings, fox_inits, rabbit_inits
from src.IO_utils import load_and_concat
import numpy as np
import matplotlib.pyplot as plt
import os

        
def run_analysis(stats, ax, N_ignore=100, freq_cut=(1, 50), **kwargs):
    ft_stats = np.fft.rfft(stats[N_ignore:])
    ft_freqs = np.fft.rfftfreq(stats[N_ignore:].shape[0],1)
    ax.plot(ft_freqs[freq_cut[0]:freq_cut[1]],np.abs(ft_stats[freq_cut[0]:freq_cut[1]]), **kwargs)

def analyse_single(path, skipdata=100):
    stats = np.load(f"{path}/stats.npy")
    genes = np.load(f"{path}/genes.npy")

    population_stats_plot(stats[skipdata:], food_objects, animal_objects, title=path)
    # for i, animal in enumerate(animal_objects.keys()):
    #    animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(0, 3))
    #    animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(3, 8))

    fig, ax = plt.subplots(figsize=(8,6))

    run_analysis(stats[::, 0], ax, skipdata, label="carrots", color="orange")
    run_analysis(stats[::, 1], ax, skipdata, label="fox", color="red")
    run_analysis(stats[::, 2], ax, skipdata, label="rabbit", color="grey")

    ax.legend()
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Units")
    fig.show()


if __name__ == "__main__":
    animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    food_objects = {"carrot": Carrot}

    # ae = AnimalEvolution(settings, food_objects, animal_objects)

    # stats, genes = ae.run_cycles(maxcycles=1000)
    # population_stats_plot(stats, food_objects, animal_objects)
    # plt.show()

    analyse_single(path="generated/finding_parameters/2021-05-20t173011455025-test-std0")
    # generated/run1/2021-05-20t154159037815-test-std0
    # generated/finding_parameters/2021-05-20t163730727533-test-std0
    
    path = "generated/finding_parameters/"
    #folders = os.listdir(path)
    #for directory in folders:
    #    print(path+directory)
    #    analyze_single(path+directory)