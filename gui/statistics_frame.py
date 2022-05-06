from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from gui.simulation_frame import SimulationFrame
from world import Map
from world.genome import N_GENES, GENE_NAMES
from world.statistics import Statistics

if TYPE_CHECKING:
    from gui.main_window import MainWindow


class PopulationGraphFrame:
    def __init__(self, root, world_map: Map):
        self.statistics = world_map.statistics

        self.frame = ttk.Frame(root, relief='ridge', borderwidth=2)

        # plot
        self.n_turns = 0
        self.x = []
        self.n_prey = []
        self.n_predators = []
        self.n_grass = []

        self.fig = Figure(figsize=(4, 3.1))

        self.plot = self.fig.add_subplot(111)
        self.plot.set_title('Population graph')

        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.15)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='x')

        # options frame
        options_frame = ttk.Frame(self.frame, relief='ridge', borderwidth=2)

        self.show_variables = {}
        for text in ['Prey', 'Predators', 'Grass', 'Markers']:
            self.show_variables[text] = tk.BooleanVar(value=True)
            button = ttk.Checkbutton(options_frame, text=text, variable=self.show_variables[text], command=self._redraw)
            button.pack(side='left')

        self.n_last = None
        self.var_n_last = tk.IntVar(value=7)
        scale_n_last = ttk.Scale(options_frame, orient='horizontal', from_=0, to=7, variable=self.var_n_last,
                                 command=self._update_n_last)
        scale_n_last.pack(side='left')

        options_frame.pack(side='bottom', padx=2, pady=2)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
        self._redraw()

    def update(self):
        self._update_next_turn()
        self._redraw()

    def _update_next_turn(self):
        self.x.append(self.n_turns)
        self.n_turns += 1
        self.n_prey.append(self.statistics.get_n_prey())
        self.n_predators.append(self.statistics.get_n_predators())
        self.n_grass.append(self.statistics.get_n_grass())

    def _redraw(self):
        self.plot.clear()

        plot_fun = self.plot.plot
        if self.n_turns == 1:
            plot_fun = self.plot.scatter

        marker = '.' if self.show_variables['Markers'].get() else None
        is_empty_plot = True
        if self.show_variables['Prey'].get():
            is_empty_plot = False
            plot_fun(self.x[self.n_last:], self.n_prey[self.n_last:], label='Prey', marker=marker,
                     c=SimulationFrame.PREY_COLOR)
        if self.show_variables['Predators'].get():
            is_empty_plot = False
            plot_fun(self.x[self.n_last:], self.n_predators[self.n_last:], label='Predators', marker=marker,
                     c=SimulationFrame.PREDATOR_COLOR)
        if self.show_variables['Grass'].get():
            is_empty_plot = False
            plot_fun(self.x[self.n_last:], self.n_grass[self.n_last:], label='Grass', marker=marker,
                     color=plt.get_cmap(SimulationFrame.GRASS_CMAP)(SimulationFrame.GRASS_CMAP_END))

        self.plot.set_title('Population graph')
        if not is_empty_plot:
            self.plot.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.21))
        self.plot.set_ylim(bottom=0)

        self.fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        self.fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

        self.canvas.draw()

    def _update_n_last(self, value):
        self.n_last = [-10, -20, -50, -100, -200, -400, -1000, None][self.var_n_last.get()]
        self._redraw()


class GeneHistogramsFrame:
    def __init__(self, root, statistics: Statistics, gene_name: str, gene_range: tuple[float, float],
                 prey_genes: list | np.array = None, predator_genes: list | np.array = None):
        self.root = root
        self.statistics = statistics
        self.gene_name = gene_name
        self.gene_range = gene_range
        self.prey_genes = prey_genes if prey_genes is not None else []
        self.predator_genes = predator_genes if predator_genes is not None else []

        self.frame = ttk.Frame(root, relief='ridge', borderwidth=2)

        self.fig = Figure(figsize=(4, 1.5))

        self.prey_plot = self.fig.add_subplot(1, 2, 1)
        self.predator_plot = self.fig.add_subplot(1, 2, 2)

        self.fig.suptitle(f'{self.gene_name} histogram')
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='x')

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
        self._redraw()

    def update(self, prey_genes: np.array, predator_genes: np.array):
        self.prey_genes = prey_genes
        self.predator_genes = predator_genes
        self._redraw()

    def _redraw(self):
        self.prey_plot.clear()
        self.prey_plot.set_title(f'Prey')
        self.predator_plot.clear()
        self.predator_plot.set_title(f'Predator')

        self.fig.suptitle(f'{self.gene_name} histogram')

        self.prey_plot.hist(self.prey_genes, bins=10, range=self.gene_range)
        self.predator_plot.hist(self.predator_genes, bins=10, range=self.gene_range)


class GenomeStatisticsFrame:
    def __init__(self, root, world_map: Map):
        self.statistics = world_map.statistics
        self.config = world_map.config
        self.gene_ranges = self.config.get_gene_ranges()

        self.frame = ttk.Frame(root, relief='groove', borderwidth=3)

        prey_gene_arrays, predator_gene_arrays = self.statistics.get_gene_arrays()
        self.gene_histograms = []
        for i in range(N_GENES):
            gene_histograms = GeneHistogramsFrame(self.frame, self.statistics, GENE_NAMES[i], self.gene_ranges[i],
                                                  prey_gene_arrays[i], predator_gene_arrays[i])
            gene_histograms.pack(fill='x')
            self.gene_histograms.append(gene_histograms)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def update(self):
        pass


class StatisticsFrame:
    def __init__(self, main_window: MainWindow):
        root = main_window.root
        map_ = main_window.map

        frame = ttk.Frame(root, relief='groove', borderwidth=3)

        self.population_graph_frame = PopulationGraphFrame(frame, map_)
        self.population_graph_frame.pack(side='right', anchor='n', expand=True, fill='x')

        self.all_genome_histograms_frame = GenomeStatisticsFrame(frame, map_)
        self.all_genome_histograms_frame.pack(side='left', expand=True, fill='both')

        frame.pack(side='left', expand=True, fill='both')

    def next_turn_update(self):
        self.population_graph_frame.update()
        self.all_genome_histograms_frame.update()
