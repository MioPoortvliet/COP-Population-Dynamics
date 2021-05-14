from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import map_graph, population_stats_plot, animal_stats_plot
from src.IO_utils import to_file, slugify, ensure_dir, to_json
from datetime import datetime
import numpy as np

fox_density = 0.005
rabbit_density = 0.11
carrot_density = 0.2
map_size = 50
settings = {
    "map_size": map_size,
    "animals": ["fox", "rabbit"],
    "foods": ["carrot", ],
    "fox": int(fox_density * map_size ** 2),
    "rabbit": int(rabbit_density * map_size ** 2),
    "carrot": int(carrot_density * map_size ** 2),
    "food_spawn_chance": {"carrot": 0.05},
    "stop_at_zero": True,
    "animal_std": 0,
    "avoid_extinction": False
}

fox_inits = {
    "mean_speed": 1,
    "mean_reproductive_drive": 10,
    "mean_sight_radius": 5,
    "mean_max_hunger": 100,
    "mean_max_age": 300
}
rabbit_inits = {
    "mean_speed": 1,
    "mean_reproductive_drive": 5,
    "mean_sight_radius": 3,
    "mean_max_hunger": 40,
    "mean_max_age": 100,
    "nutritional_value": 1 # Multiplied by max_hunger!
}


def run_sim(animal_std=settings["animal_std"], id="no_id", maxcycles=1000):
    settings["animal_std"] = animal_std
    # Set up file structure
    fpath = f"generated/{slugify(datetime.now().isoformat())}-{id}-std{animal_std}/"
    ensure_dir(fpath)
    # Write simulation parameters to file
    to_json(fpath+"settings.json", settings)
    to_json(fpath+"fox_inits.json", fox_inits)
    to_json(fpath+"rabbit_inits.json", rabbit_inits)

    animal_objects = {"fox": {"object":Fox, "init":fox_inits}, "rabbit": {"object":Rabbit, "init":rabbit_inits}}
    food_objects = {"carrot": Carrot}

    ae = AnimalEvolution(settings, food_objects, animal_objects)
    #map_graph(ae.printable_map())
    # We need pathfinding to food because the rabbits don't eat

    stats, genes = ae.run_cycles(maxcycles=maxcycles)

    # Save simulated data
    to_file(fpath+"stats", stats)
    to_file(fpath+"genes", genes)

    population_stats_plot(stats, food_objects, animal_objects)

    for i, animal in enumerate(animal_objects.keys()):
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(0, 3))
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(3, 8))



if __name__ == "__main__":
    run_sim(0, maxcycles=100, id="test")
    #for std in np.linspace(0, 2, 10):
    #    run_sim(std, maxcycles=50000, id="semiSeriousRun")