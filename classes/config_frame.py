"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
from classes.upper_frame import UpperFrame
from classes.lower_frame import LowerFrame

 
class ConfigFrame(ttk.Frame): 
    def __init__(self, master, **kwargs): 
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs) # kwargs is dictionary 
        self.upper=UpperFrame(self)
        self.rowconfigure(0,weight=0)
        self.columnconfigure(0, weight=1)
        self.upper.grid(row=0, column=0)
        

        self.lower_=LowerFrame(self)
        self.rowconfigure(1, weight=1)
        self.lower_.grid(row=1, column=0, sticky="N")
    
    def update_object_prop(self):
        self.lower_.update()


