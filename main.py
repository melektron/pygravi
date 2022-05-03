"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter) and MrFlunter (Florian Unterpertinger)
www.elektron.work
02.05.22 18:44


Main file for gravity sim
"""


import tkinter.ttk as ttk
import tkinter as tk
import classes.config as config
import classes.render_frame
import classes.config_frame
from classes.sim_space import sim_space

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

        self.after(config.dyn.framedelay, self.render_objects)

    def render_objects(self) -> None:
        # Render Start
        for obj in sim_space.objects:
            self.render_frame.render_object(obj)
        # Render End
        # recall render after x time
        self.after(config.dyn.framedelay, self.render_objects)


if __name__ == "__main__":
    sim_space.load_objects(config.user.objects)
    
    print(sim_space.objects)
    mywindow = Window()
    mywindow.mainloop()
