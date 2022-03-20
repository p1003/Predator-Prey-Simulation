import tkinter as tk
from tkinter import ttk

from config import Config
from gui.utils import center_window
from world import World


class ConfigMenuWindow:
    def __init__(self, config: Config, world: World):
        self.world = world
        self.config = config

        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.title('Config')
        self.root.protocol("WM_DELETE_WINDOW", exit)

        # config frame
        config_frame = ttk.Frame(self.root)
        row = 0

        # map size
        label_map_size = ttk.Label(config_frame, text='Map size: ')
        # TODO: only squares?
        self.var_map_size = tk.IntVar(config_frame, self.config.grid_xsize)
        # TODO: take from config?
        scale_map_size = tk.Scale(config_frame, from_=10, to=200, orient='horizontal', variable=self.var_map_size,
                                  tickinterval=190)

        label_map_size.grid(sticky='w', row=row, column=0, pady=5)
        scale_map_size.grid(row=row, column=1, padx=5)
        row += 1

        # predator count
        self.var_predator_count = tk.IntVar(value=self.config.n_predator)
        row = self._add_row_entry(config_frame, row, 'Predator count: ', self.var_predator_count)

        # prey count
        self.var_prey_count = tk.IntVar(value=self.config.n_prey)
        row = self._add_row_entry(config_frame, row, 'Prey count: ', self.var_prey_count)

        # base animal energy
        self.var_base_energy = tk.IntVar(value=self.config.base_animal_energy)
        row = self._add_row_entry(config_frame, row, 'Base animal energy: ', self.var_base_energy)

        config_frame.pack()

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

    @staticmethod
    def _add_row_entry(config_frame, row, text, textvariable):
        label = ttk.Label(config_frame, text=text)
        spinbox = ttk.Spinbox(config_frame, from_=0, to=99999999, textvariable=textvariable, width=5)

        label.grid(sticky='w', row=row, column=0, pady=5)
        spinbox.grid(row=row, column=1)

        return row + 1

    def _config_update(self):
        # TODO: square?
        self.config.grid_xsize = self.var_map_size.get()
        self.config.grid_ysize = self.var_map_size.get()
        self.config.n_predator = self.var_predator_count.get()
        self.config.n_prey = self.var_prey_count.get()
        self.config.base_animal_energy = self.var_base_energy.get()

    def _button_run_command(self):
        self._config_update()

        self.root.quit()
        self.root.destroy()

    def _button_reset_command(self):
        # TODO: take from some JSON?
        self.var_map_size.set(self.config.grid_xsize)
        self.var_predator_count.set(self.config.n_predator)
        self.var_prey_count.set(self.config.n_prey)

    def _button_save(self):
        self._config_update()
        # TODO: save to some JSON
