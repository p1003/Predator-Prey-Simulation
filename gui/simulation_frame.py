from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.colors import ListedColormap

from world import World


class SimulationFrame:
    def __init__(self, world: World, root):
        self.world = world
        self.root = root

        self.cmap = ListedColormap(['limegreen', 'yellow', 'red'])

        frame = ttk.Frame(self.root)

        self.fig = Figure(figsize=(5, 5), dpi=100)

        self.plot = self.fig.add_subplot(111)
        self.plot.imshow(self.world.map, cmap=self.cmap)

        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack()

        frame.pack()

    def update(self):
        self.plot.clear()
        self.plot.imshow(self.world.map, cmap=self.cmap)

        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])

        self.canvas.draw()
