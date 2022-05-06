# TODO: add cost (energy)
class Genome:
    """"""

    def __init__(self, viewrange: float = 1., energy_consumption_ratio: float = 1.):
        self.viewrange = viewrange
        self.energy_consumption_ratio = energy_consumption_ratio
    
    def calculate_energy_consumption(self) -> float:
        # TODO: check if this works
        return (self.viewrange - 1.) * self.energy_consumption_ratio

    def get_genes(self) -> list[float]:
        return [
            self.viewrange,
            self.energy_consumption_ratio
        ]
