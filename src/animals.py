import numpy as np
from random import gauss, randint
from src.utils import minimum_int, direction_from_difference, nonzero_idx
from numba import njit


class Entity():
    def __init__(self, nutritional_value=15):
        self.position = (None, None)
        self.exists = True # Flag variable to combat copies of array still existing
        self.nutritional_value = nutritional_value

class Animal(Entity):

    def __init__(self, mean_speed, mean_reproductive_drive, mean_sight_radius, std, mean_max_hunger, mean_max_age, *args, **kwargs):
        # Spatial properties
        super(Animal, self).__init__(*args, **kwargs)

        # Animal Properties
        self.speed = minimum_int(gauss(mean_speed, std))
        self.reproductive_drive = minimum_int(gauss(mean_reproductive_drive, std))
        self.sight_radius = minimum_int(gauss(mean_sight_radius, std))
        self.max_hunger = minimum_int(gauss(mean_max_hunger, std*3))
        self.last_direction = randint(0, 3)
        self.direction_randomness = 0.4
        self.max_age = minimum_int(gauss(mean_max_age, std*3))

        #self.nutritional_value *= self.max_hunger

        # For keeping track of stuff
        self.steps_taken = 0
        self.hunger = self.max_hunger / 2
        self.libido = 0
        self.age = 0

    def eat(self, other):
        self.hunger = max((0, self.hunger-other.nutritional_value))
        #print("chomp")

    def food_check(self, treshold=0.4):
        """Returns true if the animal is hungry and false if the animal is not hungry"""
        if self.hunger > (self.max_hunger * treshold):
            return True
        else:
            return False

    def libido_check(self):
        if self.libido >= self.reproductive_drive:
            return True
        else:
            return False


class Fox(Animal):
    def __init__(self, *args, **kwargs):
        self.identifier = 4
        super(Fox, self).__init__(*args, **kwargs)

    def pathfinding(self, animal_map, food_map):
        animals_in_sight, sorted_animals_idx = pathfinding_check(self.position, self.sight_radius, animal_map.astype(np.bool_))

        # Check if there are entities within sight radius
        if animals_in_sight > 0:
            # Yes, interact possibly?
            for other_idx in sorted_animals_idx:
                other = animal_map[tuple(other_idx)]
                L = animal_map.shape[0]

                if isinstance(other, Rabbit) and self.food_check():
                    difference = (other_idx - np.array(self.position) + L/2) % L - L/2
                    # yes, yummy
                    return direction_from_difference(difference)

                elif isinstance(other, Fox) and not self.food_check() and self.libido_check():
                    difference = (other_idx - np.array(self.position) + L/2) % L - L/2
                    return direction_from_difference(difference)

        # No, move randomly
        return round(gauss(self.last_direction, self.direction_randomness)) % 4


    def interact(self, neighbour_animal):
        # animal is fox
        # next to Fox
        if isinstance(neighbour_animal, Fox) and (not self.food_check()) and (not neighbour_animal.food_check()) and self.libido_check():
            return True # Make baby?

        else:
            return False # Make baby?

    def eat_possible(self, other):
        if isinstance(other, Rabbit):
            return True
        else:
            return False

class Rabbit(Animal):
    def __init__(self, *args, **kwargs):
        self.identifier = 2
        super(Rabbit, self).__init__(*args, **kwargs)

    def pathfinding(self, animal_map, food_map):
        animals_in_sight, sorted_animals_idx = pathfinding_check(self.position, self.sight_radius, animal_map.astype(np.bool_))
        foods_in_sight, sorted_foods_idx = pathfinding_check(self.position, self.sight_radius, food_map.astype(np.bool_))

        L = animal_map.shape[0]
        # Check if there are entities within sight radius
        if animals_in_sight > 0:
            # Yes, interact possibly?
            for other_idx in sorted_animals_idx:
                other = animal_map[tuple(other_idx)]

                if isinstance(other, Fox):
                    reverse_difference = (np.array(self.position) - other_idx + L/2) % L - L/2
                    #print(f"{self} is a moving away from a fox! {self.position}, {other.position}")
                    # Fuck, run
                    return direction_from_difference(reverse_difference)

                elif isinstance(other, Rabbit) and not self.food_check() and self.libido_check():
                    #print(f"{self} is a moving to a rabbit! {self.position}, {other.position}")
                    difference = (other_idx - np.array(self.position) + L/2) % L - L/2
                    return direction_from_difference(difference)

        if foods_in_sight > 0 and self.food_check():
            for other_idx in sorted_foods_idx:
                other = food_map[tuple(other_idx)]
                if isinstance(other, Carrot):
                    #print(f"{self} is a moving to a carrot! {self.position}, {other.position}")
                    difference = (other_idx - np.array(self.position) + L/2) % L - L/2
                    return direction_from_difference(difference)

        # No, move randomly
        #print(f"{self} is a random mover! {self.position}")
        return round(gauss(self.last_direction, self.direction_randomness)) % 4

    def interact(self, neighbour_animal):
        # animal is rabbit
        # next to rabbit
        if isinstance(neighbour_animal, Rabbit) and (not self.food_check()) and (not neighbour_animal.food_check()) and self.libido_check():
            return True # Make baby?
        # next to carrot
        else:
            return False # Make baby?

    def eat_possible(self, other):
        if isinstance(other, Carrot):
            return True
        else:
            return False

class Carrot(Entity):
    def __init__(self, *args, **kwargs):
        self.identifier = 1
        super(Carrot, self).__init__()
        self.nutritional_value = 30

#@njit
def pathfinding_check(animal_position, animal_sight_radius, entity_map):
    other_idx = nonzero_idx(entity_map, *animal_position)
    if other_idx is None:
        return 0, None

    #nearest = other_idx[((other_idx - [coordinates[0],coordinates[1]])**2).sum(1).argmin()]
    
    # differences = np.sum((other_idx - np.array(animal_position))**2, axis=1) <= animal_sight_radius**2
    L = len(entity_map)
    diff = np.mod(other_idx - np.array(animal_position) + (L/2.), L ) - (L/2.) 
    differences = np.sum( diff**2, axis=1) <= animal_sight_radius**2
    
    # Are there entities within range?
    n = np.sum(differences)
    if n > 0:
        nearest_sorted = other_idx[np.argsort((diff[::,0] ** 2 + diff[::,1] ** 2))][:n]

        return n, nearest_sorted

    else:
        return 0, None

