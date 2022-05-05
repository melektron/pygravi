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
                    acctime.delayMicroseconds(config.dyn.sframedelay)
                else:
                    time.sleep(.1)
        except Exception:
            print_exc()
        
    def do_sim_frame(self) -> None:
        # function that runns the calculations for each simulation frame
        if config.dyn.do_gravity:
            # calculate the force vectors
            for obj in self.objects:
                obj.force.cart = (0, 0)
                for obj2 in self.objects:
                    obj.force = obj.force + obj.gforce(obj2)
                    #print("Object: ", obj.name, "\tPos: ", obj.pos, "\tOhter: ", obj2.pos, "\tTemp Force: ", obj.force)

            # calculate velocity based on the current force
            for obj in self.objects:
                # acceleration caused by the force on the object
                accel: Vector2D = obj.force / obj.mass
                # add the velocity caused by the acceleration in the configured time step to the object velocity
                obj.vel += accel * config.dyn.deltat
        
        # ?????
        if config.dyn.do_collision:
            # check for collisions
            for obj in self.objects:
                for obj2 in self.objects:
                    # don't check collision with self
                    if obj is obj2:
                        continue
                    # if collison
                    if obj.pos.distance_to(obj2.pos) <= obj.radius + obj2.radius:
                        # get direction vector to other object for calculating collision angle
                        direction: Vector2D = obj2.pos - obj.pos
                        
                        # calculate main object
                        # get the angle delta of the velocity to the collision angle
                        dphi = direction.phi - obj.vel.phi
                        # mirror the velocity across the collison angle line and invert it



                        # calculate influencing object (obj2)
        
        # calculate the movement based on the current velocity
        for obj in self.objects:
            obj.pos += obj.vel * config.dyn.deltat

       




        

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
