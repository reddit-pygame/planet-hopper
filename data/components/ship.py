from math import degrees, sqrt
import pygame as pg

from .. import prepare
from .resources import RESOURCES
from .angles import get_distance, get_angle, project
from .labels import Label


class Ship(object):
    def __init__(self, planet):
        self.cargo = {x: 0 for x in RESOURCES}
        self.num_colonists = 0
        self.uranium = 0
        self.parts = 0
        self.repair_level = 100
        self.base_image = prepare.GFX["cargoship"]
        self.pos = planet.pos
        self.rect = self.base_image.get_rect(center=self.pos)
        self.destination = None
        self.image = self.base_image
        self.speed = 20
        self.animations = pg.sprite.Group()
        self.destination = planet
        self.dock()
        
    def get_info(self):
        info = {}
        info["location"] = self.location.name
        if self.destination:
            dest = self.destination.name
        else:
            dest = "None"
        info["speed"] = self.speed    
        info["destination"] = dest
        info["pos"] = self.rect.center
        info["cargo"] = {k: v for k, v in self.cargo.items()}
        info["colonists"] = self.num_colonists
        return info
        
    def show_info(self, surface):
        labels = pg.sprite.Group()
        w, h  = 200, 220
        surf = pg.Surface((w, h))
        surf.fill(pg.Color("gray10"))
        dest = "None"
        if self.destination:
            dest = self.destination.name
        Label("Destination: {}".format(dest), {"topleft": (0, 0)},
                labels)
        top = 30
        for i in self.cargo:
            lab1 = Label(i, {"topleft": (5, top)}, labels, text_color="gray85")
            lab4 = Label("{}".format(self.cargo[i]), {"topleft": (80, top)}, labels, text_color="gray80")
            top += 20
        labels.draw(surf)
        cx, cy = prepare.SCREEN_RECT.center
        if self.rect.right < cx:
            left = self.rect.right
        elif self.rect.left > cx:
            left = self.rect.left - w
        else:
            left = self.rect.centerx - (w//2)
        if self.rect.bottom < cy:
            top = self.rect.bottom
        else:
            top = self.rect.top - h
        rect = surf.get_rect(topleft=(left, top))
        surface.blit(surf, rect)
        
    def offload(self):
        planet = self.destination
        for good in self.cargo:
            planet.inventory[good] += self.cargo[good]
            self.cargo[good] = 0
            
    def dock(self):
        self.offload()
        self.docked = True
        self.rect.center = self.destination.pos
        self.pos = self.rect.center
        self.location = self.destination
        self.velocity = (0, 0)
        self.destination = None
        
    def travel(self, destination, world):
        if destination is None:
            return
        p1 = self.rect.center
        p2 = destination.pos
        dist = get_distance(p1, p2)
        if dist != 0:
            self.destination = destination
            self.location = "Space"
            angle = get_angle(p1, p2)
            self.velocity = project((0, 0), angle, 1)
            self.image = pg.transform.rotate(self.base_image, degrees(angle))
            self.docked = False
            
    def update(self):
        if self.location == "Space":
            vx, vy = self.velocity
            dx = vx * self.speed
            dy = vy * self.speed
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
            self.rect.center = self.pos
            if get_distance(self.pos, self.destination.pos) <= self.speed:
                self.dock()
        
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)


