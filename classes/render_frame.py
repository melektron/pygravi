"""
Author
"""

import tkinter.ttk as ttk
import tkinter as tk


class RenderFrame(ttk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.render_canvas = tk.Canvas(self)
        self.render_canvas.grid(row=0, column=0, sticky="NSEW")
        self.testoval = self.render_canvas.create_oval(0, 0, 50, 50)

        self.render_canvas.move(self.testoval, 10, 10)


    
