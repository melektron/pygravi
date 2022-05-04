"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
02.05.22 18:50

The space that the simulation will take place int

"""

from typing import TypedDict
import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import classes.config as config
from classes.vector import Vector2D
from traceback import print_exc


# Class that defines a physical object in the simulation
class SimObject:
    # the ids of the corresponding canvas objects
    # set when first drawn on the canvas
    ca_circle_id: int = ...
    ca_fvector_id: int = ...
    

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
        # avoid division by zero because of zero distance
        if other is self:
            return Vector2D(0, 0)
        # calculates the gravitational force to another object
        # get the distance vector between the objects
        direction: Vector2D = other.pos - self.pos
        # calculate gravitational force vector
        absforce: float =  (float(config.dyn.G) * self.mass * other.mass) / self.pos.distance_to(other.pos)
        direction.r = absforce
        return direction


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

    # executer pool
    exec_pool: PoolExecutor = ...

    SIGTERM: bool = False

    running: bool = False

    def __init__(self):
        self.objects = []

        # initialize the thread pool executor
        self.exec_pool = PoolExecutor(max_workers=10)
        self.simulation_thread = self.exec_pool.submit(self.simulation_func)
        pass

    def load_objects(self, exp_obj: list[_ObjExportType]) -> None:
        for obj in exp_obj:
            self.objects.append(SimObject(obj["name"], obj["radius"], obj["mass"], Vector2D.from_cart(
                obj["pos"]), Vector2D.from_cart(obj["vel"]), Vector2D.from_cart(obj["force"])))
    
    def simulation_func(self) -> None:
        # method that runs in a thread and handles sim frame timing
        try:
            while not self.SIGTERM:
                if self.running:
                    self.do_sim_frame()
                    time.sleep(config.dyn.sframedelay / 1000)
                else:
                    time.sleep(.1)
        except Exception:
            print_exc()
        
    def do_sim_frame(self) -> None:
        # function that runns the calculations for each simulation frame
        # turn one object
        self.objects[-1].pos.phi = self.objects[-1].pos.phi + 0.01

        for obj in self.objects:
            sforce: Vector2D = (obj.force * obj.mass * (config.dyn.deltat**2)) / 2
            svel: Vector2D = obj.vel * config.dyn.deltat

        # calculate the force vectors
        for obj in self.objects:
            obj.force.cart = (0, 0)
            for obj2 in self.objects:
                obj.force = obj.force + obj.gforce(obj2)
                #print("Object: ", obj.name, "\tPos: ", obj.pos, "\tOhter: ", obj2.pos, "\tTemp Force: ", obj.force)

    def run_simulation(self) -> None:
        self.running = True
        self.SIGTERM = False
        if self.simulation_thread.done():
            self.exec_pool.submit(self.simulation_func)
    
    def pause_simulation(self) -> None:
        self.running = False
    
    def stop_simulation(self) -> None:
        self.SIGTERM = True


sim_space = _SimSpace()
