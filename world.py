from pydoc import visiblename
from random import randrange
import numpy as np
from config import Config
from animals import Animal, Species


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

    def init(self, config: Config):
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
        a = Animal(x0=x0, y0=y0, init_energy=self.config.base_animal_energy, species=species, id=self.animal_ID, world=self)
        self.map[x0][y0] = species
        self.animals.append(a)

    def next_turn(self):
        for a in self.animals:
            old_x, old_y = a.get_position()
            direction = a.choose_direction()
            a.move(direction=direction, gridxsize=self.config.grid_xsize, gridysize=self.config.grid_ysize)
            new_x, new_y = a.get_position()
            self.map[old_x][old_y] = 0
            self.map[new_x][new_y] = a.id
    
    def get_map_for_render(self):
        render_map = self.map
        for a in self.animals:
            x, y = a.get_position()
            render_map[x][y] = a.species
        return render_map

    def get_submap(self, x: int, y: int, range: int):
        result = self.map[x-range-1:x+range, y-range-1:y+range]
        return result

    def get_n_prey(self):
        # TODO
        return 20

    def get_n_predators(self):
        # TODO
        return 30

    def get_n_grass(self):
        # TODO
        return 10
