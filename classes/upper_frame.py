"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
from classes.custom_slider import CustomSlider
import classes.config as config 
from classes.sim_space import sim_space

High_Value=True
Low_Value=False

class UpperFrame(ttk.Frame): 
    def __init__(self, master): 
        super().__init__(master)
        self.gravitation_variable=tk.DoubleVar()
        self.collision_losses_variable=tk.DoubleVar()
        self.simulation_frame_delay_variable=tk.DoubleVar()
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
        self.checkbox_gravitation_state=tk.IntVar(value=config.dyn.do_gravity)
        self.checkbox_gravitation=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_gravitation_state, onvalue=High_Value, offvalue=Low_Value, text="Gravitation", command=self.checkbox_do_gravity_change) 
        self.checkbox_gravitation.grid(row=0, column=0, sticky="W")

        #Checkbox Collision 
        self.checkbox_collision_state=tk.IntVar(value=config.dyn.do_collision)
        self.checkbox_collision=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_collision_state, onvalue=High_Value, offvalue=Low_Value, text="Collision", command=self.checkbox_do_collision_change) 
        self.checkbox_collision.grid(row=1, column=0, sticky="W")

        #Checkbox Ideal System 
        self.checkbox_ideal_state=tk.IntVar(value=config.dyn.do_ideal)
        self.checkbox_ideal=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_ideal_state, onvalue=High_Value, offvalue=Low_Value, text="Ideal System", command=self.checkbox_do_ideal_change) 
        self.checkbox_ideal.grid(row=2, column=0, sticky="W")

        #Collision Losse
        self.collision_losses_slider=CustomSlider(self, text="Collision Losses", from_=0, to=1, variable=self.collision_losses_variable, unit="J")
        self.collision_losses_variable.trace("w", self.slider_collosion_losses_change)
        self.collision_losses_slider.grid(row=2, column=0, sticky="WE", padx=10, pady=10)

        #Vector Frame (force,velocity)
        self.vector_checkbox_frame=ttk.Frame(self)
        self.vector_checkbox_frame.grid(row=2, column=0, sticky="WE", padx=10, pady=10)

        #Checkbox force vector 
        self.checkbox_force_state=tk.IntVar(value=config.dyn.show_force_vector)
        self.checkbox_force=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_force_state, onvalue=High_Value, offvalue=Low_Value, text="Force", command=self.checkbox_do_force_vector_change) 
        self.checkbox_force.grid(row=0, column=0, sticky="W")

        #Checkbox velocity vector
        self.checkbox_velocity_state=tk.IntVar(value=config.dyn.show_velocity_vector)
        self.checkbox_velocity=ttk.Checkbutton(self.checkbox_frame,variable=self.checkbox_collision_state, onvalue=High_Value, offvalue=Low_Value, text="Velocity", command=self.checkbox_do_velocity_vector_change) 
        self.checkbox_velocity.grid(row=1, column=0, sticky="W")

        #Slider Gravitation
        self.gravitation_slider=CustomSlider(self, text="Gravitation", from_=0, to=1, variable=self.gravitation_variable, resolution=15)
        self.gravitation_variable.trace("w", self.slider_G_change)
        self.gravitation_slider.grid(row=4, column=0, sticky="WE", padx=10, pady=10)

        #Slider Simulation Frame Delay
        self.simulation_frame_delay_slider=CustomSlider(self, text="Simulation Frame Delay", from_=0.03, to=1, variable=self.simulation_frame_delay_variable, unit="us")
        self.simulation_frame_delay_variable.trace("w", self.slider_sframedelay_change)
        self.simulation_frame_delay_slider.grid(row=5, column=0, sticky="WE", padx=10, pady=10)

        #Slider Time Step
        self.time_step_slider=CustomSlider(self, text="Time Step", from_=0, to=1, variable=self.time_step_variable, unit="s")
        self.time_step_variable.trace("w", self.slider_deltat_change)
        self.time_step_slider.grid(row=6, column=0, sticky="WE", padx=10, pady=10)
        
        #Start Stop Reset Button
        self.start_frame=ttk.Frame(self)
        self.start_frame.grid(row=7, column=0, sticky="WE", padx=10, pady=10)
        self.start_frame.columnconfigure((0,1,2), weight=1)

        self.start_button=ttk.Button(self.start_frame, text="START", command=sim_space.run_simulation)
        self.start_button.grid(row=0, column=0, sticky="WE", padx=10, ipady=5)

        self.stop_button=ttk.Button(self.start_frame, text="STOP", command=sim_space.pause_simulation)
        self.stop_button.grid(row=0, column=1, sticky="WE", padx=10, ipady=5)

        self.reset_button=ttk.Button(self.start_frame, text="RESET")
        self.reset_button.grid(row=0, column=2, sticky="WE", padx=10, ipady=5)

        #Place between Upper and Lower Frame
        self.place_holder_label=ttk.Label(self)
        self.place_holder_label.grid(row=8, column=0)

    
    #Collision Losses Slider 
    def slider_collosion_losses_change(self, a,b,c): 
        config.dyn.collision_losses=self.collision_losses_variable.get()
    
    #Gravitation Slider 
    def slider_G_change(self, a,b,c): 
        config.dyn.G=self.gravitation_variable.get()

    #Simulation Frame Delay Slider 
    def slider_sframedelay_change(self, a,b,c): 
        config.dyn.sim_framedelay=self.simulation_frame_delay_variable.get()

    #Time step Slider 
    def slider_deltat_change(self, a,b,c): 
        config.dyn.sim_deltat=self.time_step_variable.get()

    #Gravitation Checkbox 
    def checkbox_do_gravity_change(self):
        config.dyn.do_gravity=self.checkbox_gravitation_state.get()

    #Collision Checkbox 
    def checkbox_do_collision_change(self):
        config.dyn.do_collision=self.checkbox_collision_state.get()

    #Ideal System Checkbox 
    def checkbox_do_ideal_change(self):
        config.dyn.do_ideal=self.checkbox_ideal_state.get()

    #Force vector Checkbox 
    def checkbox_do_force_vector_change(self):
        config.dyn.show_force_vector=self.checkbox_force_state.get()

    #Velocity vector Checkbox 
    def checkbox_do_velocity_vector_change(self):
        config.dyn.show_velocity_vector=self.checkbox_velocity_state.get()
        
