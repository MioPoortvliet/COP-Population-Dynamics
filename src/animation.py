# -*- coding: utf-8 -*-
"""
For the interactive animation

@author: Jonah Post
"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib import colors
from src.process_results import *
from src.IO_utils import load_and_concat, load_json


class Animation:
    def __init__(self, population_size_func, n=3, frameskip=1):
        """
        Initializes the Animation Class. Stores and calculates all relevant physical quantities and sets up the figures for the animation.
        
        param positions: positions per particle at every timestep.
        type positions: np.ndarray
        param velocities: velocities per particle at every timestep
        type velocities: np.ndarray
        param potential energy: potential energy per particle at every timestep
        type potential energy: np.ndarray
        param properties: 
        type properties: 
        param frameskip: the number of frames to be skipped while running the animation.
        type frameskip: int
        """

        # This call forces the plot in an interactive window
        mpl.use('Qt5Agg')
        self.frameskip = frameskip
        self.func = population_size_func

        self.frame_index=0
        
        self.fig = plt.figure()
        self.gs = gridspec.GridSpec(3,6)

        self.ax = self.fig.add_subplot(self.gs[:,:-2])
        self.ax.set_aspect('equal')
        self.scats = [self.ax.scatter(self.positions[0,j,0],self.positions[0,j,1], s=2) for j,pos in enumerate(self.positions[0,::,0])]
        self.time_text = self.ax.text(.02, .02, '', transform=self.ax.transAxes, color="black")
        self.config_text = self.ax.text(.02, .95, '', transform=self.ax.transAxes, color="black")
        
        self.time_per_frame = 1
        
        #self.ax.set_xlim([0, self.box_size[0]])
        #self.ax.set_ylim([0, self.box_size[1]])
        self.ax.set_xlabel('Cycle')
        self.ax.set_ylabel('Population size')
        self.ax.set_title('Population size over time')
        
        self.tail_length = 3
    

    def run(self, final=50):
        self.anim = animation.FuncAnimation(self.fig, self.update2d, frames = np.arange(0, final, step=self.frameskip), repeat=False)
        self.gs.tight_layout(self.fig)
        plt.show()


    def update2d(self, i):
        self.frame_index=i
        for j, self.scat in enumerate(self.scats):
            if self.frame_index<self.tail_length*self.frameskip:
                self.scat._offsets = (self.positions[:self.frame_index+1,j,0:2])
                self.scat.set_sizes(np.linspace(0,4,num=self.frame_index, dtype=float))
            else:
                self.scat._offsets = (self.positions[self.frame_index+1-self.tail_length*self.frameskip:self.frame_index+1,j,0:2])
                self.scat.set_sizes(np.linspace(0,4,num=self.tail_length*self.frameskip, dtype=float))
        self.time_text.set_text('frame = {frame:.1f}\ntime = {time:.3f}e-12 s'.format(frame = self.frame_index, time = self.frame_index*self.time_per_frame*(1e12)))
