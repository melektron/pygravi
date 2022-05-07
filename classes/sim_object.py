"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 17:29

A class that represents a single object (ball) in the simulation

"""

from classes.vector import Vector2D
import classes.config as config

# Class that defines a physical object in the simulation


class SimObject:
    # the ids of the corresponding canvas objects
    # set when first drawn on the canvas
    ca_circle_id: int = ...
    ca_fvector_id: int = ...
    ca_vvector_id: int = ...

    # physical attributes
    name: str          # readable and identifiable name of the object
    radius: float      # radius of the object (sphere)
    mass: float        # mass of the object
    pos: Vector2D      # current position of the object
    vel: Vector2D      # current object velocity
    force: Vector2D    # current force on the object
    active: bool       # flag if the object should be simulated or not
    statio: bool         # stationary flag. if true, this object cannot move^
    color: str         # the fill color for rendering unless it is overridden be the renderer

    def __init__(
        self, 
        name: str, 
        r: float, 
        mass: float, 
        pos: Vector2D = ..., 
        vel: Vector2D = ..., 
        force: Vector2D = ..., 
        active: bool = True,
        statio: bool = False,
        color: str = "black"
        ):
        

        

        self.name: str = name
        self.radius: float = r
        self.mass: float = mass
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
        self.active = active
        self.statio = statio
        self.color = color

    def gforce(self, other: "SimObject") -> Vector2D:
        # avoid division by zero because of zero distance
        if other is self:
            return Vector2D(0, 0)
        # calculates the gravitational force to another object
        # get the distance vector between the objects
        direction: Vector2D = other.pos - self.pos
        # calculate gravitational force vector
        absforce: float = (float(config.dyn.G) * self.mass *
                           other.mass) / self.pos.distance_to(other.pos)
        direction.r = absforce
        return direction
    
    # creates a new copy with identical properties, shape descripdors will not be copied
    def copy(self) -> "SimObject":
        return SimObject(
            self.name,
            self.radius,
            self.mass,
            self.pos.copy(),
            self.vel.copy(),
            self.force.copy(),
            self.active,
            self.statio,
            self.color
        )
