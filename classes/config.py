"""
Author:
melektron
"""

import json as j
import shutil
from typing import Any


class ConfigPermissionError(BaseException):
    ...


class _Confhive:
    init_done: bool = False

    def __init__(self, hivefile: str) -> None:
        self.__hivefile = hivefile

        # load the config hive file
        try:
            fd = open(hivefile, "r")
        except FileNotFoundError:
            # create file from default file
            shutil.copy(hivefile + ".default", hivefile)
            fd = open(hivefile, "r")

        self.__hive: dict = j.load(fd)
        fd.close()
        # get the hive name and permissions
        self.__hivename: str = self.__hive["hivename"]
        self.__wprot: bool = self.__hive["writeprotect"]

        # load all the values
        for key, value in self.__hive["keys"].items():
            # load arguments
            self.__dict__[key] = value
        
        self.init_done = True

    # catch attribute asign events
    def __setattr__(self, config_key: str, value: Any) -> None:
        if self.init_done:
            if self.__wprot:
                raise ConfigPermissionError(
                    f"Config hive {self.__hivename} is write protected")
            self.__dict__[config_key] = value   # save to class dict
            self.__hive["keys"][config_key] = value # save to hive dict
        else:
            self.__dict__[config_key] = value   # before init is done, use a default implementation of __setattr__
                                                # to be able to set attributes normally
    
    # method that saves the current state to file
    def save(self):
        if self.__wprot:
            return
        with open(self.__hivefile, "w") as fd:
            j.dump(self.__hive, fd)

    # export written config to file uppon deletion unless the hive is write protected
    #def __del__(self):
    #    if self.__wprot:
    #        return
    #    self.save()

        


user = _Confhive("config/user.json")
const = _Confhive("config/const.json")
dyn = _Confhive("config/dyn.json")
