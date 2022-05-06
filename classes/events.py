"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 11:51

events class and instances that can be used to send signals throughout the programm making use of tkinter IntVars

"""

class _Event:
    subs: list      # list of subscribed functions
    def __init__(self):
        subs = []
    
    def trigger(self, value=0):
        for sub in self.subs:
            sub(value)
    
    def subscribe(self, callback: function):
        self.subs.append(callback)
    
# predefined events
selection_change: _Event = _Event()

