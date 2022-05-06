"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
from classes.custom_slider import CustomSlider

High_Value=1
Low_Value=0

class UpperFrame(ttk.Frame): 
    def __init__(self, master): 
        super().__init__(master)
        self.gravitation_variable=tk.DoubleVar()
        self.energy_variable=tk.DoubleVar()
        self.simulation_speed_variable=tk.DoubleVar()
        self.time_step_variable=tk.DoubleVar()


        #Headline 
        self.headline_frame=ttk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.columnconfigure(0, weight=1)
        self.headline_frame.grid(row=0, column=0, sticky="WE", padx=10, pady=10)
        

        self.headline=ttk.Label(self.headline_frame, text="Simulation Properties", font=(40))
        self.headline.grid(row=0, column=0, sticky="WE")
        
        #Checkbox Frame
        self.checkbox_frame=ttk.Frame(self)
        self.checkbox_frame.grid(row=1, column=0, sticky="WE", padx=10, pady=10)

        #Checkbox Gravitation 
        self.checkbox_gravitation_state=tk.IntVar(value=High_Value)
        self.checkbox_gravitation=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_gravitation_state, onvalue=High_Value, offvalue=Low_Value, text="Gravitation") #command and variable
        self.checkbox_gravitation.grid(row=0, column=0, sticky="W")

        #Checkbox Collision 
        self.checkbox_collision_state=tk.IntVar(value=High_Value)
        self.checkbox_collision=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_collision_state, onvalue=High_Value, offvalue=Low_Value, text="Collision") #command and variable
        self.checkbox_collision.grid(row=1, column=0, sticky="W")

        #Checkbox Ideal System 
        self.checkbox_ideal_state=tk.IntVar(value=High_Value)
        self.checkbox_ideal=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_ideal_state, onvalue=High_Value, offvalue=Low_Value, text="Ideal System") #command and variable
        self.checkbox_ideal.grid(row=2, column=0, sticky="W")

        #Energy
        self.energy_slider=CustomSlider(self, text="Collision Losses", from_=0.03, to=1, variable=self.energy_variable, unit="J")
        self.energy_variable.trace("w", lambda a,b,c: print(self.energy_variable.get()))
        self.energy_slider.grid(row=2, column=0, sticky="WE", padx=10, pady=10)

        #Walls 
        self.walls=tk.IntVar()
        self.walls.set(0)

        self.walls_frame=ttk.Frame(self)
        self.walls_frame.grid(row=3, column=0, sticky="WE", padx=10, pady=10)

        self.walls_collide=ttk.Radiobutton(self.walls_frame, text="Walls collide", variable=self.walls, value=0)
        self.walls_collide.grid(row=0, column=0, sticky="W")
        self.walls_teleport=ttk.Radiobutton(self.walls_frame, text="Walls teleport", variable=self.walls, value=1)
        self.walls_teleport.grid(row=1, column=0, sticky="W")
        self.no_walls=ttk.Radiobutton(self.walls_frame, text="No walls", variable=self.walls, value=2)
        self.no_walls.grid(row=2, column=0, sticky="W")

        #Gravitation
        self.gravitation_slider=CustomSlider(self, text="Gravitation", from_=0.03, to=1, variable=self.gravitation_variable)
        self.gravitation_variable.trace("w", lambda a,b,c: print(self.gravitation_variable.get()))
        self.gravitation_slider.grid(row=4, column=0, sticky="WE", padx=10, pady=10)

        #Simulation Speed
        self.simulation_speed_slider=CustomSlider(self, text="Simulation Speed", from_=0.03, to=1, variable=self.simulation_speed_variable)
        self.simulation_speed_variable.trace("w", lambda a,b,c: print(self.simulation_speed_variable.get()))
        self.simulation_speed_slider.grid(row=5, column=0, sticky="WE", padx=10, pady=10)

        #Time Step
        self.time_step_slider=CustomSlider(self, text="Time Step", from_=0.03, to=1, variable=self.time_step_variable, unit="s")
        self.time_step_variable.trace("w", lambda a,b,c: print(self.time_step_variable.get()))
        self.time_step_slider.grid(row=6, column=0, sticky="WE", padx=10, pady=10)
        
        #Start Stop Reset 
        self.start_frame=ttk.Frame(self)
        self.start_frame.grid(row=7, column=0, sticky="WE", padx=10, pady=10)
        self.start_frame.columnconfigure((0,1,2), weight=1)

        self.start_button=ttk.Button(self.start_frame, text="START")
        self.start_button.grid(row=0, column=0, sticky="WE", padx=10, ipady=5)

        self.stop_button=ttk.Button(self.start_frame, text="STOPP")
        self.stop_button.grid(row=0, column=1, sticky="WE", padx=10, ipady=5)

        self.reset_button=ttk.Button(self.start_frame, text="RESET")
        self.reset_button.grid(row=0, column=2, sticky="WE", padx=10, ipady=5)

        #Place between Upper and Lower Frame
        self.place_holder_label=ttk.Label(self)
        self.place_holder_label.grid(row=8, column=0)