"""
Author:
melektron
"""


import tkinter.ttk as ttk
import tkinter as tk


class Window:
    def __init__(self, master = None):
        self.win = tk.Tk()
        self.button = ttk.Button(master = self.win, text="hello")
        self.button.pack()
    
    def mainloop(self):
        self.win.mainloop()

if __name__ == "__main__":
    mywindow = Window()
    mywindow.mainloop()
