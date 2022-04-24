from __future__ import annotations

from typing import TYPE_CHECKING

from world.animals import Animal

if TYPE_CHECKING:
    from map import Map


class Statistics:
    """
    Class responsible for calculating various map statistics
    """

    def __init__(self, world_map: Map):
        self.world_map = world_map

    @staticmethod
    def get_n_prey():
        return Animal.n_prey

    @staticmethod
    def get_n_predators():
        return Animal.n_predator

    def get_n_grass(self):
        return sum(tile.get_n_plants() for row in self.world_map.tiles for tile in row)
