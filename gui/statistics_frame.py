import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from world import World


class PopulationGraphFrame:
    def __init__(self, root, world: World):
        self.world = world

        frame = ttk.Frame(root, relief='ridge', borderwidth=2)

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

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='x')

        frame.pack(expand=False, fill='both')

        # options frame
        options_frame = ttk.Frame(frame, relief='ridge', borderwidth=2)

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

        # redraw
        self._redraw()

    def update(self):
        self._update_next_turn()
        self._redraw()

    def _update_next_turn(self):
        self.x.append(self.n_turns)
        self.n_turns += 1
        self.n_prey.append(self.world.get_n_prey())
        self.n_predators.append(self.world.get_n_predators())
        self.n_grass.append(self.world.get_n_grass())

    def _redraw(self):
        self.plot.clear()

        plot_fun = self.plot.plot
        if self.n_turns == 1:
            plot_fun = self.plot.scatter

        marker = '.' if self.show_variables['Markers'].get() else None
        if self.show_variables['Prey'].get():
            plot_fun(self.x[self.n_last:], self.n_prey[self.n_last:], label='Prey', marker=marker, c='yellow')
        if self.show_variables['Predators'].get():
            plot_fun(self.x[self.n_last:], self.n_predators[self.n_last:], label='Predators', marker=marker, c='red')
        if self.show_variables['Grass'].get():
            plot_fun(self.x[self.n_last:], self.n_grass[self.n_last:], label='Grass', marker=marker, c='green')

        self.plot.set_title('Population graph')
        self.plot.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.21))
        self.plot.set_ylim(bottom=0)

        self.fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        self.fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

        self.canvas.draw()

    def _update_n_last(self, value):
        self.n_last = [-10, -20, -50, -100, -200, -400, -1000, None][self.var_n_last.get()]
        self._redraw()


class StatisticsFrame:
    def __init__(self, main_window):
        root = main_window.root
        world = main_window.world

        frame = ttk.Frame(root, relief='groove', borderwidth=3)

        self.population_graph = PopulationGraphFrame(frame, world)

        frame.pack(side='left', expand=True, fill='both')

    def next_turn_update(self):
        self.population_graph.update()
