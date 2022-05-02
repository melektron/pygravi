"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
 
class Window:
    def __init__(self, master):
        self.master = master
 
        frame = ttk.Frame(self.master)
 
        style = ttk.Style()
        style.configure("Custom.TButton",foreground="black",
                                         background="white",
                                         padding=[10, 10, 10, 10],
                                         font = "Verdana 12 underline")
 
        button = ttk.Button(frame, text = "Click Me!", style = "Custom.TButton")
        button.pack()
 
        frame.pack(padx = 5, pady = 5)
 
root = tk.Tk()
root.geometry("200x150")
window = Window(root)
root.mainloop()