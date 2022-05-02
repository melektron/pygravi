"""
Author:
melektron
"""


import tkinter.ttk as ttk
import tkinter as tk

import classes.render_frame


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.render_frame = classes.render_frame.RenderFrame(self)
        self.render_frame.config(width=500)
        self.render_frame.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

if __name__ == "__main__":
    mywindow = Window()
    mywindow.mainloop()
