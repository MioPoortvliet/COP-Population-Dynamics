import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

class MapAnimation:
    def __init__(self, simulation, frameskip=1):
        mpl.use('Qt5Agg')
        self.sim = simulation
        self.stats, self.genes = self.sim.run_cycles(maxcycles=1)
        self.frameskip= frameskip
        
        self.figure = plt.figure()
        self.gs = gridspec.GridSpec(3,20)
        n=5
        self.ax = self.figure.add_subplot(self.gs[:,2*n+1:-1])
        self.ax_cb = self.figure.add_subplot(self.gs[:,-1])
        colors= ["green","orange","white","white","red","red"]
        cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=6)
        norm = mpl.colors.Normalize(vmin=0, vmax=6)
        self.map_image = self.ax.imshow(self.sim.printable_map(), norm=norm, cmap=cmap)
        self.cbar = self.figure.colorbar(self.map_image, cax=self.ax_cb)
        self.cbar.set_ticks(np.array([1, 2, 3 , 4, 5])+.5)
        self.cbar.set_ticklabels(["Carrot", "Rabbit", "Rabbit+Carrot", "Fox", "Fox+Carrot"])
        
        self.ax_population = self.figure.add_subplot(self.gs[0,:2*n])
        self.ax_population.set_prop_cycle(color=['orange', 'red', 'grey'])
        self.lines_population = [self.ax_population.plot(self.stats[::,i]) for i in range(self.stats.shape[1])]
        self.ax_rabbit_1     = self.figure.add_subplot(self.gs[1,:n])
        self.ax_fox_1        = self.figure.add_subplot(self.gs[1,n:2*n])
        self.ax_rabbit_2     = self.figure.add_subplot(self.gs[2,:n])
        self.ax_fox_1        = self.figure.add_subplot(self.gs[2,n:2*n])
        
    def update(self,i):
        stats, genes = self.sim.run_cycles(maxcycles=self.frameskip)
        self.stats = np.append(self.stats, stats, axis=0)
        self.genes = np.append(self.genes, genes, axis=0)
        self.map_image.set_data(self.sim.printable_map())
        self.lines_population = [self.ax_population.plot(self.stats[::,i]) for i in range(self.stats.shape[1])]
        return self.map_image, self.lines_population
        
    def run(self):
        self.ani = animation.FuncAnimation(self.figure, self.update)
        self.gs.tight_layout(self.figure)
        plt.show()