import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure

from gui.utils import show_askyesno


class SimulationFrame:
    CMAP = ListedColormap(['limegreen', 'yellow', 'red'])

    def __init__(self, main_window):
        self.main_window = main_window
        root = main_window.root
        self.map = main_window.map
        self.simulation_timer = main_window.simulation_timer

        frame = ttk.Frame(root, relief='groove', borderwidth=3)

        # map
        self.fig = Figure(figsize=(5, 5))

        self.plot = self.fig.add_subplot(111)
        self.plot.imshow(self.map.get_map_for_render(), cmap=SimulationFrame.CMAP)

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

        options_frame.pack(padx=2, pady=2)

        frame.pack(side='right', expand=True, fill='both')

    def next_turn_update(self):
        self.plot.clear()
        self.plot.imshow(self.map.get_map_for_render(), cmap=SimulationFrame.CMAP)

        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])

        self.canvas.draw()

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
