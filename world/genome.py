from __future__ import annotations

from random import uniform

from config import Config

GENE_NAMES = [
    'View range',
    'Energy consumption ratio',
    'Max animal energy',
    'Fear of predators',
    'Eating over mating ratio'
]
N_GENES = len(GENE_NAMES)

class Genome:
    """"""

    def __init__(self,
                 viewrange: float = 1.,
                 energy_consumption_ratio: float = 1.,
                 max_animal_energy: int = 150,
                 fear_of_predator_ratio: float = 1.,
                 eating_over_mating_ratio: float = 1.,
                 config: Config = None
                 ):
        if config is not None:
            self.viewrange = (config.viewrange_range[0] + config.viewrange_range[1]/2)
            self.energy_consumption_ratio = (config.energy_consumption_ratio_range[0] + config.energy_consumption_ratio_range[1]/2)
            self.max_animal_energy = (config.max_animal_energy[0] + config.max_animal_energy[1]/2)
            self.fear_of_predator_ratio = (config.fear_of_predator_ratio[0] + config.fear_of_predator_ratio[1]/2)
            self.eating_over_mating_ratio = (config.eating_over_mating_ratio[0] + config.eating_over_mating_ratio[1]/2)
        else:
            self.viewrange = viewrange
            self.energy_consumption_ratio = energy_consumption_ratio
            self.max_animal_energy = max_animal_energy
            self.fear_of_predator_ratio = fear_of_predator_ratio
            self.eating_over_mating_ratio = eating_over_mating_ratio
    
    def calculate_energy_consumption(self) -> float:
        return (self.viewrange) * self.energy_consumption_ratio

    def get_genes(self) -> list[float]:
        return [
            self.viewrange,
            self.energy_consumption_ratio,
            self.max_animal_energy,
            self.fear_of_predator_ratio,
            self.eating_over_mating_ratio
        ]
    
    @staticmethod
    def _mutate_gene(gene: float , config: Config, is_additive: bool) -> float:
        if is_additive:
            return max(gene + round(uniform(-config.mutation_ratio, config.mutation_ratio), 3), 0.)
        return gene * (1. + round(uniform(-config.mutation_ratio, config.mutation_ratio), 3))
    
    @staticmethod
    def combined_genome(first: Genome, second: Genome, config: Config) -> Genome:
        if not config.simulate_genomes:
            return first.get_genes()
        first_genes = first.get_genes()
        second_genes = second.get_genes()

        # below value is ugly cheat: genomes below 3rd index mutate additively, equal or higher multiplicatively
        arbitral_var= 3

        new_genes = []
        for i in range(len(first_genes)):
            new_genes.append(Genome._mutate_gene(gene=(first_genes[i] + second_genes[i])/2, config=config, is_additive=i<arbitral_var))
        
        gene_ranges = config.get_gene_ranges()

        return Genome(
            viewrange=max(gene_ranges[0][0], min(gene_ranges[0][1], new_genes[0])),
            energy_consumption_ratio=max(gene_ranges[1][0], min(gene_ranges[1][1], new_genes[1])),
            max_animal_energy=max(gene_ranges[2][0], min(gene_ranges[2][1], new_genes[2])),
            fear_of_predator_ratio=max(gene_ranges[3][0], min(gene_ranges[3][1], new_genes[3])),
            eating_over_mating_ratio=max(gene_ranges[4][0], min(gene_ranges[4][1], new_genes[4])),
        )
