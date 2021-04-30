import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

class MapAnimation:
    def __init__(self, simulation):  
        mpl.use('Qt5Agg'
        self.sim = simulation
        self.figure, self.ax = plt.subplots(figsize=(8,6))
        colors= ["green","orange","white","white","red","red"]
        cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=6)
        norm = mpl.colors.Normalize(vmin=0, vmax=6)
        self.map_image = self.ax.imshow(self.sim.printable_map(), norm=norm, cmap=cmap)
        self.cbar = self.figure.colorbar(self.map_image)
        self.cbar.set_ticks(np.array([1, 2, 3 , 4, 5])+.5)
        self.cbar.set_ticklabels(["Carrot", "Rabbit", "Rabbit+Carrot", "Fox", "Fox+Carrot"])
    
    def update(self,i):
        stats = self.sim.run_cycles(maxcycles=1)
        self.map_image.set_data(self.sim.printable_map())
        return self.map_image
        
    def run(self):
        self.ani = animation.FuncAnimation(self.figure, self.update)
        plt.show()