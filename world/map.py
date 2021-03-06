from random import randrange
from statistics import mode

import numpy as np

from config import Config
from world.animals import Animal
from world.enumerators import Species
from world.genome import Genome
from world.statistics import Statistics


class MapTile:
    """
    Class representing one tile of the map
    """

    def __init__(self):
        self.animals: list[Animal] = []
        self.plant_supply: float = 1.0

    def put_animal(self, a: Animal):
        self.animals.append(a)

    def remove_animal(self, a_to_remove: Animal):
        animals = self.animals
        self.animals = ([a for a in animals if a.id != a_to_remove.id])

    def get_render_value(self) -> int:
        if self.animals:  # animals - return the most frequent one; 0 - prey, 1 - predator
            return mode(animal.species for animal in self.animals)
        else:  # no animals - plants
            return 2 + self.get_n_plants()

    def is_empty(self) -> int:
        return len(self.animals) == 0

    def get_n_plants(self) -> int:
        return int(self.plant_supply)
    
    def get_animal_counts(self) -> tuple[int, int]:
        prey_n: int = 0
        predator_n: int = 0
        for animal in self.animals:
            if animal.species == Species.PREY:
                prey_n += 1
            else:
                predator_n += 1
        
        return prey_n, predator_n


class Map:
    """
    Class holding all entities on it
    """

    def __init__(self, config: Config):
        self.tiles: list[list[MapTile]] = None
        self.animals: list[Animal] = None
        self.new_animals: list[Animal] = None
        self.animal_ID: int = None
        self.config = config

        self.init()
        self.statistics = Statistics(self.config, self)

    def init(self):
        self.tiles = []
        self.animals = []
        self.new_animals = []
        self.animal_ID = 0

        self.tiles = [[MapTile() for _ in range(self.config.grid_size)] for _ in range(self.config.grid_size)]

        Animal.reset_counts()
        self._init_species(self.config.n_predator, Species.PREDATOR)
        self._init_species(self.config.n_prey, Species.PREY)

    def add_animal(self, x: int, y: int, init_energy: int, species: Species):
        self.animal_ID += 1
        a = Animal(x=x, y=y, init_energy=init_energy, species=species, id=self.animal_ID, map=self, config=self.config)
        self.tiles[x][y].put_animal(a)
        self.animals.append(a)

    def add_child(self, x: int, y: int, init_energy: int, species: Species, genome: Genome):
        self.animal_ID += 1
        self.new_animals.append(
            Animal(x=x, y=y, init_energy=init_energy, species=species, id=self.animal_ID, map=self, config=self.config, genome=genome))

    def get_map_for_render(self):
        return np.array([[tile.get_render_value() for tile in row] for row in self.tiles], dtype=np.int8)

    def next_turn(self):
        self._clean_dead_animals()
        self._move_animals()
        self._process_interactions()
        self._put_newborns_on_map()
        self._process_plants_eating_and_growing()

    def _init_species(self, n, species):
        for _ in range(n):
            while True:
                x = randrange(0, self.config.grid_size)
                y = randrange(0, self.config.grid_size)
                if self.tiles[x][y].is_empty():
                    break
            self.add_animal(x, y, self.config.base_animal_energy, species)

    def _clean_dead_animals(self):
        alive: list[Animal] = []
        dead: list[Animal] = []
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
            a.move(direction=direction, gridsize=self.config.grid_size)
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
                    for i in range(len(self.tiles[x][y].animals) // 2):
                        self.tiles[x][y].animals[i*2].interact(self.tiles[x][y].animals[i*2 + 1])
                        interacted[self.tiles[x][y].animals[i*2].id] = True
                        interacted[self.tiles[x][y].animals[i*2 + 1].id] = True

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
                eaters_ids = []
                for a in self.tiles[x][y].animals:
                    interacted[a.id] = True
                    if a.species == Species.PREY and not a.check_if_energy_over_max():
                        eaters_ids.append(a.id)
                current_plant_supply = self.tiles[x][y].plant_supply // 1
                if current_plant_supply > 1 and len(eaters_ids) > 0:

                    if current_plant_supply <= len(eaters_ids):
                        supply = 1
                        i = 0
                        for a in self.tiles[x][y].animals:
                            if a.id in eaters_ids:
                                a.energy = min(a.energy + supply, a.genome.max_animal_energy)
                                i += 1
                            if i >= current_plant_supply:
                                break

                    else:
                        general_supply = current_plant_supply / len(eaters_ids)
                        supply = general_supply + current_plant_supply % len(eaters_ids)
                        for a in self.tiles[x][y].animals:
                            if a.species == Species.PREY:
                                a.energy = min(a.energy + supply, a.genome.max_animal_energy)
                                supply = general_supply

                    self.tiles[x][y].plant_supply = 0.0

        for tiles_row in self.tiles:
            for tile in tiles_row:
                tile.plant_supply = min(tile.plant_supply + self.config.plant_regeneration_ratio,
                                        self.config.max_plant_supply)

    def get_submap(self, x: int, y: int, radius: int) -> list[list[MapTile]]:
        result_tiles: list[list[MapTile]] = []
        for i in range(x - radius, x + radius + 1):
            row: list[MapTile] = []
            for j in range(y - radius, y + radius + 1):
                x_size = self.config.grid_size
                y_size = self.config.grid_size
                row.append(self.tiles[(i + x_size) % x_size][(j + y_size) % y_size])
            result_tiles.append(row)
        return result_tiles
