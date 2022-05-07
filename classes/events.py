"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 11:51

events class and instances that can be used to send signals throughout the programm making use of tkinter IntVars

"""

class _Event:
    _subs: list      # list of subscribed functions
    def __init__(self):
        self._subs = []
    
    def trigger(self, value=0):
        for sub in self._subs:
            sub(value)
    
    def subscribe(self, callback):
        self._subs.append(callback)
    
# predefined events

# objects
objects_change: _Event = _Event()   # objects have been added/removed (no value)
selection_change: _Event = _Event() # selected object has changed (no value)
object_prop_change: _Event = _Event()   # an object property was changed, some views migth have to refresh

# view
show_force: _Event = _Event()   # value is True/False for ON/OFF
show_velocity: _Event = _Event()   # value is True/False for ON/OFF

