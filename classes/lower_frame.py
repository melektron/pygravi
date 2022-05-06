"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
from classes.custom_slider import CustomSlider

High_Value=1
Low_Value=0

class LowerFrame(ttk.Frame): 
    def __init__(self, master): 
        super().__init__(master)
        self.mass_variable=tk.DoubleVar()
        self.diameter_variable=tk.DoubleVar()


        #Object settings Headline 
        self.object_headline_frame=ttk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.columnconfigure(0, weight=1)
        self.object_headline_frame.grid(row=0, column=0, sticky="WE", pady=10)
        
        self.object_headline=ttk.Label(self.object_headline_frame, text="Object Properties", font=(40))
        self.object_headline.grid(row=0, column=0, sticky="WE")

        #Object Name Frame
        self.object_frame=ttk.Frame(self)
        self.object_frame.columnconfigure(1, weight=1)
        self.object_frame.grid(row=1, column=0, sticky="WE", pady=10)

        self.object_name_label=ttk.Label(self.object_frame, text="Object name: ")
        self.object_name_label.grid(row=0, column=0)

        self.object_name_entry=ttk.Entry(self.object_frame)
        self.object_name_entry.grid(row=0, column=1, sticky="WE")

        #Checkbox Ideal System 
        self.checkbox_object_state=tk.IntVar(value=High_Value)
        self.checkbox_object=ttk.Checkbutton(self,variable=self.checkbox_object_state, onvalue=High_Value, offvalue=Low_Value, text="Object ON/OFF") #command and variable
        self.checkbox_object.grid(row=2, column=0, sticky="W", pady=10)

        #Mass
        self.mass_slider=CustomSlider(self, text="Mass", from_=0.03, to=1, variable=self.mass_variable, unit="kg")
        self.mass_variable.trace("w", lambda a,b,c: print(self.mass_variable.get()))
        self.columnconfigure(0, weight=1)
        self.mass_slider.grid(row=3, column=0, sticky="WE", pady=10)

        #Diameter
        self.diameter_slider=CustomSlider(self, text="Diameter", from_=0.03, to=1, variable=self.diameter_variable, unit="m")
        self.diameter_variable.trace("w", lambda a,b,c: print(self.diameter_variable.get()))
        self.columnconfigure(0, weight=1)
        self.diameter_slider.grid(row=4, column=0, sticky="WE", pady=10)