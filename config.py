class Config:
    """
    Simulation Config
    """

    def __init__(self):
        self.n_predator = 15
        self.n_prey = 30
        self.grid_size = 30
        self.base_animal_energy = 100
        self.plant_regeneration_ratio = 0.2
        self.max_plant_supply = 15
        self.minimal_reproduction_energy = 30

        self.simulate_genomes = True
        self.viewrange_range = (0, 5)
        self.energy_consumption_ratio_range = (0.5, 1.5)
        self.max_animal_energy_range = (100, 200)
        self.fear_of_predator_ratio_range = (0.5, 1.5)
        self.eating_over_mating_ratio_range = (0.5, 1.5)

        self.food_efficiency_ratio = 0.5

        self.mutation_ratio = 0.05

    def get_gene_ranges(self):
        return [self.viewrange_range, self.energy_consumption_ratio_range, self.max_animal_energy_range,
                self.fear_of_predator_ratio_range, self.eating_over_mating_ratio_range]

    def set_gene_ranges(self, vierwange_range, energy_consumption_ratio_range, max_animal_energy_range,
                        fear_of_predator_ratio_range, eating_over_mating_ratio_range):
        self.viewrange_range = vierwange_range
        self.energy_consumption_ratio_range = energy_consumption_ratio_range
        self.max_animal_energy_range = max_animal_energy_range
        self.fear_of_predator_ratio_range = fear_of_predator_ratio_range
        self.eating_over_mating_ratio_range = eating_over_mating_ratio_range
