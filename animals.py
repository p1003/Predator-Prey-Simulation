from enum import IntEnum

class Species(IntEnum):
    PREY = 1
    PREDATOR = 2

class Directions(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4

class Animal:
    """
    Tracks the animal's position, energy, species (rabbit/fox) and state (live/dead).
    """

    def __init__(self, x0, y0, init_energy, species, id):
        self.x = x0
        self.y = y0
        self.energy = init_energy
        self.species = species
        self.id = id
        self.isDead = False


    def interact(self, other):
        """
        Interact with another animal:
            - If they're from the same species, ignore each other.
            - Fox eats rabbit.
        """
        if self.species == Species.PREY and other.species == Species.PREDATOR:
            self.die()

        elif self.species == Species.PREDATOR and other.species == Species.PREY:
            other.die()



    def die(self):
        "R.I.P"
        self.isDead = True


    def move(self, direction, gridxsize, gridysize):
        """Move a step on the grid. Each step consumes 1 energy; if no energy left, die.
        If hitting the bounds of the grid, "bounde back", step to the opposite direction insetad.

        Arguments:
            direction {int} -- direction to move: UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3, STAY: 4
        """
        self.energy -= 1

        if direction == Directions.LEFT:
            self.x += 1 if self.x > 0 else -1   #"bounce back"
        if direction == Directions.RIGHT:
            self.x -= 1 if self.x < gridxsize-1 else -1
        if direction == Directions.UP:
            self.y += 1 if self.y < gridysize-1 else -1
        if direction == Directions.DOWN:
            self.y -= 1 if self.y > 0 else -1
        if direction == Directions.STAY:
            pass

        if self.energy <= 0:
            self.die()          #R.I.P.

    def get_position(self):
        return self.x, self.y