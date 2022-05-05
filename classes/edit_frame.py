"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 11:51

The GUI frame on the left of the window for adding/remoing/selecting simulation objects

"""

import tkinter as tk
import tkinter.ttk as ttk
 
class EditFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)