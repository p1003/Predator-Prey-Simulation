import tkinter as tk

from config import Config
from gui.config_menu_window import ConfigMenuWindow
from gui.simulation_frame import SimulationFrame
from gui.utils import center_window
from world import World


class MainWindow:
    def __init__(self, config: Config, world: World):
        self.config = config
        self.world = world
        self.root = None
        self.init()

    def init(self):
        config_menu_window = ConfigMenuWindow(self.config, self.world)
        config_menu_window.start_loop()

        self.world.init(self.config)

        self.root = tk.Tk()
        self.root.title('Simulation')
        self.root.protocol("WM_DELETE_WINDOW", exit)

        SimulationFrame(self)

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        center_window(self.root)

        self.start_loop()

    def reinit(self):
        self.root.quit()
        self.root.destroy()
        self.init()

    def start_loop(self):
        self.root.mainloop()
