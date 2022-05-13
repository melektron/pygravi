"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
05.05.22 11:51


class to load object values form real planet data provided be the 
"Solar System OpenData" API:
https://api.le-systeme-solaire.net/en/

Swagger API docs:
https://api.le-systeme-solaire.net/swagger/#/

Example request to get mars value:
https://api.le-systeme-solaire.net/rest.php/bodies/mars

More complex example searching planet by it's english name and only returning mass, id and englishName
https://api.le-systeme-solaire.net/rest.php/bodies/?data=mass,massValue,massExponent,id,englishName&filter[]=englishName,eq,pluto

"""

import requests as req
from classes.sim_object import SimObject
from classes.vector import Vector2D

class Planets:
    @staticmethod
    def request_planet_data(name: str):
        api_url = "https://api.le-systeme-solaire.net/rest.php/bodies/"
        params = {"data": "mass,massValue,massExponent,id,englishName,meanRadius", "filter": [f"englishName,eq,{name}"]}
        return req.get(api_url, params).json()["bodies"]
    
    @staticmethod
    def planet_to_object(planet: dict) -> SimObject:
        return SimObject(
            planet["englishName"], 
            planet["meanRadius"] * 1000,  # km to m
            planet["mass"]["massValue"] * pow(10, planet["mass"]["massExponent"]),
            color="#ff0000"
            )
    
    @staticmethod
    def get_scaled_planet(name: str) -> SimObject:
        planet: SimObject = Planets.planet_to_object(Planets.request_planet_data(name)[0])
        planet.radius /= 1e6
        planet.mass /= 1e17
        #print(planet)
        return planet
