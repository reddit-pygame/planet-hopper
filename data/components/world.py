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
    prefixes = ["Gul", "Krel", "Grim", "Ar", "Vog", "Brel", "Zar", "Hol", "Vel", "Rek", "Sar", "Zil"]
    suffixes = ["nib", "vex", "vin", "bin", "bos", "nos", "tos", "bis", "nis", "tis", "nex", "blit"]
    def __init__(self):
        self.planets = self.make_planets()
        self.distances = self.get_distances()
        foods = [x for x in  self.planets.values() if x.resource == "Food"]
        self.ship = Ship(choice(foods))
        world_info = self.get_planet_info()
        ship_info = self.ship.get_info()
        self.captain = Captain(world_info, ship_info, self.distances)
        self.day = 0
        
    def make_names(self, num_planets):
        names = []
        pre = sample(self.prefixes, num_planets)
        suf = sample(self.suffixes, num_planets)
        for p, s in zip(pre, suf):
            names.append("{}{}".format(p, s))
        return names
        
    def make_planets(self):
        sr = prepare.SCREEN_RECT
        planets = {}
        self.planet_group = pg.sprite.Group()
        resources = ["Food", "Aluminum", "Uranium", "Titanium", "Plastic", "Gold"]
        num_planets = len(resources)
        img_names = ["planet{}".format(x) for x in range(1, 11)]
        images = [choice(img_names) for _ in range(num_planets)]
        colors = sample(PLANET_COLORS, num_planets)        
        names = self.make_names(num_planets)
        for n, resource, image, color in zip(names, resources, images, colors):
            img = prepare.GFX[image]
            rpm = uniform(.5, 2.0)
            radius = randint(30, 60)
            w = radius * 2
            pos = randint(radius, sr.w - radius), randint(radius, sr.h - radius)
            rect = pg.Rect(0, 0, w, w)
            rect.center = pos
            while any((x.rect.colliderect(rect) for x in planets.values())):
                pos = randint(radius, sr.w - radius), randint(radius, sr.h - radius)
                rect = pg.Rect(0, 0, w, w)
                rect.center = pos
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

    def load_cargo(self, cargo):
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
                    
    def follow_orders(self, orders):
        if orders["destination"] is not None:
            self.load_cargo(orders["cargo"])
            destination = self.planets[orders["destination"]]
            self.ship.travel(destination, self)
            
    def daily_update(self):
        self.day += 1
        for p in self.planets.values():
            p.produce()
            p.consume()
        if self.ship.docked:
            planet_info = self.get_planet_info()
            ship_info = self.ship.get_info()
            orders = self.captain.get_orders(planet_info, ship_info, self.distances)
            self.follow_orders(orders)


