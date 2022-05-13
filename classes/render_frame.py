"""
Author
melektron
"""

from copy import deepcopy
import tkinter.ttk as ttk
import tkinter as tk

from classes.vector import Vector2D
from classes.sim_object import SimObject
from classes.sim_space import sim_space
import classes.events as events
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

        # list of all currently valid object oval descriptors
        self.object_ovals: list[int] = []
        # list of all currently valid object force vector descriptors
        self.object_force_vectors: list[int] = []
        # list of all currently valid object velocity vector descriptors
        self.object_velocity_vectors: list[int] = []

        # === Object tools
        self.tool_action_active: bool = False   # flag that indicates that a tool has previously been used on an object by clicking and that the tool is still active
        self.active_tool: str = ""              # name of the tool that is still active
        self.influenced_object_start_position: Vector2D = Vector2D(0, 0)    # position of the object influenced by the tool when the object was first clicked on
        self.influenced_object_start_active: bool = False   # The active flag of the object when the action started
        self.influenced_object: SimObject = ... # object influencec by the current action


        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.render_canvas = tk.Canvas(self, highlightthickness=0)
        self.mouse_coords_text = self.render_canvas.create_text(10, 10, anchor="nw", text="X: N/A    Y: N/A")
        self.render_canvas.bind("<Motion>", self.canvas_mouse_move)
        self.render_canvas.bind("<Button-1>", self.canvas_mouse_l_p)
        self.render_canvas.bind("<ButtonRelease-1>", self.canvas_mouse_l_r)

        # on Windows and Linux right mouse is <Button-3>
        if config.dyn.platform.startswith("windows") or config.dyn.platform.startswith("linux"):
            self.render_canvas.bind("<Button-3>", self.canvas_mouse_r_p)
            self.render_canvas.bind("<ButtonRelease-3>", self.canvas_mouse_r_r)
        # on Mac, right mouse is <Button-2> and middle mouse is <Button-3>
        elif config.dyn.platform.startswith("darwin"):
            self.render_canvas.bind("<Button-2>", self.canvas_mouse_r_p)
            self.render_canvas.bind("<ButtonRelease-2>", self.canvas_mouse_r_r)
        
        # on Mac and Windows, <MouseWheel> is the mouse wheel event
        if config.dyn.platform.startswith("windows") or config.dyn.platform.startswith("darwin"):
            self.render_canvas.bind("<MouseWheel>", self.canvas_mouse_scroll)
        # on Linux (X11), <Button-4> and <Button-5> are the mouse wheel up and down events
        elif config.dyn.platform.startswith("linux"):
            self.render_canvas.bind("<Button-4>", self.canvas_mouse_scroll)
            self.render_canvas.bind("<Button-5>", self.canvas_mouse_scroll)
        
        self.render_canvas.bind("<Escape>", self.canvas_escape)
        self.render_canvas.grid(row=0, column=0, sticky="NSEW")


    def canvas_mouse_move(self, event):
        (x, y) = self.render2simcords(event.x, event.y)
        self.render_canvas.itemconfig(self.mouse_coords_text, text=f"X: {round(x, 2)}   Y: {round(y, 2)}")

        if self.render_offset_move_active:
            self.render_offset.cart = (
                self.render_offset_before.x + event.x - self.render_offset_init_mouse_pos.x,
                self.render_offset_before.y + event.y - self.render_offset_init_mouse_pos.y
            )
        
        if self.tool_action_active:
            if self.active_tool == "move":
                self.influenced_object.pos.cart = self.render2simcords(event.x, event.y)
            if self.active_tool == "paste":
                self.influenced_object.pos.cart = self.render2simcords(event.x, event.y)

    def canvas_mouse_r_p(self, event):
        # === initiate view moving
        self.render_offset_before.cart = self.render_offset.cart
        self.render_offset_init_mouse_pos.cart = (event.x, event.y)
        self.render_offset_move_active = True
        # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
        self.render_canvas.focus_set()
    
    def canvas_mouse_r_r(self, event):
        self.render_offset_move_active = False
        
        # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
        self.render_canvas.focus_set()
    
    def canvas_mouse_l_p(self, event):
        # somecode

        # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
        self.render_canvas.focus_set()
    
    def canvas_mouse_l_r(self, event):
        # === handle active tool actions
        # if any tool is active, do the corresponding tool action
        if self.tool_action_active:
            if self.active_tool == "move":
                self.influenced_object.pos.cart = self.render2simcords(event.x, event.y)    # place object on mouse position
                self.influenced_object.vel.cart = (0, 0)    # zero the velocity after manually placing an object
                self.influenced_object.active = self.influenced_object_start_active    # return activity state to what it was before
                self.active_tool = ""
                self.tool_action_active = False
                self.influenced_object = ...
                events.object_prop_change.trigger()
                # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
                self.render_canvas.focus_set()
                return
            elif self.active_tool == "paste":
                self.influenced_object.pos.cart = self.render2simcords(event.x, event.y)    # place object on mouse position
                self.influenced_object.active = self.influenced_object_start_active    # return activity state to what it was before
                self.active_tool = ""
                self.tool_action_active = False
                self.influenced_object = ...
                events.objects_change.trigger()
                # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
                self.render_canvas.focus_set()
                return
        
        # === handle object independent tools
        if config.dyn.tool == "new":
            # create a new object from the default values
            new_obj = sim_space.default_object.copy()
            new_obj.pos.cart = self.render2simcords(event.x, event.y)
            sim_space.objects.append(new_obj)   # add the new object to the simulation
            events.objects_change.trigger()
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        if config.dyn.tool == "paste":
            # create a new object from the clipboard unless it is empty
            if sim_space.clipboard_object is ...: 
                # set canvas in focus on any mouse actino at the end so other widgets don't steel focus before
                self.render_canvas.focus_set()
                return
            new_obj = sim_space.clipboard_object.copy()
            new_obj.pos.cart = self.render2simcords(event.x, event.y)
            new_obj.vel.cart = (0, 0)
            sim_space.objects.append(new_obj)   # add the new object to the simulation
            events.objects_change.trigger()
            # set canvas in focus on any mouse actino at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
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
            # clicked next to object, remove selection
            sim_space.selected_object = ...
            events.selection_change.trigger()
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        # === handle tools that need an object to be clicked
        if config.dyn.tool == "move":
            self.initiate_move(clicked_obj)
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        if config.dyn.tool == "delete":
            sim_space.objects.remove(clicked_obj)   # delete the object from the simulation and rendering list
            events.objects_change.trigger()
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        if config.dyn.tool == "select":
            sim_space.selected_object = clicked_obj
            events.selection_change.trigger()
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        if config.dyn.tool == "copy":
            sim_space.clipboard_object = clicked_obj.copy()
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        if config.dyn.tool == "duplicate":
            sim_space.clipboard_object = clicked_obj.copy()
            self.initiate_paste()
            # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
            self.render_canvas.focus_set()
            return
        
        
        # set canvas in focus on any mouse action at the end so other widgets don't steel focus before
        self.render_canvas.focus_set()
        
    def canvas_mouse_scroll(self, event: tk.Event):
        # on linux, the delta is 0 and the directino has to be retrieved by whether the event was caused by
        # <Button-4> or <Button-5>. Here we just manually set the delta to make comatible with code below
        if config.dyn.platform.startswith("linux"):
            if event.num == 4: event.delta = 120
            elif event.num == 5: event.delta = -120
        
        # get mouse position in rendering frame that is to be preserved
        mousepos_sim: Vector2D = Vector2D.from_cart(self.render2simcords(event.x, event.y))
        # change zoom factor
        self.zoom_factor += self.zoom_factor * config.const.zoom_step * event.delta / config.dyn.mouse_scrl_div
        # get the new render coordinate of the preserved simulation coordinate
        oldmousepos_now_render: Vector2D = Vector2D.from_cart(self.sim2rendercords(mousepos_sim.x, mousepos_sim.y))
        # add to old offset
        self.render_offset += Vector2D(event.x - oldmousepos_now_render.x, event.y - oldmousepos_now_render.y )
        
    def canvas_escape(self, event):
        # === handle active tool actions
        # if any tool is active, do the corresponding tool action
        if self.tool_action_active:
            if self.active_tool == "move":
                # abort move
                self.influenced_object.pos.cart = self.influenced_object_start_position.cart    # place object back in oritginal position
                self.influenced_object.active = True    # enable the object for simulation
                self.active_tool = ""
                self.tool_action_active = False
                self.influenced_object = ...
                return
            elif self.active_tool == "paste":
                # abort paste
                sim_space.objects.remove(self.influenced_object)
                self.active_tool = ""
                self.tool_action_active = False
                self.influenced_object = ...
                return

        # === deselect current selection if no tool is active
        if sim_space.selected_object is not ...:
            sim_space.selected_object = ...
            events.selection_change.trigger()
            return

        # === set tool to select if nothing else caught the escape key
        if config.dyn.tool != "select":
            config.dyn.tool = "select"
            events.tool_change.trigger()
            return
        
    def copy_selection(self):
        if not sim_space.selected_object is ...:
            sim_space.clipboard_object = sim_space.selected_object.copy()

    def initiate_paste(self):
        if self.tool_action_active: return  # don't override existing action
        self.tool_action_active = True
        self.active_tool = "paste"
        self.influenced_object = sim_space.clipboard_object.copy()
        self.influenced_object_start_active = self.influenced_object.active
        self.influenced_object.active = False
        self.influenced_object.vel.cart = (0, 0)
        sim_space.objects.append(self.influenced_object)   # add the new object to the simulation
        print("ctrlv")
    
    def initiate_move(self, obj: SimObject):
        if self.tool_action_active: return  # don't override existing action
        self.influenced_object = obj
        self.influenced_object_start_active = obj.active
        self.influenced_object.active = False
        self.influenced_object_start_position.cart = obj.pos.cart
        self.active_tool = "move"
        self.tool_action_active = True

    def render_objects(self, objs: list[SimObject]) -> None:
        # make a copy of all shapes currently on the canvas
        ovals = deepcopy(self.object_ovals)
        fvectors = deepcopy(self.object_force_vectors)
        vvectors = deepcopy(self.object_velocity_vectors)
        for obj in objs:
            if obj.ca_circle_id is not ...:
                if not obj.ca_circle_id in ovals:   # if it is the first time it was checked
                    self.object_ovals.append(obj.ca_circle_id)  # add it to the list of existing shapes
                else:
                    ovals.remove(obj.ca_circle_id)  # this shape is still required, so remove it from the temporary oval list
            # do same thing with f and v vectors
            if obj.ca_fvector_id is not ...:
                if not obj.ca_fvector_id in fvectors:
                    self.object_force_vectors.append(obj.ca_fvector_id)
                else:
                    fvectors.remove(obj.ca_fvector_id)

            if obj.ca_vvector_id is not ...:
                if not obj.ca_vvector_id in vvectors:
                    self.object_velocity_vectors.append(obj.ca_vvector_id)
                else:
                    vvectors.remove(obj.ca_vvector_id)
            # render the object
            self._render_object(obj)
        
        # any shapes that are left in one of the temporary list don't belong to an existing object anymore. they should be delted
        for shape in ovals:
            self.render_canvas.delete(shape)
            self.object_ovals.remove(shape)
        for shape in fvectors:
            self.render_canvas.delete(shape)
            self.object_force_vectors.remove(shape)
        for shape in vvectors:
            self.render_canvas.delete(shape)
            self.object_velocity_vectors.remove(shape)

    def _render_object(self, obj: SimObject) -> None:
        # get corner positions of objects
        x0, y0 = self.sim2rendercords(obj.pos.x - obj.radius, obj.pos.y - obj.radius)
        x1, y1 = self.sim2rendercords(obj.pos.x + obj.radius, obj.pos.y + obj.radius)
        fill = obj.color
        line = "black"
        width = 1
        if obj is sim_space.selected_object:
            width=3
        elif not obj.active:
            fill = "lightgray"
        

        # render oval representing the object
        if obj.ca_circle_id is ...:
            # if object has not been drawn jet, create new object
            obj.ca_circle_id = self.render_canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=line, width=width)
        else:
            self.render_canvas.coords(
                obj.ca_circle_id,
                x0, y0, x1, y1)
            self.render_canvas.itemconfig(obj.ca_circle_id, fill=fill, outline=line, width=width)

        # force vector
        if config.dyn.show_force_vector:#
            # get the values
            fx0, fy0 = self.sim2rendercords(obj.pos.x, obj.pos.y)
            fx1, fy1 = self.sim2rendercords(obj.pos.x + obj.force.x, obj.pos.y + obj.force.y)

            # render the force vectors as arrow lines
            if obj.ca_fvector_id is ...:
                obj.ca_fvector_id = self.render_canvas.create_line(
                    fx0, fy0, fx1, fy1, arrow=tk.LAST, fill="blue")
            else:
                self.render_canvas.coords(
                    obj.ca_fvector_id,
                    fx0, fy0, fx1, fy1)
        else:
            obj.ca_fvector_id = ...
        
        # velocity vector
        if config.dyn.show_velocity_vector:#
            # get the values
            vx0, vy0 = self.sim2rendercords(obj.pos.x, obj.pos.y)
            # apply a scaling factor because velocity is to small to see otherwise
            scaled_vel: Vector2D = obj.vel * config.const.velocity_vector_display_factor
            vx1, vy1 = self.sim2rendercords(obj.pos.x + scaled_vel.x, obj.pos.y + scaled_vel.y)

            # render the force vectors as arrow lines
            if obj.ca_vvector_id is ...:
                obj.ca_vvector_id = self.render_canvas.create_line(
                    vx0, vy0, vx1, vy1, arrow=tk.LAST, fill="red")
            else:
                self.render_canvas.coords(
                    obj.ca_vvector_id,
                    vx0, vy0, vx1, vy1)
        else:
            obj.ca_vvector_id = ...

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