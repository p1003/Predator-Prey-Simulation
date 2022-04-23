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