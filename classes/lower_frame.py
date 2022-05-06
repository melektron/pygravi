"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
from classes.custom_slider import CustomSlider
from classes.sim_space import sim_space
import classes.events as events

High_Value=True
Low_Value=False

class LowerFrame(ttk.Frame): 
    def __init__(self, master): 
        super().__init__(master)
        self.mass_variable=tk.DoubleVar()
        self.diameter_variable=tk.DoubleVar()


        #Object settings Headline 
        self.object_headline_frame=ttk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.columnconfigure(0, weight=1)
        self.object_headline_frame.grid(row=0, column=0, sticky="WE", pady=10, padx=10)
        
        self.object_headline=ttk.Label(self.object_headline_frame, text="Object Properties", font=(40))
        self.object_headline.grid(row=0, column=0, sticky="WE")

        #Object Name Frame
        self.object_frame=ttk.Frame(self)
        self.object_frame.columnconfigure(1, weight=1)
        self.object_frame.grid(row=1, column=0, sticky="WE", pady=10, padx=10)

        self.object_name_label=ttk.Label(self.object_frame, text="Object name: ")
        self.object_name_label.grid(row=0, column=0)

        self.object_name_entry_variable=tk.StringVar()
        self.object_name_entry=ttk.Entry(self.object_frame, width=10, textvariable=self.object_name_entry_variable, validate="focusout", validatecommand=self._object_name_entry_change)
        self.object_name_entry.bind("<Return>", self._object_name_entry_change)
        self.object_name_entry.grid(row=0, column=1, sticky="WE")

        #Checkbox ON/OFF
        self.checkbox_object_state=tk.IntVar(value=High_Value)
        self.checkbox_object=ttk.Checkbutton(self,variable=self.checkbox_object_state, command=self._checkbox_on_off_change, onvalue=High_Value, offvalue=Low_Value, text="Object ON/OFF") #command and variable
        self.checkbox_object.grid(row=2, column=0, sticky="W", pady=10, padx=10)

        #Mass
        self.mass_slider=CustomSlider(self, text="Mass", from_=0, to=1, variable=self.mass_variable, unit="kg")
        self.mass_variable.trace("w", self._slider_mass_change)
        self.columnconfigure(0, weight=1)
        self.mass_slider.grid(row=3, column=0, sticky="WE", pady=10, padx=10)

        #Diameter
        self.diameter_slider=CustomSlider(self, text="Radius", from_=0, to=1, variable=self.diameter_variable, unit="m")
        self.diameter_variable.trace("w", self._slider_diameter_change)
        self.columnconfigure(0, weight=1)
        self.diameter_slider.grid(row=4, column=0, sticky="WE", pady=10, padx=10)

        # subscribe to selection change event to update all values according to the new selection
        events.selection_change.subscribe(self.update)

    #Entry Name
    def _object_name_entry_change(self, event=...): 
        sim_space.selected_object.name=self.object_name_entry_variable.get()

    #Checkbox ON/OFF 
    def _checkbox_on_off_change(self): 
        sim_space.selected_object.active=self.checkbox_object_state.get()
        print("checkbox: ", sim_space.selected_object.active)

    #Slider Mass
    def _slider_mass_change(self, a,b,c): 
        sim_space.selected_object.mass=self.mass_variable.get()

    #Slider Radius
    def _slider_diameter_change(self, a,b,c): 
        sim_space.selected_object.radius=self.diameter_variable.get()

    #Werte aus auswahl auslesen
    def update(self, event_data): 
        self.object_name_entry_variable.set(sim_space.selected_object.name)
        self.checkbox_object_state.set(sim_space.selected_object.active)
        self.mass_variable.set(sim_space.selected_object.mass)
        self.diameter_variable.set(sim_space.selected_object.radius)