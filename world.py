from random import randrange
import numpy as np
from config import Config
from animals import Animal, Directions, Species


class World:
    """
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    """

    def __init__(self, config: Config):
        self.config = config
        self.map = np.zeros((config.grid_xsize, config.grid_ysize), dtype=np.int8)
        self.animal_ID = 0
        self.animals: list[Animal] = []
        self.init_animals()

    
    def init_animals(self):
        for i in range(self.config.n_predator):
            x = randrange(0,self.config.grid_xsize)
            y = randrange(0,self.config.grid_ysize)
            while(self.map[x][y] != 0):
                x = randrange(0,self.config.grid_xsize)
                y = randrange(0,self.config.grid_ysize)
            self.add_animal(x0=x, y0=y, species=Species.PREDATOR)

        for i in range(self.config.n_prey):
            x = randrange(0,self.config.grid_xsize)
            y = randrange(0,self.config.grid_ysize)
            while(self.map[x][y] != 0):
                x = randrange(0,self.config.grid_xsize)
                y = randrange(0,self.config.grid_ysize)
            self.add_animal(x0=x, y0=y, species=Species.PREY)

    def add_animal(self, x0: int, y0: int, species: int):
        self.animal_ID = self.animal_ID + 1
        a = Animal(x0=x0, y0=y0, init_energy=self.config.base_animal_energy, species=species, id=self.animal_ID)
        self.map[x0][y0] = species
        self.animals.append(a)

    def next_turn(self):
        for a in self.animals:
            direction = Directions.DOWN
            old_x, old_y = a.get_position()
            a.move(direction=direction, gridxsize=self.config.grid_xsize, gridysize=self.config.grid_ysize)
            new_x, new_y = a.get_position()
            self.map[old_x][old_y] = 0
            self.map[new_x][new_y] = a.species


print(World(Config()).map)