from __future__ import annotations

from random import choice, random
from typing import TYPE_CHECKING

from config import Config
from world.enumerators import Species, Directions
from world.genome import Genome

if TYPE_CHECKING:
    from world import Map
    from world.map import MapTile
    from world.animals import Animal


class Animal:
    """
    Tracks the animal's position, energy, species (rabbit/fox) and state (live/dead).
    """
    n_prey = 0
    n_predator = 0

    def __init__(self, x: int, y: int, init_energy: int, species: Species, id: int, map: Map, config: Config, genome: Genome = Genome()):
        self.x = x
        self.y = y
        self.energy = init_energy
        self.species = species
        self.id = id
        self.isDead: bool = False
        self.map = map
        self.config = config
        self.genome = genome
        self.energy_consumption = self.genome.calculate_energy_consumption()

        if self.species == Species.PREY:
            Animal.n_prey += 1
        elif self.species == Species.PREDATOR:
            Animal.n_predator += 1
        else:
            raise ValueError(f'{self.species} is a wrong species')

    def interact(self, other: Animal):
        """
        """
        if self.species == other.species:
            if self.energy > self.config.minimal_reproduction_energy and other.energy > self.config.minimal_reproduction_energy:
                new_self_energy = self.energy // 3 * 2
                new_other_energy = other.energy // 3 * 2
                child_energy = (self.energy - new_self_energy) + (other.energy - new_other_energy)
                self.energy = new_self_energy
                other.energy = new_other_energy
                x, y = self.get_position()
                self.map.add_child(x=x, y=y, init_energy=child_energy, species=self.species)

        elif self.species == Species.PREY and other.species == Species.PREDATOR:
            self.die()
            other.energy += self.energy

        elif self.species == Species.PREDATOR and other.species == Species.PREY:
            other.die()
            self.energy += other.energy

    def die(self):
        if not self.isDead:
            self.isDead = True
            if self.species == Species.PREY:
                Animal.n_prey -= 1
            else:
                Animal.n_predator -= 1

    def move(self, direction, gridxsize, gridysize):
        """
        Move a step on the grid. Each step consumes 1 energy; if no energy left, die.
        If hitting the bounds of the grid, "bounde back", step to the opposite direction insetad.

        Arguments:
            direction {int} -- direction to move: UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3, STAY: 4
        """
        energy_int = int(self.energy_consumption)
        if random() > self.energy_consumption % 1:
            energy_int += 1
        self.energy = max(0, self.energy - energy_int)

        # TODO: check toroid map
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

    def choose_direction(self):
        if self.config.simulate_genomes:
            # TODO: different behavior for prey and predator
            x, y = self.get_position()
            neighbourhood: list[list[MapTile]] = self.map.get_submap(x=x, y=y, radius=int(self.genome.viewrange))
            # TODO: detection of other animals and food
            return choice(list(Directions))
        else:
            return choice(list(Directions))

    def get_position(self):
        return self.x, self.y

    @classmethod
    def reset_counts(cls):
        cls.n_prey = 0
        cls.n_predator = 0
