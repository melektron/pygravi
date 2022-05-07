"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
02.05.22 18:50

The space that the simulation will take place int

"""

from typing import TypedDict
import time
import external.GS_timing as acctime    # more accurate timing
from traceback import print_exc
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import itertools

import classes.config as config
from classes.vector import Vector2D
from classes.sim_object import SimObject


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
    selected_object: SimObject

    # executer pool
    exec_pool: PoolExecutor = ...

    SIGTERM: bool = False

    running: bool = False

    def __init__(self):
        self.objects = []
        self.selected_object: SimObject = ...

        # initialize the thread pool executor
        self.exec_pool = PoolExecutor(max_workers=10)
        self.simulation_thread = self.exec_pool.submit(self.simulation_func)
        pass

    def load_objects(self, exp_obj: list[_ObjExportType]) -> None:
        for obj in exp_obj:
            self.objects.append(SimObject(obj["name"], obj["radius"], obj["mass"], Vector2D.from_cart(
                obj["pos"]), Vector2D.from_cart(obj["vel"]), Vector2D.from_cart(obj["force"]), obj["active"]))

    def append_object(self, obj: SimObject):
        self.objects.append(obj)

    def simulation_func(self) -> None:
        # method that runs in a thread and handles sim frame timing
        try:
            while not self.SIGTERM:
                if self.running:
                    self.do_sim_frame()
                    acctime.delayMicroseconds(config.dyn.sim_framedelay)
                else:
                    time.sleep(.1)
        except Exception:
            print_exc()

    def do_sim_frame(self) -> None:
        # function that runns the calculations for each simulation frame
        if config.dyn.do_gravity:
            # calculate the force vectors
            for obj in self.objects:
                if not obj.active: continue
                obj.force.cart = (0, 0)
                for obj2 in self.objects:
                    if not obj2.active: continue
                    obj.force = obj.force + obj.gforce(obj2)
                    #print("Object: ", obj.name, "\tPos: ", obj.pos, "\tOhter: ", obj2.pos, "\tTemp Force: ", obj.force)

            # calculate velocity based on the current force
            for obj in self.objects:
                # acceleration caused by the force on the object
                accel: Vector2D = obj.force / obj.mass
                # add the velocity caused by the acceleration in the configured time step to the object velocity
                obj.vel += accel * config.dyn.sim_deltat

        if config.dyn.do_collision:
            done_objects = []   # list of all objects that have been calculated already
            # get a list of every possible combination of two different objects
            object_pairs = itertools.combinations(self.objects, 2) # 2 means two per pair
            for obj, obj2 in object_pairs:
                # if the two are colliding
                if obj.pos.distance_to(obj2.pos) <= obj.radius + obj2.radius:
                    # calculate collision using conservation of momentum and some clever vector magic
                    # Source of formula and code: https://scipython.com/blog/two-dimensional-collisions/
                    m1, m2 = obj.mass, obj2.mass
                    M = m1 + m2
                    r1, r2 = obj.pos, obj2.pos
                    d = r1.distance_to(r2)**2
                    v1, v2 = obj.vel, obj2.vel
                    u1 = v1 - 2*m2 / M * ((v1-v2) @ (r1-r2)) / d * (r1 - r2)
                    u2 = v2 - 2*m1 / M * ((v2-v1) @ (r2-r1)) / d * (r2 - r1)
                    obj.vel = u1
                    obj2.vel = u2

                    #print(f"vel a: {obj.vel}, {obj2.vel}")

        # calculate the movement based on the current velocity
        for obj in self.objects:
            if not obj.active: continue  # don't move disabled objects
            if obj.statio: continue  # don't move stationary objects
            obj.pos += obj.vel * config.dyn.sim_deltat

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
