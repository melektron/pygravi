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
import classes.planets



class Window(tk.Tk):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=3)
        #self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)
        

        self.edit_frame = classes.edit_frame.EditFrame(self, width=350)
        self.edit_frame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
        self.edit_frame.grid_propagate(0)  # keep left column fixed size (width)

        self.render_frame = classes.render_frame.RenderFrame(self, width=300)
        self.render_frame.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

        self.config_frame = classes.config_frame.ConfigFrame(self, width=350)
        self.config_frame.grid(row=1, column=2, sticky="NS", padx=5, pady=5)
        self.config_frame.grid_propagate(0)  # keep right column fixed size (width)

        self.after(config.dyn.visual_framedelay, self.render_objects)

    def render_objects(self) -> None:
        # Render Start
        for obj in sim_space.objects:
            self.render_frame.render_object(obj)
        # Render End
        # recall render after x time
        self.after(config.dyn.visual_framedelay, self.render_objects)


if __name__ == "__main__":
    #myobj = classes.planets.Planets.planet_to_object(classes.planets.Planets.request_planet_data("earth")[0])
    #sim_space.append_object(myobj)
    sim_space.load_objects(config.user.objects)
    mywindow = Window()
    #mywindow.state("zoomed")
    mywindow.geometry("1600x600")
    mywindow.mainloop()
    sim_space.stop_simulation()

    # save the config
    config.user.save()
    config.dyn.save()
    # const cannot be saved
