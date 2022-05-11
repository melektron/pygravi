"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter) and MrFlunter (Florian Unterpertinger)
www.elektron.work
02.05.22 18:44

test


Main file for gravity sim
"""

import platform
import tkinter.ttk as ttk
import tkinter as tk
import classes.config as config
from classes.sim_space import sim_space
import classes.render_frame
import classes.config_frame
import classes.edit_frame
import classes.antiblurr
import classes.planets
import classes.events as events



class Window(tk.Tk):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # don't allow window config changes to be saved just jet
        self.wnd_save_config_flag = False

        self.title("PyPhySim v1.1dev")
        if platform.system().lower().startswith("windows"):
            self.iconbitmap('resource/pyphysim_logo.ico')
        elif platform.system().lower().startswith("linux"):
            self.iconbitmap('@resource/pyphysim_logo.xbm')

        self.columnconfigure(1, weight=3)
        #self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)
        
        self.edit_frame = classes.edit_frame.EditFrame(self, width=350)
        self.edit_frame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
        self.edit_frame.grid_propagate(0)  # keep left column fixed size (width)

        self.render_frame = classes.render_frame.RenderFrame(self, width=300)
        self.render_frame.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

        self.config_frame = classes.config_frame.ConfigFrame(self, width=350)
        self.config_frame.grid(row=1, column=2, sticky="NS", padx=5, pady=5)
        self.config_frame.grid_propagate(0)  # keep right column fixed size (width)
        
        # === register global keyboard shortcuts
        self.bind_all("<Control-e>", self.ccb_e, "+")
        self.bind_all("<Control-n>", self.ccb_n, "+")
        self.bind_all("<Control-BackSpace>", self.ccb_del, "+")
        self.bind_all("<Delete>", self.ccb_del, "+")    
        self.bind_all("<Control-m>", self.ccb_m, "+")
        self.bind_all("<Control-c>", self.ccb_c, "+")
        self.bind_all("<Control-v>", self.ccb_v, "+")
        self.bind_all("<Control-d>", self.ccb_d, "+")
        self.bind_all("<F11>", self.ccb_f11, "+")

        # window config change to store the last position and size
        self.bind("<Configure>", self.wnd_cfg)

        self.after(config.dyn.visual_framedelay, self.render_objects)

        # load last geometry from file and configure window in the same way
        self.geometry(f"{config.dyn.geometry['w']}x{config.dyn.geometry['h']}+{config.dyn.geometry['x']}+{config.dyn.geometry['y']}")
        self.set_fs(config.dyn.geometry['fullscreen'])

        # save window size and position changes from now on
        self.wnd_save_config_flag = True
        
    
    def ccb_s(self, event=...):
        pass
    
    def ccb_e(self, event=...):
        config.dyn.tool = "select"
        events.tool_change.trigger()
        pass
    
    def ccb_n(self, event=...):
        config.dyn.tool = "new"
        events.tool_change.trigger()
        pass
    
    def ccb_del(self, event=...):
        if self.render_frame.tool_action_active: return     # if an action is active, stop
        if sim_space.selected_object is not ...:
            if sim_space.selected_object in sim_space.objects:
                sim_space.objects.remove(sim_space.selected_object)
                events.objects_change.trigger()
            sim_space.selected_object = ...
            events.selection_change.trigger()
        else:
            config.dyn.tool = "delete"
            events.tool_change.trigger()
    
    def ccb_m(self, event=...):
        if self.render_frame.tool_action_active: return     # if an action is active, stop
        if sim_space.selected_object is not ...:
            self.render_frame.initiate_move(sim_space.selected_object)
        else:
            config.dyn.tool = "move"
            events.tool_change.trigger()
        pass
    
    def ccb_c(self, event=...):
        if self.render_frame.tool_action_active: return     # if an action is active, stop
        if sim_space.selected_object is not ...:
            self.render_frame.copy_selection()
        else:
            config.dyn.tool = "copy"
            events.tool_change.trigger()
        pass
    
    def ccb_v(self, event=...):
        if self.render_frame.tool_action_active: return     # if an action is active, stop
        if sim_space.clipboard_object is not ...:
            self.render_frame.initiate_paste()
        else:
            config.dyn.tool = "paste" 
            events.tool_change.trigger()
        pass
    
    def ccb_d(self, event=...):
        if self.render_frame.tool_action_active: return     # if an action is active, stop
        if sim_space.selected_object is not ...:
            self.render_frame.copy_selection()
            self.render_frame.initiate_paste()
        else:
            config.dyn.tool = "duplicate"
            events.tool_change.trigger()
        pass
    
    def ccb_f11(self, event=...):
        config.dyn.geometry["fullscreen"] = not config.dyn.geometry["fullscreen"]
        self.set_fs(config.dyn.geometry["fullscreen"])

    def set_fs(self, val: bool):
        if platform.system().lower().startswith("windows"):
            self.attributes("-fullscreen", bool(val))
        elif platform.system().lower().startswith("linux"):
            self.attributes("-fullscreen", bool(val))
        config.dyn.geometry["fullscreen"] = bool(val)
    
    def wnd_cfg(self, event: tk.Event=...):
        if self.wnd_save_config_flag:
            if event.widget == self: # only if the values apply to the main window
                # save the position 
                config.dyn.geometry["x"] = event.x
                config.dyn.geometry["y"] = event.x
                config.dyn.geometry["w"] = event.width
                config.dyn.geometry["h"] = event.height

    def render_objects(self) -> None:
        # Render Start
        self.render_frame.render_objects(sim_space.objects)
        # Render End
        # recall render after x time
        self.after(config.dyn.visual_framedelay, self.render_objects)


if __name__ == "__main__":
    #myobj = classes.planets.Planets.planet_to_object(classes.planets.Planets.request_planet_data("earth")[0])
    #sim_space.append_object(myobj)
    sim_space.load_objects(config.user.objects)
    sim_space.load_default_object(config.user.default_object)
    events.objects_change.trigger() # notify about object change
    mywindow = Window()
    
    #mywindow.state("zoomed")
    #mywindow.geometry("1600x800")
    mywindow.mainloop()
    sim_space.stop_simulation()

    # save the config
    config.user.save()
    config.dyn.save()
    # const cannot be saved
