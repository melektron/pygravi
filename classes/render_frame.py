"""
Author
"""

import tkinter.ttk as ttk
import tkinter as tk
from classes.vector import Vector2D
from classes.sim_object import SimObject
import classes.config as config


class RenderFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)

        # zoom factor for object rendering
        self.zoom_factor: float = 1    # start of with 1:1
        # rendering offset to move the scene around
        self.render_offset: Vector2D = Vector2D(0, 0)
        # rendering offset at the point where the mouse button was pressed to start moving the offset
        self.render_offset_before: Vector2D = Vector2D(0, 0)
        # mouse pointer position when offset move was initiated
        self.render_offset_init_mouse_pos: Vector2D = Vector2D(0, 0)
        # flag that indicates that the mouse button has been pressed to initialize offset moving
        self.render_offset_move_active: bool = False

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.render_canvas = tk.Canvas(self)
        self.render_canvas.bind("<Motion>", self.canvas_mouse_move)
        self.render_canvas.bind("<Button-1>", self.canvas_mouse_b1p)
        self.render_canvas.bind("<ButtonRelease-1>", self.canvas_mouse_b1r)
        self.render_canvas.bind("<MouseWheel>", self.canvas_mouse_scroll)
        self.render_canvas.grid(row=0, column=0, sticky="NSEW")

        # mouse-tracking testoval
        #self.ovrx = 25
        #self.ovry = 25
        #self.testvector: Vector2D = Vector2D(50, 50)
        #self.testoval = self.render_canvas.create_oval(
        #    self.testvector.x - self.ovrx,
        #    self.testvector.y - self.ovry,
        #    self.testvector.x + self.ovrx,
        #    self.testvector.y + self.ovry)
        #self.testarrow = self.render_canvas.create_line(
        #    0, 0, self.ovrx, self.ovry, arrow=tk.LAST)
        #self.moveactive: bool = False

    def canvas_mouse_move(self, event):
        if self.render_offset_move_active:
            self.render_offset.cart = (
                self.render_offset_before.x + event.x - self.render_offset_init_mouse_pos.x,
                self.render_offset_before.y + event.y - self.render_offset_init_mouse_pos.y
            )
        # for testoval
        #if (self.moveactive):
        #    # save mouse values to vector
        #    self.testvector.cart = (event.x, event.y)
#
        #    # move to vector
        #    self.render_canvas.moveto(
        #        self.testoval,
        #        self.testvector.x - self.ovrx,
        #        self.testvector.y - self.ovry)
        #    self.render_canvas.coords(
        #        self.testarrow, 0, 0, self.testvector.x, self.testvector.y)

    def canvas_mouse_b1p(self, event):
        #self.moveactive = not self.moveactive   # toggle for testoval
        self.render_offset_before.cart = self.render_offset.cart
        self.render_offset_init_mouse_pos.cart = (event.x, event.y)
        self.render_offset_move_active = True
    
    def canvas_mouse_b1r(self, event):
        self.render_offset_move_active = False

    def canvas_mouse_scroll(self, event):
        # for testoval
        #if not self.moveactive:
        #    self.testvector.phi = self.testvector.phi + (event.delta / 960)
        #    self.render_canvas.moveto(
        #        self.testoval,
        #        self.testvector.x - self.ovrx,
        #        self.testvector.y - self.ovry)
        #    self.render_canvas.coords(
        #        self.testarrow, 0, 0, self.testvector.x, self.testvector.y)
        
        # get mouse position in rendering frame that is to be preserved
        mousepos_sim: Vector2D = Vector2D.from_cart(self.render2simcords(event.x, event.y))
        # change zoom factor
        self.zoom_factor += config.const.zoom_step * event.delta / 120
        # get the new render coordinate of the preserved simulation coordinate
        oldmousepos_now_render: Vector2D = Vector2D.from_cart(self.sim2rendercords(mousepos_sim.x, mousepos_sim.y))
        # add to old offset
        self.render_offset += Vector2D(event.x - oldmousepos_now_render.x, event.y - oldmousepos_now_render.y )
        


    def render_object(self, obj: SimObject) -> None:

        # get corner positions of objects
        x0, y0 = self.sim2rendercords(obj.pos.x - obj.radius, obj.pos.y - obj.radius)
        x1, y1 = self.sim2rendercords(obj.pos.x + obj.radius, obj.pos.y + obj.radius)

        # render oval representing the object
        if obj.ca_circle_id is ...:
            # if object has not been drawn jet, create new object
            obj.ca_circle_id = self.render_canvas.create_oval(x0, y0, x1, y1)
        else:
            self.render_canvas.coords(
                obj.ca_circle_id,
                x0, y0, x1, y1)

        # show force vector
        if config.dyn.show_fvector:#
            # get the values
            fx0, fy0 = self.sim2rendercords(obj.pos.x, obj.pos.y)
            fx1, fy1 = self.sim2rendercords(obj.pos.x + obj.force.x, obj.pos.y + obj.force.y)

            # render the force vectors as arrow lines
            if obj.ca_fvector_id is ...:
                obj.ca_fvector_id = self.render_canvas.create_line(
                    fx0, fy0, fx1, fy1, arrow=tk.LAST)
            else:
                self.render_canvas.coords(
                    obj.ca_fvector_id,
                    fx0, fy0, fx1, fy1)

    def sim2rendercords(self, simx, simy) -> tuple[float, float]:
        return (
            simx * self.zoom_factor + self.render_offset.x,
            simy * self.zoom_factor + self.render_offset.y
        )
    
    def render2simcords(self, renderx, rendery) -> tuple[float, float]:
        return (
            (renderx - self.render_offset.x) / self.zoom_factor,
            (rendery - self.render_offset.y) / self.zoom_factor
        )