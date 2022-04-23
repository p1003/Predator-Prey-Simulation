from random import choice

from world.abstracts import AbstractMap, AbstractMapTile, AbstractAnimal
from world.enumerators import Species, Directions


class Animal(AbstractAnimal):
    """
    Tracks the animal's position, energy, species (rabbit/fox) and state (live/dead).
    """
    n_prey = 0
    n_predator = 0

    def __init__(self, x: int, y: int, init_energy: int, species: Species, id: int, map: AbstractMap):
        self.x = x
        self.y = y
        self.energy = init_energy
        self.species = species
        self.id = id
        self.isDead = False
        self.viewrange = 1
        self.map = map
        #TODO: self.genome = ...

        if self.species == Species.PREY:
            Animal.n_prey += 1
        elif self.species == Species.PREDATOR:
            Animal.n_predator += 1
        else:
            raise ValueError(f'{self.species} is a wrong species')

    def interact(self, other: AbstractAnimal):
        """
        """
        if self.species == other.species:
            if self.energy > self.map.minimal_reproduction_energy and other.energy > self.map.minimal_reproduction_energy:
                new_self_energy = self.energy//3 * 2
                new_other_energy = other.energy//3 * 2
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
        self.energy -= 1

        if direction == Directions.LEFT:
            self.x -= 1 if self.x > 0 else -1
        if direction == Directions.RIGHT:
            self.x += 1 if self.x < gridxsize-1 else -1
        if direction == Directions.UP:
            self.y += 1 if self.y < gridysize-1 else -1
        if direction == Directions.DOWN:
            self.y -= 1 if self.y > 0 else -1
        if direction == Directions.STAY:
            pass

        if self.energy <= 0:
            self.die()          #R.I.P.

    def choose_direction(self):
        x, y = self.get_position()
        neighbourhood: list[list[AbstractMapTile]] = self.map.get_submap(x=x, y=y, radius=self.viewrange)
        # TODO: detection of other animals and food
        return choice(list(Directions))

    def get_position(self):
        return self.x, self.y

    @classmethod
    def reset_counts(cls):
        cls.n_prey = 0
        cls.n_predator = 0

class Genome:
    """"""
