from random import choice, sample, uniform, randint
import json

import pygame as pg

from .. import prepare
from .planet import PLANET_COLORS


prefixes = ["Gul", "Krel", "Grim", "Ar", "Vog", "Brel",
                "Zar", "Hol", "Vel", "Rek", "Sar", "Zil"]
suffixes = ["nib", "vex", "vin", "bin", "bos", "nos",
                "tos", "bis", "nis", "tis", "nex", "blit"]

def make_names(num_planets):
        names = []
        pre = sample(prefixes, num_planets)
        suf = sample(suffixes, num_planets)
        return ["{}{}".format(p, s) for p, s in zip(pre, suf)]

def make_planets():
    sr = prepare.SCREEN_RECT
    planets = {}
    resources = ["Food", "Aluminum", "Uranium", "Titanium", "Plastic", "Gold"]
    num_planets = len(resources)
    img_names = ["planet{}".format(x) for x in range(1, 11)]
    images = [choice(img_names) for _ in range(num_planets)]
    colors = sample(PLANET_COLORS, num_planets)
    names = make_names(num_planets)
    rpms = [uniform(.5, 2.0) for _ in range(len(resources))]
    radii = [randint(30, 60) for r in range(len(resources))]
    positions = []
    rects = []
    for radius in radii:
        w = radius * 2
        pos = randint(radius, sr.w - radius), randint(radius, sr.h - radius)
        rect = pg.Rect(0, 0, w, w)
        rect.center = pos
        while any((x.colliderect(rect) for x in rects)):
            pos = randint(radius, sr.w - radius), randint(radius, sr.h - radius)
            rect = pg.Rect(0, 0, w, w)
            rect.center = pos
        rects.append(rect)
        positions.append(rect.center)
    print "postions: ", positions    
    return zip(names, images, rpms, resources, colors, positions, radii)

def generate_worlds():
    worlds = {}
    for i in range(5):
        worlds[i] = make_planets()
    with open("worlds.json", "w") as f:
        json.dump(worlds, f)
