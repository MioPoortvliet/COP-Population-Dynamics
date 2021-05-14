# -*- coding: utf-8 -*-

from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot
from examples.graphs import settings, fox_inits, rabbit_inits
from src.IO_utils import load_and_concat
import numpy as np
import matplotlib.pyplot as plt

"""
If you care about the values of the frequancy in the frequency domain,
you should set freq_val=True and make sure to give a delta.
The delta parameter is just the value difference between two points in the quantity that will be converted to frequencies.
So in the case of a time series this is just the time between two datapoints.
"""
def FT(array, delta=1., freq_val=False):
    shift = np.fft.ifftshift(array)
    shiftfourier = np.fft.fft(shift)
    fourier = np.fft.fftshift(shiftfourier)
    if freq_val == True:
        freq = np.fft.fftshift(np.fft.fftfreq(len(array), d=delta))
        return fourier, freq
    elif freq_val == False:
        return fourier
    else:
        raise TypeError("'freq_val' should be 'boolean'")

def IFT(array, d_freq=1., freq_val=False):
    shift = np.fft.fftshift(array)
    shiftifourier = np.fft.ifft(shift)
    ifourier = np.fft.ifftshift(shiftifourier)
    if freq_val == True:
        time = np.fft.fftshift(np.fft.fftfreq(len(array), d=d_freq))
        return ifourier, time
    elif freq_val == False:
        return ifourier
    else:
        raise TypeError("'freq_val' should be 'boolean'")
        
def run_analysis(stats):
    ft_stats = np.fft.rfft(stats)
    ft_freqs = np.fft.rfftfreq(stats.shape[0],1)
    print(ft_stats)
    plt.figure()
    plt.plot(ft_freqs[1:250],np.abs(ft_stats[1:250]))
    plt.show()
    
if __name__ == "__main__":
    # animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    # food_objects = {"carrot": Carrot}

    # ae = AnimalEvolution(settings, food_objects, animal_objects)

    # stats, genes = ae.run_cycles(maxcycles=1000)
    # population_stats_plot(stats, food_objects, animal_objects)
    # plt.show()
    
    stats = np.load("generated/2021-05-14t164643174477-test-std0/stats.npy")
    plt.figure()
    plt.plot(stats[::,0])
    plt.plot(stats[::,1])
    plt.plot(stats[::,2])
    plt.show()
    
    run_analysis(stats[::,0])
    run_analysis(stats[::,1])
    run_analysis(stats[::,2])