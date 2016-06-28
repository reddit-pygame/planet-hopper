from random import choice
from itertools import cycle

import pygame as pg


        
class Captain(object):
    def __init__(self, world_info, ship_info, distances):
        dists = []
        for planet in distances:
            total = sum(distances[planet].values())
            dists.append((planet, total))
        dists.sort(key=lambda x: x[1])
        self.base = dists[0][0]
        self.route = self.make_route(world_info)
        speed = ship_info["speed"]
        self.route_days = self.get_total_route_time(distances, speed)
        self.destinations = cycle(self.route)
        
    def get_total_route_time(self, distances, speed):
        total = 0
        x = self.route[0]
        for p in self.route:
            total += distances[x][p] // speed
            x = p
        total += distances[self.route[0]][self.route[-1]] // speed          
        return total
        
    def make_route(self, world_info):
        dests = [x for x in world_info.keys() if x != self.base]
        route = []
        for d in dests:
            route.append(d)
            route.append(self.base)
        return route
        
    def get_orders(self, world_info, ship_info, distances):
        """
        
        Choose cargo, passengers and destination
        for next trip. This method is called once each day
        while the ship is docked on a planet.
        
        "destination": the name of the planet to travel to
        "cargo": a dict of what cargo should be brought on board
        "colonists": the number of colonists to deliver to the next planet
        
        Parameters
        *********
        world_info: a dict of dicts keyed by planet name
                        each planet

        ship_info: a dict of information  
        """
        destination = next(self.destinations)
        w = world_info
        loc = ship_info["location"]
        
        cargo = {}
        if  loc == self.base:
            for g in w[loc]["inventory"]:
                if g != w[destination]["resource"]:
                    base_need = w[loc]["consumption"][g] * self.route_days
                    amt = w[destination]["consumption"][g] * self.route_days
                    onhand = w[loc]["inventory"][g]
                    if onhand > base_need + amt:
                        haul = amt
                    elif onhand > base_need:
                        haul = onhand - base_need
                    else:
                        haul = 0
                    cargo[g] = haul
                
        else:
            good = w[loc]["resource"]
            amt = w[loc]["inventory"][good]
            cargo[good] = amt        
      
        orders = {
            "destination": destination,
            "cargo": cargo,
            "colonists": 0}
        return orders
        
   