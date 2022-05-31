import tkinter as tk
from tkinter import ttk
from typing import Type

from config import Config
from gui.utils import center_window
from world import Map
from world.genome import GENE_NAMES


class RangeVar:
    def __init__(self, var_class: Type[tk.Variable], default_range: tuple[float, float]):
        self.low = var_class(value=default_range[0])
        self.high = var_class(value=default_range[1])

    def get(self):
        return self.low.get(), self.high.get()

    def set(self, range_: tuple[float, float]):
        self.low.set(range_[0])
        self.high.set(range_[1])


class GenomeConfigMenuFrame:
    def __init__(self, root, config: Config, world_map: Map):
        self.root = root
        self.config = config
        self.map = world_map

        frame = ttk.Frame(self.root, relief='groove', borderwidth=2)

        self.var_simulate_genomes = tk.BooleanVar(value=self.config.simulate_genomes)
        button_simulate_genomes = ttk.Checkbutton(frame, text='Simulate genomes', variable=self.var_simulate_genomes)
        button_simulate_genomes.pack()

        label_ranges = ttk.Label(frame, text='Gene ranges:')
        label_ranges.pack()

        # gene ranges
        ranges_frame = ttk.Frame(frame)
        self.row = 0
        self.gene_variables = []
        for gene_name, gene_range in zip(GENE_NAMES, self.config.get_gene_ranges()):
            if type(gene_range[0]) is int:
                var_type, inc = tk.IntVar, 1
            else:
                var_type, inc = tk.DoubleVar, 0.1
            var = RangeVar(var_type, gene_range)
            self._add_row_range_spinboxes(ranges_frame, gene_name + ': ', var, inc=inc)
            self.gene_variables.append(var)

        ranges_frame.pack()

        frame.pack()

    def config_update(self):
        self.config.simulate_genomes = self.var_simulate_genomes.get()
        self.config.set_gene_ranges(*[var.get() for var in self.gene_variables])

    def reset(self):
        self.var_simulate_genomes.set(self.config.simulate_genomes)
        for var, gene_range in zip(self.gene_variables, self.config.get_gene_ranges()):
            var.set(gene_range)

    def _add_row_range_spinboxes(self, frame, text, range_var, from_=0, to=99999999, inc=1.):
        label = ttk.Label(frame, text=text)
        spinbox_low = ttk.Spinbox(frame, from_=from_, to=to, textvariable=range_var.low, width=4, increment=inc)
        label_range_sign = ttk.Label(frame, text='-')
        spinbox_high = ttk.Spinbox(frame, from_=from_, to=to, textvariable=range_var.high, width=4, increment=inc)

        label.grid(sticky='w', row=self.row, column=0, pady=5)
        spinbox_low.grid(row=self.row, column=1, padx=2)
        label_range_sign.grid(row=self.row, column=2)
        spinbox_high.grid(row=self.row, column=3, padx=2)

        self.row += 1


class ConfigMenuWindow:
    def __init__(self, config: Config, world_map: Map):
        self.map = world_map
        self.config = config

        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.title('Config')
        self.root.protocol("WM_DELETE_WINDOW", exit)

        # config frame
        config_frame = ttk.Frame(self.root)
        self.row = 0

        # map size
        label_map_size = ttk.Label(config_frame, text='Map size: ')
        self.var_map_size = tk.IntVar(config_frame, self.config.grid_size)
        scale_map_size = tk.Scale(config_frame, from_=10, to=200, orient='horizontal', variable=self.var_map_size,
                                  tickinterval=190)

        label_map_size.grid(sticky='w', row=self.row, column=0, pady=5)
        scale_map_size.grid(row=self.row, column=1, padx=5)
        self.row += 1

        # predator count
        self.var_predator_count = tk.IntVar(value=self.config.n_predator)
        self._add_row_spinbox(config_frame, 'Predator count: ', self.var_predator_count)

        # prey count
        self.var_prey_count = tk.IntVar(value=self.config.n_prey)
        self._add_row_spinbox(config_frame, 'Prey count: ', self.var_prey_count)

        # base animal energy
        self.var_base_energy = tk.IntVar(value=self.config.base_animal_energy)
        self._add_row_spinbox(config_frame, 'Base animal energy: ', self.var_base_energy)

        # plant regeneration ratio
        self.var_plant_regen = tk.DoubleVar(value=self.config.plant_regeneration_ratio)
        self._add_row_spinbox(config_frame, 'Grass regeneration ratio: ', self.var_plant_regen, inc=0.1)

        # max grass
        self.var_max_grass = tk.IntVar(value=self.config.max_plant_supply)
        self._add_row_spinbox(config_frame, 'Maximum grass units: ', self.var_max_grass)

        # min reproduction energy
        self.var_min_reproduction_energy = tk.IntVar(value=self.config.minimal_reproduction_energy)
        self._add_row_spinbox(config_frame, 'Minimum reproduction energy: ', self.var_min_reproduction_energy)

        config_frame.pack()

        # config genome frame
        self.config_genome_frame = GenomeConfigMenuFrame(self.root, self.config, self.map)

        # control frame
        control_frame = ttk.Frame(self.root, relief='ridge', borderwidth=2)

        button_run = ttk.Button(control_frame, text='Run', command=self._button_run_command)
        button_run.pack(side='left')

        button_reset = ttk.Button(control_frame, text='Reset', command=self._button_reset_command)
        button_reset.pack(side='left')

        button_save = ttk.Button(control_frame, text='Save', command=self._button_save)
        button_save.pack(side='left')

        control_frame.pack(side='bottom', padx=2, pady=2)

        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.resizable(False, False)
        self.root.update()
        center_window(self.root)

    def start_loop(self):
        self.root.mainloop()

    def _add_row_spinbox(self, config_frame, text, textvariable, inc=1.):
        label = ttk.Label(config_frame, text=text)
        spinbox = ttk.Spinbox(config_frame, from_=0, to=99999999, textvariable=textvariable, width=5, increment=inc)

        label.grid(sticky='w', row=self.row, column=0, pady=5)
        spinbox.grid(row=self.row, column=1)

        self.row += 1

    def _config_update(self):
        self.config.grid_size = self.var_map_size.get()
        self.config.n_predator = self.var_predator_count.get()
        self.config.n_prey = self.var_prey_count.get()
        self.config.base_animal_energy = self.var_base_energy.get()
        self.config.plant_regeneration_ratio = self.var_plant_regen.get()
        self.config.max_plant_supply = self.var_max_grass.get()
        self.config.minimal_reproduction_energy = self.var_min_reproduction_energy.get()

        self.config_genome_frame.config_update()

    def _button_run_command(self):
        self._config_update()

        self.root.quit()
        self.root.destroy()

    def _button_reset_command(self):
        self.var_map_size.set(self.config.grid_size)
        self.var_predator_count.set(self.config.n_predator)
        self.var_prey_count.set(self.config.n_prey)
        self.var_base_energy.set(self.config.base_animal_energy)
        self.var_plant_regen.set(self.config.plant_regeneration_ratio)
        self.var_max_grass.set(self.config.max_plant_supply)
        self.var_min_reproduction_energy.set(self.config.minimal_reproduction_energy)

        self.config_genome_frame.reset()

    def _button_save(self):
        self._config_update()
