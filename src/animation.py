import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

class MapAnimation:
    def __init__(self, simulation, frameskip=1):
        """
        Initializes the Animation Class. Stores and calculates all relevant physical quantities and sets up the figures for the animation.
        
        param simulation: simulation describing the animal evolution
        type simulation: class
        param frameskip: the number of simulations steps between frames.
        type frameskip: int
        """
        mpl.use('Qt5Agg')
        self.sim = simulation
        self.stats, self.genes = self.sim.run_cycles(maxcycles=1)
        self.frameskip= frameskip
        
        self.labels = (0, 8)
        self.genes_labels = ["speed",
    						"reproductive_drive",
    						"sight_radius",
    						"max_hunger",
    						"max_age",
    						"age",
    						"hunger",
    						"libido"
		]
        
        self.figure = plt.figure()
        self.gs = gridspec.GridSpec(6,20)
        n=5
        self.ax = self.figure.add_subplot(self.gs[:-2,2*n+1:-1])
        self.ax_cb = self.figure.add_subplot(self.gs[:-2,-1])
        colors= ["green","orange","white","white","red","red"]
        cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=6)
        norm = mpl.colors.Normalize(vmin=0, vmax=6)
        self.map_image = self.ax.imshow(self.sim.printable_map(), norm=norm, cmap=cmap)
        self.cbar = self.figure.colorbar(self.map_image, cax=self.ax_cb)
        self.cbar.set_ticks(np.array([1, 2, 3 , 4, 5])+.5)
        self.cbar.set_ticklabels(["Carrot", "Rabbit", "Rabbit+Carrot", "Fox", "Fox+Carrot"])
        
        # make all axes
        self.ax_animal_population = self.figure.add_subplot(self.gs[-2:,2*n+1:-1])
        self.ax_food_population = self.ax_animal_population.twinx()
        self.ax_animal_population.set_prop_cycle(color=['red', 'grey'])
        self.ax_food_population.set_prop_cycle(color=['orange'])
        self.lines_animal_population = [self.ax_animal_population.plot(self.stats[::,i]) for i in range(1,self.stats.shape[1])]
        self.lines_food_population = [self.ax_food_population.plot(self.stats[::,0])]
        
        self.ax_rabbit_1     = self.figure.add_subplot(self.gs[1:3,0:n])
        self.lines_rabbit_1   = [self.ax_rabbit_1.plot(self.genes[::, 1, i, 0], label=label) for i, label in enumerate(self.genes_labels[0:3])]
        
        self.ax_fox_1        = self.figure.add_subplot(self.gs[1:3,n:2*n])
        self.lines_fox_1   = [self.ax_fox_1.plot(self.genes[::, 0, i, 0], label=label) for i, label in enumerate(self.genes_labels[0:3])]
        
        self.ax_rabbit_2     = self.figure.add_subplot(self.gs[4:,0:n])
        self.lines_rabbit_2   = [self.ax_rabbit_2.plot(self.genes[::, 1, i+3, 0], label=label) for i, label in enumerate(self.genes_labels[3:8])]
        
        self.ax_fox_2        = self.figure.add_subplot(self.gs[4:,n:2*n])
        self.lines_fox_2   = [self.ax_fox_2.plot(self.genes[::, 0, i+3, 0], label=label) for i, label in enumerate(self.genes_labels[3:8])]
        
    def update(self,j):
        """
        Runs the symulation for [frameskip] cycles and then updates the figure. To be called by the FuncAnimation function.
        
        :param j: animation frame number
        :type j: int
        """
        stats, genes = self.sim.run_cycles(maxcycles=self.frameskip)
        self.stats = np.append(self.stats, stats, axis=0)
        self.genes = np.append(self.genes, genes, axis=0)
        self.map_image.set_data(self.sim.printable_map())
        [ax.clear() for ax in [self.ax_animal_population, self.ax_food_population, self.ax_rabbit_1, self.ax_fox_1, self.ax_rabbit_2, self.ax_fox_2 ]]
        
        self.ax_animal_population.set_prop_cycle(color=['red', 'grey'])
        self.ax_food_population.set_prop_cycle(color=['orange'])
        self.lines_animal_population = [self.ax_animal_population.plot(self.stats[::,i]) for i in range(1,self.stats.shape[1])]
        self.lines_food_population = [self.ax_food_population.plot(self.stats[::,0])]
        
        self.lines_rabbit_1   = [self.ax_rabbit_1.plot(self.genes[::, 1, i+self.labels[0], 0], label=label) for i, label in enumerate(self.genes_labels[0:3])]
        self.lines_fox_1   = [self.ax_fox_1.plot(self.genes[::, 0, i, 0], label=label) for i, label in enumerate(self.genes_labels[0:3])]
        self.lines_rabbit_2   = [self.ax_rabbit_2.plot(self.genes[::, 1, i+3, 0], label=label) for i, label in enumerate(self.genes_labels[3:8])]
        self.lines_fox_2   = [self.ax_fox_2.plot(self.genes[::, 0, i+3, 0], label=label) for i, label in enumerate(self.genes_labels[3:8])]
        self.ax_fox_1.legend(bbox_to_anchor=(.7, 1,.3,.4))
        self.ax_fox_2.legend(bbox_to_anchor=(.5, 1,.3,.4))
        
        [ax.set_ylim(0) for ax in [self.ax_animal_population, self.ax_food_population, self.ax_rabbit_1, self.ax_fox_1, self.ax_rabbit_2, self.ax_fox_2 ]]
        [ax.set_xlim(0) for ax in [self.ax_animal_population, self.ax_food_population, self.ax_rabbit_1, self.ax_fox_1, self.ax_rabbit_2, self.ax_fox_2 ]]
        
        return self.map_image
        
    def run(self):
        """
        Run the animation by repeated calling of update()
        """
        self.ani = animation.FuncAnimation(self.figure, self.update)
        self.gs.tight_layout(self.figure)
        plt.show()