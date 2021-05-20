from src.animals import Fox, Rabbit, Carrot
from examples.graphs import run_sim
from src.analysis import analyse_single

# Simulation settings
fox_density = 0.0009
rabbit_density = 0.007
carrot_density = 0.02
map_size = 150
settings = {
	"map_size": map_size,
	"animals": ["fox", "rabbit"],
	"foods": ["carrot", ],
	"fox": int(fox_density * map_size ** 2),
	"rabbit": int(rabbit_density * map_size ** 2),
	"carrot": int(carrot_density * map_size ** 2),
	"food_spawn_chance": {"carrot": 0.0004},
	"stop_at_zero": True,
	"animal_std": 0.1,
	"avoid_extinction": False
}

# Animal settings
fox_inits = {
	"mean_speed": 3,
	"mean_reproductive_drive": 200,
	"mean_sight_radius": 5,
	"mean_max_hunger": 4000,
	"mean_max_age": 10000
}
rabbit_inits = {
	"mean_speed": 2,
	"mean_reproductive_drive": 30,
	"mean_sight_radius": 10,
	"mean_max_hunger": 400,
	"mean_max_age": 4000,
	"nutritional_value": 400
}

# Set up simulation
animal_objects = {"fox": {"object": Fox, "init": fox_inits}, "rabbit": {"object": Rabbit, "init": rabbit_inits}}
food_objects = {"carrot": Carrot}

if __name__ == '__main__':
	outputpath = run_sim(settings, id="main", maxcycles=1000, food_objects=food_objects, animal_objects=animal_objects)
	analyse_single(outputpath, skipdata=0)
