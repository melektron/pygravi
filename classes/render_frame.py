"""
Author
"""

import tkinter.ttk as ttk
import tkinter as tk
from classes.vector import Vector2D


class RenderFrame(ttk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.render_canvas = tk.Canvas(self)
        self.render_canvas.bind("<Motion>", self.canvas_mouse_move)
        self.render_canvas.bind("<Button-1>", self.canvas_mouse_b1)
        self.render_canvas.bind("<MouseWheel>", self.canvas_mouse_scroll)
        self.render_canvas.grid(row=0, column=0, sticky="NSEW")
        self.ovrx = 25
        self.ovry = 25
        self.testvector: Vector2D = Vector2D(50, 50)
        self.testoval = self.render_canvas.create_oval(
            self.testvector.x - self.ovrx,
            self.testvector.y - self.ovry,
            self.testvector.x + self.ovrx,
            self.testvector.y + self.ovry)
        self.testarrow = self.render_canvas.create_line(
            0, 0, self.ovrx, self.ovry, arrow=tk.LAST)

        self.moveactive: bool = False

    def canvas_mouse_move(self, event):
        if (self.moveactive):
            # save mouse values to vector
            self.testvector.cart = (event.x, event.y)

            # move to vector
            self.render_canvas.moveto(
                self.testoval,
                self.testvector.x - self.ovrx,
                self.testvector.y - self.ovry)
            self.render_canvas.coords(self.testarrow, 0, 0, self.testvector.x, self.testvector.y)

    def canvas_mouse_b1(self, event):
        self.moveactive = not self.moveactive   # toggle

    def canvas_mouse_scroll(self, event):
        if not self.moveactive:
            self.testvector.phi = self.testvector.phi + (event.delta / 960)
            self.render_canvas.moveto(
                self.testoval,
                self.testvector.x - self.ovrx,
                self.testvector.y - self.ovry)
            self.render_canvas.coords(self.testarrow, 0, 0, self.testvector.x, self.testvector.y)
