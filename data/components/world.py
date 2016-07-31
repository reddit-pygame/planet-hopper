from math import sqrt
from random import randint, sample, choice, uniform

import pygame as pg

from .. import prepare
from .angles import get_distance, get_angle, project
from .planet import Planet, PLANET_COLORS
from .ship import Ship
from .captain import Captain


class World(object):
    """A single World object represents the entire simulation."""
    def __init__(self, planet_values):
        self.planets = self.make_planets(planet_values)
        self.distances = self.get_distances()
        foods = [x for x in  self.planets.values() if x.resource == "Food"]
        self.ship = Ship(choice(foods))
        world_info = self.get_planet_info()
        ship_info = self.ship.get_info()
        self.captain = Captain(world_info, ship_info, self.distances)
        self.day = 0
        
    def make_planets(self, planet_values):
        planets = {} 
        self.planet_group = pg.sprite.Group()
        for n, image, rpm, resource, color, pos, radius in planet_values:
            img = prepare.GFX[image]    
            planet = Planet(n, img, rpm, resource, color, pos, radius, self.planet_group)
            planets[n] = planet
        return planets
        
    def get_planet_info(self):
        planet_info = {}
        for p in self.planets.values():
            planet_info[p.name] = p.get_info()
        return planet_info
            
    def get_distances(self):
        d = {}
        for planet in self.planets.values():
            name = planet.name
            d[name] = {}
            for other in self.planets.values():
                d[name][other.name] = get_distance(planet.pos, other.pos)
        return d                

    def load_cargo(self, cargo, num_colonists):
        if self.ship.location:
            planet = self.ship.location
            inv = planet.inventory
            for c in cargo:
                amt = cargo[c]
                if inv[c] >= amt:
                    self.ship.cargo[c] += amt
                    inv[c] -= amt
                else:
                    self.ship.cargo += inv[c]
                    inv[c] = 0
            if planet.num_colonists >= num_colonists:
                planet.num_colonists -= num_colonists
                self.ship.num_colonists += num_colonists

    def follow_orders(self, orders):
        if orders["destination"] is not None:
            self.load_cargo(orders["cargo"], orders["colonists"])
            destination = self.planets[orders["destination"]]
            self.ship.travel(destination, self)
            
    def daily_update(self):
        self.day += 1
        for p in self.planets.values():
            p.daily_update()
        if self.ship.docked:
            planet_info = self.get_planet_info()
            ship_info = self.ship.get_info()
            orders = self.captain.get_orders(planet_info, ship_info, self.distances)
            self.follow_orders(orders)


