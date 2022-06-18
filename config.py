import json

PARAMETER_NAMES = ['Predator count', 'Prey count', 'Base animal energy', 'Grass regeneration ratio',
                   'Maximum grass units', 'Minimum reproduction energy', 'Food efficiency ratio']


class Config:
    """
    Simulation Config
    """

    def __init__(self):
        self.grid_size = 30

        self.n_predator = 15
        self.n_prey = 30
        self.base_animal_energy = 100
        self.plant_regeneration_ratio = 0.2
        self.max_plant_supply = 15
        self.minimal_reproduction_energy = 30
        self.food_efficiency_ratio = 0.5

        self.simulate_genomes = True
        self.viewrange_range = (1, 0, 5)
        self.energy_consumption_ratio_range = (1., 0.5, 1.5)
        self.max_animal_energy_range = (150, 100, 200)
        self.fear_of_predator_ratio_range = (1., 0.5, 1.5)
        self.eating_over_mating_ratio_range = (1., 0.5, 1.5)

        self.mutation_ratio = 0.05

    def save(self, file_name='config.json'):
        with open(file_name, 'w') as file:
            file.write(json.dumps(self, default=lambda o: o.__dict__))

    def load(self, file_name='config.json'):
        with open(file_name, 'r') as file:
            file_dict = json.load(file)
            for attr, value in file_dict.items():
                setattr(self, attr, value)

    def get_regular_parameters(self):
        return [self.n_predator, self.n_prey, self.base_animal_energy, self.plant_regeneration_ratio,
                self.max_plant_supply, self.minimal_reproduction_energy, self.food_efficiency_ratio]

    def set_regular_parameters(self, n_predator, n_prey, base_animal_energy, plant_regeneration_ratio,
                               max_plant_suppy, minimal_reproduction_energy, food_efficiency_ratio):
        self.n_predator = n_predator
        self.n_prey = n_prey
        self.base_animal_energy = base_animal_energy
        self.plant_regeneration_ratio = plant_regeneration_ratio
        self.max_plant_supply = max_plant_suppy
        self.minimal_reproduction_energy = minimal_reproduction_energy
        self.food_efficiency_ratio = food_efficiency_ratio

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
