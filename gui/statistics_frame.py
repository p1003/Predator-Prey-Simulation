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


class PopulationStatisticsFrame:
    def __init__(self, root, world_map: Map, statistics_frame: StatisticsFrame):
        self.statistics_frame = statistics_frame

        self.frame = ttk.Frame(root, relief='groove', borderwidth=3)

        # population graph
        self.population_graph_frame = PopulationGraphFrame(self.frame, world_map)
        self.population_graph_frame.pack(expand=False, fill='x')

        # gene histograms button
        self.button_gene_histograms = ttk.Button(self.frame, text='Show genome histograms',
                                                 command=self._button_gene_histograms_command)
        self.button_gene_histograms.pack(expand=False, fill='x')

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
        self._redraw()

    def update(self):
        self._redraw()

    def _redraw(self):
        self.population_graph_frame.update()

    def _button_gene_histograms_command(self):
        self.statistics_frame.negate_gene_histograms()
        if self.statistics_frame.show_gene_histograms:
            self.button_gene_histograms.config(text='Close genome histograms')
        else:
            self.button_gene_histograms.config(text='Show genome histograms')


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

        self.fig = Figure(figsize=(5, 1.6))

        self.prey_plot = self.fig.add_subplot(1, 2, 1)
        self.predator_plot = self.fig.add_subplot(1, 2, 2)

        self.fig.suptitle(f'{self.gene_name}')
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

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
        self.predator_plot.set_title(f'Predators')

        self.fig.suptitle(f'{self.gene_name}')

        self.prey_plot.hist(self.prey_genes, bins=10, range=self.gene_range)
        self.predator_plot.hist(self.predator_genes, bins=10, range=self.gene_range)

        self.canvas.draw()


class GenomeStatisticsFrame:
    def __init__(self, root, world_map: Map):
        self.statistics = world_map.statistics
        self.config = world_map.config
        self.gene_ranges = self.config.get_gene_ranges()

        self.prey_gene_arrays, self.predator_gene_arrays = self.statistics.get_gene_arrays()

        self.frame = ttk.Frame(root, relief='groove', borderwidth=3)

        self.genome_histograms = []
        for i in range(N_GENES):
            gene_histograms = GeneHistogramsFrame(self.frame, self.statistics, GENE_NAMES[i], self.gene_ranges[i])
            gene_histograms.pack(expand=True, fill='x')
            self.genome_histograms.append(gene_histograms)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
        self._redraw()

    def unpack(self):
        self.frame.pack_forget()

    def update(self):
        self.prey_gene_arrays, self.predator_gene_arrays = self.statistics.get_gene_arrays()
        self._redraw()

    def _redraw(self):
        for i, gene_histograms in enumerate(self.genome_histograms):
            gene_histograms.update(self.prey_gene_arrays[i], self.predator_gene_arrays[i])


class StatisticsFrame:
    def __init__(self, main_window: MainWindow):
        root = main_window.root
        map_ = main_window.map

        self.show_gene_histograms = False

        frame = ttk.Frame(root, relief='groove', borderwidth=3)

        self.population_statistics_frame = PopulationStatisticsFrame(frame, map_, self)
        self.population_statistics_frame.pack(side='right', expand=True, fill='both')

        self.genome_histograms_frame = GenomeStatisticsFrame(frame, map_)
        self.genome_histograms_frame.pack(side='left', expand=True, fill='both')
        self.genome_histograms_frame.unpack()

        frame.pack(side='left', expand=True, fill='both')

    def next_turn_update(self, refresh_complex=True):
        self.population_statistics_frame.update()
        if refresh_complex and self.show_gene_histograms:
            self.genome_histograms_frame.update()

    def negate_gene_histograms(self):
        self.show_gene_histograms = not self.show_gene_histograms
        if self.show_gene_histograms:
            self.genome_histograms_frame.pack()
        else:
            self.genome_histograms_frame.unpack()
