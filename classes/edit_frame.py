"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 11:51

The GUI frame on the left of the window for adding/remoing/selecting simulation objects

"""

from mailbox import _singlefileMailbox
import tkinter as tk
import tkinter.ttk as ttk
from turtle import back
from wsgiref import simple_server
from numpy import isin

from pyparsing import col
import classes.config as config
from classes.object_prop_frame import ObjectPropFrame
from classes.sim_object import SimObject
import classes.events as events
from classes.sim_space import sim_space


class Headline(ttk.Frame):
    def __init__(self, master, text="", **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)
        self.headline_label = ttk.Label(self, text=text, font=(40))
        self.headline_label.grid(row=0, column=0, sticky="W")

class EditFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)

        self.columnconfigure(0, weight=1)

        # === object tools
        # Headline
        self.headline_object_tools = Headline(self, text="Object Tools")
        self.headline_object_tools.grid(row=0, column=0, sticky="WE", padx=10, pady=10)

        # toolbar
        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.grid(row=1, column=0, sticky="WE", padx=10, pady=10)
        self.toolbar_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="toolbar_buttons")
        self.current_tool_variable = tk.StringVar(value=config.dyn.tool)
        self.current_tool_variable.trace("w", self.tool_change)

        self.tool_button_select = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="select", text="Select")
        self.tool_button_select.grid(row=0, column=0, sticky="WE", padx=5)

        self.tool_button_place = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="new", text="New")
        self.tool_button_place.grid(row = 0, column=1, sticky="WE", padx=5)

        self.tool_button_delete = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="delete", text="Delete")
        self.tool_button_delete.grid(row = 0, column=2, sticky="WE", padx=5)

        self.tool_button_move = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="move", text="Move")
        self.tool_button_move.grid(row = 0, column=3, sticky="WE", padx=5)

        self.tool_button_copy = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="copy", text="Copy")
        self.tool_button_copy.grid(row = 1, column=0, sticky="WE", padx=5)

        self.tool_button_paste = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="paste", text="Paste")
        self.tool_button_paste.grid(row = 1, column=1, sticky="WE", padx=5)

        self.tool_button_dup = ttk.Radiobutton(self.toolbar_frame, variable=self.current_tool_variable, value="dup", text="Duplicate")
        self.tool_button_dup.grid(row = 1, column=2, columnspan=2, sticky="WE", padx=5)

        #space between object tools and object list 
        self.place_holder_label=ttk.Label(self)
        self.place_holder_label.grid(row=2, column=0)

        # === object list
        # subscribe to object change events to get notified when object list should change
        events.objects_change.subscribe(self.update_object_list)
        events.object_prop_change.subscribe(self.update_object_props)
        events.selection_change.subscribe(self.update_selection)

        # headline object list
        self.headline_object_list = Headline(self, text="Objects")
        self.headline_object_list.grid(row=3, column=0, sticky="WE", padx=10, pady=10)
        
        # create the tree view to display all the objects
        columns = ("active")
        self.object_tree=ttk.Treeview(self, columns=columns, show="tree headings")
        self.object_tree.grid(row=4, column=0, sticky="WNE", padx=10)
        
        # define the headings
        self.object_tree.heading("#0", text="Name")
        self.object_tree.heading("active", text="Active")

        # configuring columns
        self.object_tree.column("#0", width=150, anchor="w")    # automatic first column
        self.object_tree.column("active", width=50, anchor="w")

        # dict to map treeview id's to actual objects
        self.tree_id_to_obj: dict[str, SimObject] = {}

        # default object to list
        self.object_tree_default_object = self.object_tree.insert("", tk.END, id="default", text="Default Object", values=(str(True)), tags=("default"))
        self.configure_colors("default", sim_space.default_object.color)

        # get notification when selection is made
        self.object_tree.bind("<<TreeviewSelect>>", self.treeview_select_callback)


        # === Object properties
        self.obeject_prop=ObjectPropFrame(self)
        self.obeject_prop.grid(row=6, column=0, sticky="WNE")
        
        
        
        # update object list manualy the first time
        self.update_object_list()
    
    # method that automatically configures back and foreground of a treeview tag depending on the given background color
    def configure_colors(self, tag_name: str, bgcolor: str):
        # turn color string in a float rgb value (0.0 - 1.0)
        red, green, blue = tuple(c / 65535 for c in self.winfo_rgb(bgcolor))
        # ajust fg for bg brightness https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        fgcolor = "black" if (red*0.299 + green*0.587 + blue*0.114) > 183 else "white"
        self.object_tree.tag_configure(tag_name, background=bgcolor, foreground=fgcolor)

    # trace callback for self.current_tool_variable
    def tool_change(self, a, b, c):
        config.dyn.tool = self.current_tool_variable.get()
    
    # method to update object list with current objects (also used as objects_change event callback)
    def update_object_list(self, event_data=...):
        # delete old items
        for id, obj in self.tree_id_to_obj.copy().items():
            if not obj in sim_space.objects:
                self.object_tree.delete(id)
                self.tree_id_to_obj.pop(id)
        # potentially add new items
        for obj in sim_space.objects:
            if not obj in self.tree_id_to_obj.values():
                # add the object
                new_id = self.object_tree.insert("", tk.END, text=obj.name, values=(str(bool(obj.active))))
                self.object_tree.item(new_id, tags=(new_id))
                self.configure_colors(new_id, obj.color)
                self.tree_id_to_obj[new_id] = obj
    
    # object property change event callback to update all properties of the current objects with new values
    def update_object_props(self, event_data=...):
        # default objects
        self.object_tree.item(self.object_tree_default_object, text=sim_space.default_object.name, values=(str(bool(sim_space.default_object.active))))
        # regular objects
        for id, obj in self.tree_id_to_obj.items():
            self.object_tree.item(id, text=obj.name, values=(str(bool(obj.active))))
            self.configure_colors(id, obj.color)

    # selection change event callback
    def update_selection(self, event_data=...):
        if event_data is self: return   # ignore events sent by self
        if sim_space.selected_object is ...:
            self.object_tree.selection_clear()
        else:
            # get tree view id corresponding to the object by reverse dict lookup
            selid = next(key for key, value in self.tree_id_to_obj.items() if value is sim_space.selected_object)
            # select the item
            self.object_tree.selection_set(selid)
            

    def treeview_select_callback(self, event=...):
        if len(self.object_tree.selection()) == 0:
            sim_space.selected_object = ... # deselect all
        else:
            sel = self.object_tree.selection()[0]    # only take first selection
            if sel == "default":    # if default object
                sim_space.selected_object = sim_space.default_object
            else:
                sim_space.selected_object = self.tree_id_to_obj[sel]
        events.selection_change.trigger(self) # self is transmitted for the class to know that the event was sent by itself to ignore it
       

