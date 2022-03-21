import tkinter as tk
from threading import Thread, Event
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure

from gui.utils import show_askyesno


class SimulationFrame:
    CMAP = ListedColormap(['limegreen', 'yellow', 'red'])

    def __init__(self, main_window):
        self.main_window = main_window
        self.world = self.main_window.world
        self.root = self.main_window.root

        # options frame
        options_frame = ttk.Frame(self.root, relief='ridge', borderwidth=2)

        button_start = ttk.Button(options_frame, text='Start', command=self._button_start_command)
        button_start.pack(side='left')

        button_stop = ttk.Button(options_frame, text='Stop', command=self._button_stop_command)
        button_stop.pack(side='left')

        self.var_simulation_speed = tk.IntVar(value=0)
        scale_simulation_speed = ttk.Scale(options_frame, orient='horizontal', from_=-2, to=14,
                                           variable=self.var_simulation_speed, command=self._update_simulation_speed)
        scale_simulation_speed.pack(side='left')

        button_next_turn = ttk.Button(options_frame, text='Next turn', command=self._next_turn_update)
        button_next_turn.pack(side='left')

        button_reset = ttk.Button(options_frame, text='Reset', command=self._button_reset_command)
        button_reset.pack(side='left')

        options_frame.pack(side='bottom', padx=2, pady=2)

        # simulation frame
        simulation_frame = ttk.Frame(self.root)

        self.fig = Figure(figsize=(4, 4))

        self.plot = self.fig.add_subplot(111)
        self.plot.imshow(self.world.map, cmap=SimulationFrame.CMAP)

        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        simulation_frame.pack(side='top', fill='both')

        # simulation timer
        class SimulationTimer(Thread):
            def __init__(self, action, timeout=1):
                Thread.__init__(self, daemon=True)
                self.action = action
                self.timeout = timeout

                self.can_run = Event()
                self.stopped = Event()

                self.killed = False

            def run(self):
                while True:
                    self.can_run.wait()
                    if self.killed:
                        break
                    while not self.stopped.wait(self.timeout):
                        self.action()

            def start_timer(self):
                self.stopped.clear()
                self.can_run.set()

            def stop_timer(self):
                self.can_run.clear()
                self.stopped.set()

            def is_running(self):
                return self.can_run.is_set()

            def kill(self):
                self.killed = True
                self.can_run.set()
                self.stopped.set()

            def update_timeout(self, timeout):
                self.timeout = timeout

        self.simulation_timer = SimulationTimer(self._next_turn_update)
        self.simulation_timer.stop_timer()
        self.simulation_timer.start()

    def _next_turn_update(self):
        self.world.next_turn()

        self.plot.clear()
        self.plot.imshow(self.world.get_map_for_render() , cmap=SimulationFrame.CMAP)

        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])

        self.canvas.draw()

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
