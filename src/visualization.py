import matplotlib.pyplot as plt


def map_graph(map):
	cb = plt.imshow(map)
	cbar = plt.colorbar(cb)
	cbar.set_ticks(range(1, 4))
	cbar.set_ticklabels(["Carrot", "Rabbit", "Fox"])
	plt.show()
