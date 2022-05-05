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
from classes.sim_space import sim_space
import classes.render_frame
import classes.config_frame
import classes.edit_frame
import classes.antiblurr



class Window(tk.Tk):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=3)
        #self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)

        self.edit_frame = classes.edit_frame.EditFrame(self, width=400)
        self.edit_frame.grid(row=1, column=0, padx=5, pady=5)

        self.render_frame = classes.render_frame.RenderFrame(self, width=300)
        self.render_frame.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

        self.config_frame = classes.config_frame.ConfigFrame(self, width=400)
        self.config_frame.grid(row=1, column=2, padx=5, pady=5)

        self.after(config.dyn.vframedelay, self.render_objects)

    def render_objects(self) -> None:
        # Render Start
        for obj in sim_space.objects:
            self.render_frame.render_object(obj)
        # Render End
        # recall render after x time
        self.after(config.dyn.vframedelay, self.render_objects)


if __name__ == "__main__":
    sim_space.load_objects(config.user.objects)
    sim_space.run_simulation()
    mywindow = Window()
    mywindow.mainloop()
    sim_space.stop_simulation()
