"""
Author:
MrFlunter
"""

import tkinter as tk
import tkinter.ttk as ttk
 
class ConfigFrame:
    def __init__(self, master):
        self.master = master
 
        frame = ttk.Frame(self.master, borderwidth=2, relief=tk.GROOVE)
 
        #Headline
        headline=ttk.Label(frame,text="Settings")

        def output_Schieberegler1(v): 
            Schieberegler1.config(text='you select ' + v) 

        Schieberegler1=ttk.Label(frame)

        button = ttk.Button(frame, text = "Click Me!", style = "Custom.TButton")
        button.pack()
 
        frame.pack(padx = 5, pady = 5)
 
if __name__ =="__main__": 
    root = tk.Tk()
    root.geometry("300x400")
    frame=ConfigFrame(root)


    root.mainloop()
    
