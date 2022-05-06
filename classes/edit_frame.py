"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 11:51

The GUI frame on the left of the window for adding/remoing/selecting simulation objects

"""

import tkinter as tk
import tkinter.ttk as ttk
import classes.config as config


class Headline(ttk.Frame):
    def __init__(self, master, text="", **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)
        self.headline_label = ttk.Label(self, text=text, font=(24))
        self.headline_label.grid(row=0, column=0, sticky="W", padx=5)

class EditFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master, borderwidth=2, relief=tk.GROOVE, **kwargs)

        self.columnconfigure(0, weight=1)

        # === object tools
        # Headline
        self.headline_object_tools = Headline(self, text="Object Tools")
        self.headline_object_tools.grid(row=0, column=0, sticky="WE")

        # toolbar
        self.toolbar_frame = ttk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.toolbar_frame.grid(row=1, column=0, sticky="WE", padx=5)
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


        # === object list
        # headline object list
        self.headline_object_list = Headline(self, text="Objects")
        self.headline_object_list.grid(row=2, column=0, sticky="WE")


    # trace callback for self.current_tool_variable
    def tool_change(self, a, b, c):
        config.dyn.tool = self.current_tool_variable.get()
