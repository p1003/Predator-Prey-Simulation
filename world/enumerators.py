from enum import IntEnum

class Species(IntEnum):
    PREY = 0
    PREDATOR = 1

class Directions(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4