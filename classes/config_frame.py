"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
 
class ConfigFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)
        
        
 
if __name__ =="__main__": 
    root = tk.Tk()
    root.geometry("300x400")
    frame=ConfigFrame(root)


    root.mainloop()
    
