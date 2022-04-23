from random import randrange

import numpy as np

from config import Config
from world.abstracts import AbstractAnimal, AbstractMap, AbstractMapTile
from world.animals import Animal
from world.enumerators import Species


class MapTile(AbstractMapTile):
    """
    Class representing one tile of the map
    """

    def __init__(self):
        self.animals = []
        self.plant_supply = 1.0
    
    def put_animal(self, a: Animal):
        self.animals.append(a)
    
    def remove_animal(self, a_to_remove: Animal):
        animals = self.animals
        self.animals = ([a for a in animals if a.id != a_to_remove.id])

    def get_render_value(self):
        if len(self.animals) > 0:
            return self.animals[0].species
        return 0

    def get_n_plants(self):
        return int(self.plant_supply)


class Map(AbstractMap):
    """
    Class holding all entities on it
    """

    def __init__(self, config: Config):
        self.init(config=config)

    def init(self, config: Config):
        self.tiles = []
        self.animals = []
        self.new_animals = []
        self.animal_ID = 0
        self.x_size = config.grid_xsize
        self.y_size = config.grid_ysize
        self.plant_regeneration_ratio = config.plant_regeneration_ratio
        self.max_plant_supply = config.max_plant_supply
        self.minimal_reproduction_energy = config.minimal_reproduction_energy

        for x in range(self.x_size):
            self.tiles.append([])
            for _ in range(self.y_size):
                self.tiles[x].append(MapTile())
        self.init_animals(config.n_predator, config.n_prey, config.base_animal_energy)
    
    def init_animals(self, n_predator, n_prey, base_animal_energy):
        for _ in range(n_predator):
            while True:
                x = randrange(0,self.x_size)
                y = randrange(0,self.y_size)
                if self.tiles[x][y].get_render_value() == 0:
                    break

            self.add_animal(x=x, y=y, init_energy=base_animal_energy, species=Species.PREDATOR)

        for _ in range(n_prey):
            while True:
                x = randrange(0,self.x_size)
                y = randrange(0,self.y_size)
                if self.tiles[x][y].get_render_value() == 0:
                    break

            self.add_animal(x=x, y=y, init_energy=base_animal_energy, species=Species.PREY)

    def add_animal(self, x: int, y: int, init_energy: int, species: int):
        self.animal_ID += 1
        a = Animal(x=x, y=y, init_energy=init_energy, species=species, id=self.animal_ID, map=self)
        self.tiles[x][y].put_animal(a)
        self.animals.append(a)
    
    def add_child(self, x: int, y: int, init_energy: int, species: int):
        self.animal_ID += 1
        self.new_animals.append(Animal(x=x, y=y, init_energy=init_energy, species=species, id=self.animal_ID, map=self))

    def get_map_for_render(self):
        render_map = np.zeros((self.x_size, self.y_size), dtype=np.int8)

        for x in range(self.x_size):
            for y in range(self.y_size):
                render_map[x][y] = self.tiles[x][y].get_render_value()
        
        return render_map
    
    def next_turn(self):
        self._clean_dead_animals()
        self._move_animals()
        self._process_interactions()
        self._put_newborns_on_map()
        self._process_plants_eating_and_growing()
    
    def _clean_dead_animals(self):
        alive: list[AbstractAnimal] =[]
        dead: list[AbstractAnimal] = []
        for animal in self.animals:
            dead.append(animal) if animal.isDead else alive.append(animal)
        
        for animal in dead:
            x, y = animal.get_position()
            self.tiles[x][y].remove_animal(animal)
        self.animals = alive

    def _move_animals(self):
        for a in self.animals:
            old_x, old_y = a.get_position()
            direction = a.choose_direction()
            a.move(direction=direction, gridxsize=self.x_size, gridysize=self.y_size)
            new_x, new_y = a.get_position()
            if not (new_x == old_x and new_y == old_y):
                self.tiles[old_x][old_y].remove_animal(a)
                self.tiles[new_x][new_y].put_animal(a)
    
    def _process_interactions(self):
        interacted = {}
        for animal in self.animals:
            interacted[animal.id] = False
        
        for animal in self.animals:
            if not interacted[animal.id]:
                x, y = animal.get_position()
                if len(self.tiles[x][y].animals) > 1:
                    for i in range(len(self.tiles[x][y].animals)//2):
                        self.tiles[x][y].animals[i].interact(self.tiles[x][y].animals[i+1])
                        interacted[self.tiles[x][y].animals[i].id] = True
                        interacted[self.tiles[x][y].animals[i+1].id] = True
    
    def _put_newborns_on_map(self):
        for new_born in self.new_animals:
            x, y = new_born.get_position()
            self.animals.append(new_born)
            self.tiles[x][y].put_animal(new_born)
        self.new_animals.clear()
    
    def _process_plants_eating_and_growing(self):
        interacted = {}
        for animal in self.animals:
            interacted[animal.id] = False
        
        for animal in self.animals:
            if not interacted[animal.id]:
                x, y = animal.get_position()
                prey_on_tile_count = 0
                for a in self.tiles[x][y].animals:
                    interacted[a.id] = True
                    if a.species == Species.PREY:
                        prey_on_tile_count += 1
                current_plant_supply = self.tiles[x][y].plant_supply // 1
                if current_plant_supply > 1 and prey_on_tile_count > 0:

                    if current_plant_supply <= prey_on_tile_count:
                        supply = 1
                        i = 0
                        for a in self.tiles[x][y].animals:
                            if a.species == Species.PREY:
                                a.energy += supply
                                i += 1
                            if i >= current_plant_supply:
                                break

                    else:
                        general_supply = current_plant_supply / prey_on_tile_count
                        supply = general_supply + current_plant_supply % prey_on_tile_count
                        for a in self.tiles[x][y].animals:
                            if a.species == Species.PREY:
                                a.energy += supply
                                supply = general_supply

                self.tiles[x][y].plant_supply = 0.0

        for tiles_row in self.tiles:
            for tile in tiles_row:
                tile.plant_supply = min(tile.plant_supply + self.plant_regeneration_ratio, self.max_plant_supply)
    
    def get_submap(self, x: int, y: int, radius: int) -> list[list[MapTile]]:
        result_tiles: list[list[MapTile]] = []
        for i in range(max(x-radius, 0), min(x+radius+1, self.x_size - 1)):
            row: list[MapTile] = []
            for j in range(max(y-radius, 0), min(y+radius+1, self.y_size - 1)):
                row.append(self.tiles[i][j])
            result_tiles.append(row)
        return result_tiles

    @staticmethod
    def get_n_prey():
        return Animal.n_prey

    @staticmethod
    def get_n_predators():
        return Animal.n_predator

    def get_n_grass(self):
        return sum(tile.get_n_plants() for row in self.tiles for tile in row)
