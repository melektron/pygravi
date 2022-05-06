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
import math

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
            # check for collisions
            for obj in self.objects:
                for obj2 in self.objects:
                    # don't check collision with self
                    if obj is obj2:
                        continue
                    if obj in done_objects:
                        continue
                    # if collison
                    if obj.pos.distance_to(obj2.pos) <= obj.radius + obj2.radius:
                        print(f"vel f: {obj.vel}, {obj2.vel}")
                        # get direction vector to other object containing the collision angle
                        direction: Vector2D = obj2.pos - obj.pos

                        # calculate main object
                        # get the angle delta of the velocity and the collision angle
                        obj_dphi = direction.phi - obj.vel.phi
                        obj2_dphi = direction.phi - obj2.vel.phi

                        # split the velocity in two vectors, one containing the velocity in the collision angle,
                        # the other one the rest that is not influencec by conservation of momentum
                        # for object 1
                        obj_collision_vel: Vector2D = Vector2D.from_polar(
                            (direction.phi, obj.vel.r*math.cos(obj_dphi)))
                        obj_carry_vel = Vector2D.from_polar(
                            (direction.phi-config.const.pi/2, obj.vel.r*math.sin(obj_dphi)))
                        # for object 2
                        obj2_collision_vel = Vector2D.from_polar(
                            (direction.phi, obj2.vel.r*math.cos(obj2_dphi)))
                        obj2_carry_vel = Vector2D.from_polar(
                            (direction.phi-config.const.pi/2, obj2.vel.r*math.sin(obj2_dphi)))

                        # calculating the conservation of momentum using the absloute collision velocity according to
                        # v1' = (m1*v1 + m2*(2*v2-v1)) / (m1+m2)
                        # for object 1
                        obj_vel_after = obj.mass * obj_collision_vel.r
                        obj_vel_after += obj2.mass * \
                            (2 * obj2_collision_vel.r-obj_collision_vel.r)
                        obj_vel_after /= obj.mass + obj2.mass
                        # for object 2
                        obj2_vel_after = obj2.mass * obj2_collision_vel.r
                        obj2_vel_after += obj.mass * \
                            (2 * obj_collision_vel.r-obj2_collision_vel.r)
                        obj2_vel_after /= obj2.mass + obj.mass

                        # change the value of the collision velocity but keep the angle from before
                        print(
                            f"col vel before: {obj_collision_vel}, {obj_collision_vel}")
                        obj_collision_vel.r = obj_vel_after
                        obj2_collision_vel.r = obj2_vel_after
                        print(
                            f"col vel after : {obj_collision_vel}, {obj_collision_vel}")

                        # set the final velocity of the objects to the carry velocity (that was not affected by the collision)
                        # plus the collision velocity that has been modified
                        obj.vel = obj_carry_vel + obj_collision_vel
                        obj2.vel = obj2_carry_vel + obj2_collision_vel

                        # declare these two objects as done
                        done_objects += [obj, obj2]

                        print(f"vel a: {obj.vel}, {obj2.vel}")

        # calculate the movement based on the current velocity
        for obj in self.objects:
            if not obj.active: continue
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
