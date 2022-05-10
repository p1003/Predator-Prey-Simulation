from __future__ import annotations

from random import uniform

from config import Config

N_GENES = 2
GENE_NAMES = [
    'View range',
    'Energy consumption ratio',
    'Fear of predators',
    'Eating over mating ratio'
]

# TODO: add cost (energy)
class Genome:
    """"""

    def __init__(self,
                 viewrange: float = 1.,
                 energy_consumption_ratio: float = 1.,
                 fear_of_predator_ratio: float = 1.,
                 eating_over_mating_ratio: float = 1.,
                 ):
        self.viewrange = viewrange
        self.energy_consumption_ratio = energy_consumption_ratio
        self.fear_of_predator_ratio = fear_of_predator_ratio
        self.eating_over_mating_ratio = eating_over_mating_ratio
    
    def calculate_energy_consumption(self) -> float:
        return (self.viewrange) * self.energy_consumption_ratio

    def get_genes(self) -> list[float]:
        return [
            self.viewrange,
            self.energy_consumption_ratio,
            self.fear_of_predator_ratio,
            self.eating_over_mating_ratio,
        ]
    
    @staticmethod
    def _mutate_gene(gene: float , config: Config, is_additive: bool) -> float:
        if is_additive:
            return max(gene + round(uniform(-config.mutation_ratio, config.mutation_ratio), 3), 0.)
        return gene * (1. + round(uniform(-config.mutation_ratio, config.mutation_ratio), 3))
    
    @staticmethod
    def combined_genome(first: Genome, second: Genome, config: Config) -> Genome:
        first_genes = first.get_genes()
        second_genes = second.get_genes()

        new_genes = []
        for i in range(len(first_genes)):
            new_genes.append(Genome._mutate_gene(gene=(first_genes[i] + second_genes[i])/2, config=config, is_additive=i<2))
        viewrange_min, viewrange_max = config.viewrange_range
        energy_consumption_ratio_min, energy_consumption_ratio_max = config.energy_consumption_ratio_range

        return Genome(
            viewrange=max(viewrange_min, min(viewrange_max, new_genes[0])),
            energy_consumption_ratio=max(energy_consumption_ratio_min, min(energy_consumption_ratio_max, new_genes[1])),
            fear_of_predator_ratio=new_genes[2],
            eating_over_mating_ratio=new_genes[3],
        )
