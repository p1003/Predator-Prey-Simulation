class Config:
    """
    Simulation Config
    """
    
    def __init__(self):
        self.n_predator = 15
        self.n_prey = 30
        self.grid_xsize = 30
        self.grid_ysize = 30
        self.base_animal_energy = 100
        self.plant_regeneration_ratio = 0.2
        self.max_plant_supply = 15.0
        self.minimal_reproduction_energy = 30
        