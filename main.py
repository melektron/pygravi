"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter) and MrFlunter (Florian Unterpertinger)
www.elektron.work
02.05.22 18:44


Main file for gravity sim
"""


import tkinter.ttk as ttk
import tkinter as tk
import classes.render_frame
import classes.config_frame

import classes.antiblurr



class Window(tk.Tk):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)

        self.render_frame = classes.render_frame.RenderFrame(self)
        self.render_frame.config(width=20)
        self.render_frame.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

        self.config_frame = classes.config_frame.ConfigFrame(self)
        self.config_frame.config(width=100)
        self.config_frame.grid(row=1, column=2, sticky="NSEW", padx=5, pady=5)

if __name__ == "__main__":
    mywindow = Window()
    mywindow.mainloop()
