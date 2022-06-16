from __future__ import annotations

from random import choice, random
from typing import TYPE_CHECKING

from config import Config
from world.enumerators import Species, Directions
from world.genome import Genome

import numpy as np

if TYPE_CHECKING:
    from world import Map
    from world.map import MapTile
    from world.animals import Animal


class Animal:
    n_prey = 0
    n_predator = 0

    def __init__(self, x: int, y: int, init_energy: int, species: Species, id: int, map: Map, config: Config, genome: Genome = None):
        if not Genome:
            self.genome = Genome(config=config)
        else:
            self.genome = genome
        self.x = x
        self.y = y
        self.energy = init_energy
        self.species = species
        self.id = id
        self.isDead: bool = False
        self.map = map
        self.config = config
        self.energy_consumption = self.genome.calculate_energy_consumption()

        if self.species == Species.PREY:
            Animal.n_prey += 1
        elif self.species == Species.PREDATOR:
            Animal.n_predator += 1
        else:
            raise ValueError(f'{self.species} is a wrong species')

    def interact(self, other: Animal):
        if self.species == other.species:
            if self.energy > self.config.minimal_reproduction_energy and other.energy > self.config.minimal_reproduction_energy:
                new_self_energy = self.energy // 3 * 2
                new_other_energy = other.energy // 3 * 2
                child_energy = (self.energy - new_self_energy) + (other.energy - new_other_energy)
                self.energy = new_self_energy
                other.energy = new_other_energy
                x, y = self.get_position()
                self.map.add_child(
                    x=x, y=y, init_energy=child_energy, species=self.species, 
                    genome=Genome.combined_genome(
                        first=self.genome,
                        second=other.genome,
                        config=self.config
                    ))

        elif self.species == Species.PREY and other.species == Species.PREDATOR:
            if not other.check_if_energy_over_max():
                self.die()
                other.energy += int(self.energy*self.config.food_efficiency_ratio)

        elif self.species == Species.PREDATOR and other.species == Species.PREY:
            if not self.check_if_energy_over_max():
                other.die()
                self.energy += int(other.energy*self.config.food_efficiency_ratio)

    def die(self):
        if not self.isDead:
            self.isDead = True
            if self.species == Species.PREY:
                Animal.n_prey -= 1
            else:
                Animal.n_predator -= 1

    def move(self, direction, gridxsize, gridysize):
        energy_int = int(self.energy_consumption)
        if random() > self.energy_consumption % 1 and self.energy_consumption != 1.:
            energy_int += 1
        self.energy = max(0, self.energy - energy_int)

        if direction == Directions.LEFT:
            self.x = (self.x + gridxsize - 1) % gridxsize
        if direction == Directions.RIGHT:
            self.x = (self.x + gridxsize + 1) % gridxsize
        if direction == Directions.UP:
            self.y = (self.y + gridysize - 1) % gridysize
        if direction == Directions.DOWN:
            self.y = (self.y + gridysize + 1) % gridysize
        if direction == Directions.STAY:
            pass

        if self.energy <= 0:
            self.die()  # R.I.P.

    def _calc_tile_choice_value(self, current_tile: MapTile) -> float:
        if not current_tile.is_empty():
            result = 0.0
            prey_n, predator_n = current_tile.get_animal_counts()
            if self.species == Species.PREY:
                result -= predator_n * self.genome.fear_of_predator_ratio
                result += prey_n / self.genome.eating_over_mating_ratio
                result += current_tile.get_n_plants() * self.genome.eating_over_mating_ratio
            else:
                result += predator_n / self.genome.eating_over_mating_ratio
                result += prey_n * self.genome.eating_over_mating_ratio
            return result

    def choose_direction(self) -> Directions:
        if not self.config.simulate_genomes:
            return choice(list(Directions))
        x, y = self.get_position()
        current_viewrange = int(self.genome.viewrange)
        if random() > self.genome.viewrange % 1 and self.genome.viewrange != 1.:
            current_viewrange += 1

        neighbourhood: list[list[MapTile]] = self.map.get_submap(x=x, y=y, radius=current_viewrange)

        n_size = current_viewrange*2 + 1

        directions_weights = [1., 1., 1., 1., 1.] # []
        for i in range(n_size):
            for j in range(n_size):
                tile_choice_value = self._calc_tile_choice_value(current_tile=neighbourhood[i][j])
                x_dist = abs(i-current_viewrange)
                y_dist = abs(j-current_viewrange)
                if x_dist == 0 and y_dist == 0:
                    directions_weights[4] = tile_choice_value
                    
                else:
                    x_direction: Directions
                    y_direction: Directions
                    x_weight = float(x_dist)/(x_dist + y_dist)
                    y_weight = float(y_dist)/(x_dist + y_dist)
                    distance_weight = 1./(pow(x_dist, 2) + pow(y_dist, 2))

                    if i > current_viewrange:
                        x_direction = Directions.RIGHT
                    elif i < current_viewrange:
                        x_direction = Directions.LEFT
                    else:
                        x_direction = Directions.STAY

                    if j > current_viewrange:
                        y_direction = Directions.DOWN
                    elif j < current_viewrange:
                        y_direction = Directions.UP
                    else:
                        y_direction = Directions.STAY
                    
                    directions_weights[x_direction.value] += tile_choice_value * x_weight * distance_weight
                    directions_weights[y_direction.value] += tile_choice_value * y_weight * distance_weight

        # below lines handles negative values
        for i in range(4):
            if directions_weights[i] < 0.:
                if i%2 == 0:
                    directions_weights[i+1] -= directions_weights[i]
                    directions_weights[i] = 0.
                else:
                    directions_weights[i-1] -= directions_weights[i]
                    directions_weights[i] = 0.
        
        if directions_weights[4] < 0.:
            for i in range(4):
                directions_weights[i] -= directions_weights[4]/4
            directions_weights[4] = 0.
        directions_weights = np.array(directions_weights)
        directions_weights /= directions_weights.sum()
        return Directions(np.random.choice(a=np.array([0, 1, 2, 3, 4]), size=1, p=directions_weights))

    def check_if_energy_over_max(self):
        return self.energy > int(self.genome.get_genes()[2])

    def get_position(self):
        return self.x, self.y

    @classmethod
    def reset_counts(cls):
        cls.n_prey = 0
        cls.n_predator = 0
