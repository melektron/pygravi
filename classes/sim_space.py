"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
02.05.22 18:50

The space that the simulation will take place int

"""

from typing import TypedDict
import classes.config as config
from classes.vector import Vector2D



# Class that defines a physical object in the simulation
class SimObject:
    # the id of the corresponding canvas object
    # set when first drawn on the canvas
    canvas_id: int = ...

    # physical attributes
    name: str          # readable and identifiable name of the object
    radius: float      # radius of the object (sphere)
    mass: float        # mass of the object
    pos: Vector2D      # current position of the object
    vel: Vector2D      # current object velocity
    force: Vector2D    # current force on the object

    def __init__(self, name: str, r: float, mass: float, pos: Vector2D = ..., vel: Vector2D = ..., force: Vector2D = ...):
        if pos is ...:
            self.pos = Vector2D(0, 0)
        else:
            self.pos = pos

        if vel is ...:
            self.vel = Vector2D(0, 0)
        else:
            self.vel = vel

        if force is ...:
            self.force = Vector2D(0, 0)
        else:
            self.force = force

        self.name: str = name
        self.radius: float = r
        self.mass: float = mass

    def gforce(self, other: "SimObject") -> Vector2D:
        # calculates the gravitational force to another object

        # get the distance vector between the objects
        distance: Vector2D = other - self
        # calculate gravitational force vector
        return (config.dyn.G * self.mass * other.mass) / (distance * distance)


class _ObjExportType(TypedDict):
    name: str
    radius: float
    mass: float
    pos: list    # Vector
    vel: list    # Vector
    force: list  # Vector


class _SimSpace:

    # list of all objects
    objects: list[SimObject] = ...

    def __init__(self):
        self.objects = []
        pass

    def load_objects(self, exp_obj: list[_ObjExportType]) -> None:
        for obj in exp_obj:
            self.objects.append(SimObject(obj["name"], obj["radius"], obj["mass"], Vector2D.from_cart(
                obj["pos"]), Vector2D.from_cart(obj["vel"]), Vector2D.from_cart(obj["force"])))


sim_space = _SimSpace()
