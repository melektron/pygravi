"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
from classes.sim_prop_frame import SimPropFrame

 
class ConfigFrame(ttk.Frame): 
    def __init__(self, master, **kwargs): 
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs) # kwargs is dictionary 
        self.sim_prop=SimPropFrame(self)
        self.rowconfigure(0,weight=0)
        self.columnconfigure(0, weight=1)
        self.sim_prop.grid(row=0, column=0)
        

    

