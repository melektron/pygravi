"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk


class CustomSlider(ttk.Frame): 
    def __init__(self, master, text="", from_: float=0, to: float=1, position: float=1, resolution: int=3, variable: tk.DoubleVar=..., unit: str=""): 
        super().__init__(master) # Master is root 
        self.resolution: int=resolution
        self.variable: tk.DoubleVar=variable

        # subscribe to external variable updates if a variable was provided
        if not self.variable is ...:
            self.variable.trace("w", self._Variable_change_event)


        #Sliderframe Columnconfigure 
        self.columnconfigure((0,2), uniform="min_max_entrys", weight=1)
        self.columnconfigure(1, weight=2, uniform="min_max_entrys")

        #Slider Frame
        self.info_frame=ttk.Frame(self)
        self.info_frame.grid(row=0, column=0, columnspan=3, sticky="WE")

        #Slider Name
        self.label=ttk.Label(self.info_frame, text=text)
        self.label.grid(row=0, column=0)

        #Current Value Entry
        self.current_value=tk.StringVar(value=str(position))
        self.current_entry=ttk.Entry(self.info_frame, width=10, textvariable=self.current_value, validate="focusout", validatecommand=self._Value_Entry_Change)
        self.current_entry.bind("<Return>", self._Value_Entry_Change)
        self.current_entry.grid(row=0, column=1)

        #Slider unit 
        self.slider_unit=ttk.Label(self.info_frame, text=unit)
        self.slider_unit.grid(row=0, column=2)

        #Slider 
        self.slider=ttk.Scale(self, from_=0, to=100, command=self._SliderChange)
        self.slider.grid(row=1, column=1, sticky="WE")

        #Slider min Entry 
        self.min_value=tk.StringVar(value=str(from_))
        self.min_entry=ttk.Entry(self, width=10, textvariable=self.min_value, validate="focusout", validatecommand=self._Limit_Entry_Change)
        self.min_entry.bind("<Return>", self._Limit_Entry_Change)
        self.min_entry.grid(row=1, column=0, sticky="WE")

        #Slider max Entry 
        self.max_value=tk.StringVar(value=str(to))
        self.max_entry=ttk.Entry(self, width=10, textvariable=self.max_value, validate="focusout", validatecommand=self._Limit_Entry_Change)
        self.max_entry.bind("<Return>", self._Limit_Entry_Change)
        self.max_entry.grid(row=1, column=2, sticky="WE")

        # call the variable change callback manually to update the slider to values set in the variable
        # before creation of the slider (e.g. during construction)
        if not self.variable is ...:
            self._Variable_change_event(...,...,...)

        
    #Scale change 
    def _SliderChange(self, v): 
        current_min: float=eval(self.min_value.get())
        current_max: float=eval(self.max_value.get())
        scale=round((current_max-current_min)*float(v)/100+current_min, self.resolution) #Resolution 
        self.current_value.set(str(scale))
        self._Update_Variable()

    #Current Entry Value change 
    def _Value_Entry_Change(self, event=...): 
        value: float=eval(self.current_value.get())
        current_min: float=eval(self.min_value.get())
        current_max: float=eval(self.max_value.get())
        if value > current_max: 
            self.max_value.set(str(value))
            current_max=value
        elif value < current_min: 
            self.min_value.set(str(value))
            current_min=value
        value-=current_min
        max_=current_max-current_min
        x_slider=value*100/max_ 
        self.slider.set(x_slider)
        self._Update_Variable()
        self.focus()

    #min max Entry change 
    def _Limit_Entry_Change(self, event=...): 
        value: float=eval(self.current_value.get())
        current_min: float=eval(self.min_value.get())
        current_max: float=eval(self.max_value.get())       
        if current_max <= current_min: 
            self.max_value.set(current_min+1)
            current_max=current_min+1
        if current_max < value: 
            self.current_value.set(str(current_max))
            value=current_max
        if current_min > value:  
            self.current_value.set(str(current_min))
            value=current_min
        value-=current_min
        max_=current_max-current_min
        x_slider=value*100/max_ 
        self.slider.set(x_slider)
        self._Update_Variable()
        self.focus()

    #Checks if an argument is given 
    def _Update_Variable(self):
        if self.variable is ...: 
            return  
        x: float=eval(self.current_value.get())
        if x == self.variable.get(): 
            return 
        self.variable.set(x)
    
    def _Variable_change_event(self, a, b, c):
        self.current_value.set(str(self.variable.get()))
        self._Value_Entry_Change()