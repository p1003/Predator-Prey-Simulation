from __future__ import annotations

import numpy as np
from config import Config
from abc import ABC, abstractmethod

from world.enumerators import Species

class AbstractAnimal(ABC):
    x: int
    y: int
    energy: int
    species: Species
    id: int
    isDead: bool
    viewrange: int
    map: AbstractMap

    @abstractmethod
    def interact(self, other: AbstractAnimal):
        pass

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def move(self, direction, gridxsize, gridysize):
        pass

    @abstractmethod
    def choose_direction(self):
        pass

    @abstractmethod
    def get_position(self):
        pass

class AbstractMapTile(ABC):
    animals: list[AbstractAnimal]
    plant_supply: float

    @abstractmethod
    def put_animal(self, a: AbstractAnimal):
        pass
    
    @abstractmethod
    def remove_animal(self, a_to_remove: AbstractAnimal):
        pass

    @abstractmethod
    def get_render_value(self):
        pass

class AbstractMap(ABC):
    tiles: list[list[AbstractMapTile]]
    animals: list[AbstractAnimal]
    new_animals: list[AbstractAnimal]
    animal_ID: int
    x_size: int
    y_size: int
    plant_regeneration_ratio: float

    @abstractmethod
    def init(self, config: Config):
        pass

    @abstractmethod
    def init_animals(self, n_predator, n_prey):
        pass

    @abstractmethod
    def add_animal(self, x: int, y: int, init_energy: int, species: int):
        pass

    @abstractmethod
    def add_child(self, x: int, y: int, init_energy: int, species: int):
        pass

    @abstractmethod
    def get_map_for_render(self):
        pass

    @abstractmethod
    def next_turn(self):
        pass

    @abstractmethod
    def get_submap(self, x: int, y: int, radius: int) -> list[list[AbstractMapTile]]:
        pass
