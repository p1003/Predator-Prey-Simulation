from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from config import Config
from world.animals import Animal
from world.enumerators import Species
from world.genome import N_GENES

if TYPE_CHECKING:
    from map import Map


class Statistics:
    """
    Class responsible for calculating various map statistics
    """

    def __init__(self, config: Config, world_map: Map):
        self.config = config
        self.world_map = world_map

    @staticmethod
    def get_n_prey():
        return Animal.n_prey

    @staticmethod
    def get_n_predators():
        return Animal.n_predator

    def get_n_grass(self):
        return sum(tile.get_n_plants() for row in self.world_map.tiles for tile in row)

    def get_gene_arrays(self):
        prey_genes = [[] for _ in range(N_GENES)]
        predator_genes = [[] for _ in range(N_GENES)]

        for animal in self.world_map.animals:
            if animal.species == Species.PREY:
                current_genes = prey_genes
            else:
                current_genes = predator_genes

            animal_genes = animal.genome.get_genes()
            for i in range(N_GENES):
                current_genes[i].append(animal_genes[i])

        prey_genes = [np.array(genes) for genes in prey_genes]
        predator_genes = [np.array(genes) for genes in predator_genes]

        return prey_genes, predator_genes

    def get_energies(self):
        prey_energies, predator_energies = [], []
        for animal in self.world_map.animals:
            if animal.species == Species.PREY:
                prey_energies.append(animal.energy)
            else:
                predator_energies.append(animal.energy)

        return prey_energies, predator_energies
