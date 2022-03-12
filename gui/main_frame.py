import tkinter as tk
from tkinter import ttk

from world import World
from gui.simulation_frame import SimulationFrame


class MainFrame:
    def __init__(self, world: World):
        self.world = world

        self.root = tk.Tk()
        self.root.title('Simulation')

        self.simulation_frame = SimulationFrame(world, self.root)
        self._add_map_manipulation_frame()

    def start_loop(self):
        self.root.mainloop()

    def _add_map_manipulation_frame(self):
        frame = ttk.Frame(self.root)

        button_next_move = ttk.Button(frame, text='next turn', command=lambda: self._next_turn_command())
        button_next_move.pack()

        frame.pack()

    def _next_turn_command(self):
        self.world.next_turn()
        self.simulation_frame.update()
