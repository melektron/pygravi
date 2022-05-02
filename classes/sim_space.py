"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
02.05.22 18:50

The space that the simulation will take place int

"""

import classes.config as config
from classes.vector import Vector2D


# Class that defines a physical object in the simulation
class SimObject:
    # the id of the corresponding canvas object
    # set when first drawn on the canvas
    canvas_id: int = None

    def __init__(self, name: str, r: float, pos: Vector2D, mass: float):
        self.name: str = name
        self.radius: float = r
        self.pos: Vector2D = pos
        self.mass: float = mass

    
    def gforce(self, other: "SimObject") -> Vector2D:
        # calculates the gravitational force to another object
        
        # get the distance vector between the objects
        distance: Vector2D = other - self
        # calculate gravitational force vector
        return (config.dyn.G * self.mass * other.mass) / (distance * distance)
        




class _SimSpace:
    def __init__(self):
        pass
