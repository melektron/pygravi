"""
Author
"""

import tkinter.ttk as ttk
import tkinter as tk

from classes.vector import Vector2D
from classes.sim_object import SimObject
from classes.sim_space import sim_space
from classes.config_frame import config_frame
import classes.config as config


class RenderFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)

        # === Rendering 
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

        # === Object tools
        self.tool_action_active: bool = False   # flag that indicates that a tool has previously been used on an object by clicking and that the tool is still active
        self.active_tool: str = ""              # name of the tool that is still active
        self.influenced_object_start_position: Vector2D = Vector2D(0, 0)    # position of the object influenced by the tool when the object was first clicked on
        self.influenced_object: SimObject = ... # object influencec by the current action


        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.render_canvas = tk.Canvas(self)
        self.render_canvas.bind("<Motion>", self.canvas_mouse_move)
        self.render_canvas.bind("<Button-1>", self.canvas_mouse_b1p)
        self.render_canvas.bind("<ButtonRelease-1>", self.canvas_mouse_b1r)
        self.render_canvas.bind("<Button-3>", self.canvas_mouse_b3p)
        self.render_canvas.bind("<ButtonRelease-3>", self.canvas_mouse_b3r)
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
        
        if self.tool_action_active:
            if self.active_tool == "move":
                self.influenced_object.pos.cart = self.render2simcords(event.x, event.y)
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

    def canvas_mouse_b3p(self, event):
        #self.moveactive = not self.moveactive   # toggle for testoval
        self.render_offset_before.cart = self.render_offset.cart
        self.render_offset_init_mouse_pos.cart = (event.x, event.y)
        self.render_offset_move_active = True
    
    def canvas_mouse_b3r(self, event):
        self.render_offset_move_active = False
    
    def canvas_mouse_b1p(self, event):
        pass
    
    def canvas_mouse_b1r(self, event):
        # === handle active tool actions
        # if any tool is active, do the corresponding tool action
        if self.tool_action_active:
            if self.active_tool == "move":
                self.influenced_object.pos.cart = self.render2simcords(event.x, event.y)    # place object on mouse position
                self.influenced_object.vel.cart = (0, 0)    # zero the velocity after manually placing an object
                self.influenced_object.active = True    # enable the object for simulation
                self.active_tool = ""
                self.tool_action_active = False
                self.influenced_object = ...
                return
        
        # === handle object independent tools
        if config.dyn.tool == "new":
            # create a new object from the default values
            new_obj = SimObject(
                config.user.default_object["name"],
                config.user.default_object["radius"],
                config.user.default_object["mass"],
                Vector2D.from_cart(self.render2simcords(event.x, event.y))
                )
            sim_space.objects.append(new_obj)   # add the new object to the simulation
            return

        
        # === check if an object was clicked
        # get the simulation coordinates corresponding to the mouse coordinates
        x, y = self.render2simcords(event.x, event.y)
        # check if it is within any of the objects
        clicked_obj: SimObject = ...
        for obj in sim_space.objects:
            if pow(x - obj.pos.x, 2) + pow(y - obj.pos.y, 2) < pow(obj.radius, 2): # https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle
                clicked_obj = obj
        if clicked_obj is ...:
            return
        
        # === handle tools that need an object to be clicked
        if config.dyn.tool == "move":
            self.influenced_object = clicked_obj
            self.influenced_object.active = False
            self.influenced_object_start_position.cart = clicked_obj.pos.cart
            self.active_tool = "move"
            self.tool_action_active = True
            return
        
        if config.dyn.tool == "delete":
            if clicked_obj.ca_circle_id is not ...:
                self.render_canvas.delete(clicked_obj.ca_circle_id) # remove from the canvas, otherwise the object would simply freeze and not disappear
            sim_space.objects.remove(clicked_obj)   # delete the object from the simulation and rendering list
            return
        
        if config.dyn.tool == "select":
            sim_space.selected_object = clicked_obj
        

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
        fill = "black"
        if obj is sim_space.selected_object:
            fill="lightblue"
        elif not obj.active:
            fill = "lightgray"
        

        # render oval representing the object
        if obj.ca_circle_id is ...:
            # if object has not been drawn jet, create new object
            obj.ca_circle_id = self.render_canvas.create_oval(x0, y0, x1, y1, fill=fill)
        else:
            self.render_canvas.coords(
                obj.ca_circle_id,
                x0, y0, x1, y1)
            self.render_canvas.itemconfig(obj.ca_circle_id, fill=fill)

        # show force vector
        if config.dyn.show_force_vector:#
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