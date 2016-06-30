from random import choice
from itertools import cycle

import pygame as pg


        
class Captain(object):
    def __init__(self, world_info, ship_info, distances):
       pass
        
    def get_orders(self, world_info, ship_info, distances):
        """
        Choose cargo, passengers and destination
        for next trip. This method is called once each day
        while the ship is docked on a planet.
        
        Method should return a dict with the following key, value pairs:
        
        "destination": the name of the planet to travel to
        "cargo": a dict of what cargo should be brought on board
        "colonists": the number of colonists to deliver to the next planet
        
        Parameters
        *********
        world_info: a dict of dicts keyed by planet name
                        each planet

        ship_info: a dict of information about the transport ship

        distances: a dict of distances between each planet        
        """
        orders = {
            "destination": None,
            "cargo": {},
            "colonists": 0}
        return orders

