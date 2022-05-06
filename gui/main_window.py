import tkinter as tk

import matplotlib

from config import Config
from gui.config_menu_window import ConfigMenuWindow
from gui.simulation_frame import SimulationFrame
from gui.statistics_frame import StatisticsFrame
from gui.utils import center_window, SimulationTimer
from world import Map


class MainWindow:
    def __init__(self, config: Config, map: Map):
        self.config = config
        self.map = map

        self.refresh_complex = True

        self.root = None

        self.simulation_timer = None

        self.simulation_frame = None
        self.statistics_frame = None

        matplotlib.rcParams.update({'font.size': 8})

        self.init()

    def init(self):
        config_menu_window = ConfigMenuWindow(self.config, self.map)
        config_menu_window.start_loop()

        self.map.init()

        self.root = tk.Tk()
        self.root.title('Simulation')
        self.root.protocol("WM_DELETE_WINDOW", exit)

        self.simulation_timer = SimulationTimer(self._next_turn_update)
        self.simulation_timer.start()

        self.simulation_frame = SimulationFrame(self)
        self.statistics_frame = StatisticsFrame(self)

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

    def _next_turn_update(self):
        self.map.next_turn()

        self.statistics_frame.next_turn_update(self.refresh_complex)
        self.simulation_frame.next_turn_update(self.refresh_complex)
