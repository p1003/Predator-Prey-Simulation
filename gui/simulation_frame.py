from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure

from gui.utils import show_askyesno

if TYPE_CHECKING:
    from gui.main_window import MainWindow


class SimulationFrame:
    GRASS_CMAP = 'YlGn'
    GRASS_CMAP_START = 0.2
    GRASS_CMAP_END = 0.8
    PREY_COLOR = 'royalblue'
    PREDATOR_COLOR = 'red'

    def __init__(self, main_window: MainWindow):
        self.main_window = main_window
        root = main_window.root
        self.config = main_window.config
        self.map = main_window.map
        self.simulation_timer = main_window.simulation_timer

        self.cmap = self._init_cmap()

        frame = ttk.Frame(root, relief='groove', borderwidth=3)

        # map
        self.fig = Figure(figsize=(5, 5))

        self.plot = self.fig.add_subplot(111)
        self.plot.pcolor(self.map.get_map_for_render(), cmap=self.cmap, vmin=0,
                         vmax=2 + self.config.max_plant_supply)

        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        # options frame
        options_frame = ttk.Frame(frame, relief='ridge', borderwidth=2)

        button_start = ttk.Button(options_frame, text='Start', command=self._button_start_command)
        button_start.pack(side='left')

        button_stop = ttk.Button(options_frame, text='Stop', command=self._button_stop_command)
        button_stop.pack(side='left')

        self.var_simulation_speed = tk.IntVar(value=0)
        scale_simulation_speed = ttk.Scale(options_frame, orient='horizontal', from_=-2, to=14,
                                           variable=self.var_simulation_speed, command=self._update_simulation_speed)
        scale_simulation_speed.pack(side='left')

        button_next_turn = ttk.Button(options_frame, text='Next turn', command=self._button_next_turn_command)
        button_next_turn.pack(side='left')

        button_reset = ttk.Button(options_frame, text='Reset', command=self._button_reset_command)
        button_reset.pack(side='left')

        self.button_refresh = tk.Button(options_frame, text='Refresh', command=self._button_refresh_command, bd=1,
                                        relief=tk.GROOVE, width=6, fg='white', bg='#007aff')
        self.button_refresh.pack(side='left')

        options_frame.pack(padx=2, pady=2)

        frame.pack(side='right', expand=True, fill='both')

    def next_turn_update(self, refresh_complex=True):
        if refresh_complex:
            self.plot.clear()
            self.plot.pcolor(self.map.get_map_for_render(), cmap=self.cmap, vmin=0,
                             vmax=2 + self.config.max_plant_supply)

            self.fig.gca().set_xticks([])
            self.fig.gca().set_yticks([])

            self.canvas.draw()

    def refresh(self):
        self.next_turn_update()

    def _init_cmap(self):
        grass_cmap = plt.get_cmap(SimulationFrame.GRASS_CMAP)
        inc = (SimulationFrame.GRASS_CMAP_END - SimulationFrame.GRASS_CMAP_START) / (self.config.max_plant_supply + 1)
        grass_cmap_list = [grass_cmap(x) for x in
                           np.arange(SimulationFrame.GRASS_CMAP_START, SimulationFrame.GRASS_CMAP_END + inc / 2, inc)]

        return ListedColormap([SimulationFrame.PREY_COLOR, SimulationFrame.PREDATOR_COLOR] + grass_cmap_list)

    def _button_next_turn_command(self):
        self.simulation_timer.trigger_action()

    def _button_start_command(self):
        self.simulation_timer.start_timer()

    def _button_stop_command(self):
        self.simulation_timer.stop_timer()

    def _update_simulation_speed(self, value):
        timeout = 2 ** -self.var_simulation_speed.get()
        self.simulation_timer.update_timeout(timeout)

    def _button_reset_command(self):
        was_running = self.simulation_timer.is_running()
        self.simulation_timer.stop_timer()
        if show_askyesno('Reset', 'Are you sure want to abandon the current simulation and reset the settings?'):
            self.simulation_timer.kill()
            self.main_window.reinit()
        else:
            if was_running:
                self.simulation_timer.start_timer()

    def _button_refresh_command(self):
        self.main_window.refresh_complex = not self.main_window.refresh_complex
        if self.main_window.refresh_complex:
            self.main_window.refresh()
        if self.main_window.refresh_complex:
            self.button_refresh.config(bg='#007aff')
        else:
            self.button_refresh.config(bg='#bcbcbc')
