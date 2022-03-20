import tkinter as tk
from sys import exit
from tkinter import messagebox


def show_error(error_message):
    """
    Show a window with an error.
    """
    messagebox.showerror('Error', error_message)
    exit()


def show_askyesno(title, message):
    """
    Show a window with yes/no quesion.
    """
    return messagebox.askyesno(title, message)


def center_window(root: tk.Tk):
    """
    Place the window near the center of the screen.
    """
    # window_width = root.winfo_reqwidth()
    # window_height = root.winfo_reqheight()
    window_width, window_height = [int(val) for val in root.geometry().split('+')[0].split('x')]

    position_right = int(root.winfo_screenwidth() // 3 - window_width / 2)
    position_down = int(root.winfo_screenheight() // 3 - window_height / 2)

    root.geometry(f'+{position_right}+{position_down}')
