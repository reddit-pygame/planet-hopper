from math import pi as PI
import pygame as pg

from .. import prepare
from .resources import RESOURCES
from .labels import Label



PLANET_COLORS = [
            (12, 93, 47),# emeraldish green
            (113, 78, 24),# tannish
            (113, 78, 24),# lilacish
            (101, 31, 28),# red desert
            (136, 163, 24),# eerie light green
            (201, 74, 0),# orange
            (131, 191, 198),# pale milky blue
            (209, 174, 0),# yellow
            (0,206,168),# venus blue
            (145, 190, 198),# icy blue
            (128, 128, 128),# medium moon grey
            (255, 127, 182),# pink
            (0, 74, 127),# vivid blue
            (0, 12, 62),# dark blue
            (127, 255, 142),# moon chees green
            (112, 93, 0),# dark mustard
            (38, 127, 0),# lime green
            (255, 178, 127),# pale desert
            (127, 51, 0),# orangey brown
            (119, 28, 101),# bold lilac
            (119, 28, 51),# deep milky rose
            (139, 69, 19),# brown desert
            (0, 0, 128),# very vivid blue
            (110,139, 61)# pale olive
            ]



class Planet(pg.sprite.Sprite):
    def __init__(self, name, image, rpm, resource, color, pos, radius, *groups):
        super(Planet, self).__init__(*groups)
        self.num_colonists = 10
        self.resource = resource
        self.inventory = {
                "Food": 1000,
                "Uranium": 1000,
                "Plastic": 1000,
                "Aluminum": 1000,
                "Titanium": 1000,
                "Gold": 1000
                }
        self.name = name
        self.radius = radius
        self.pos = tuple(pos)
        self.color = color
        w = self.radius * 2 
        self.redraw = False
        self.circum = int(2 * PI * self.radius)
        self.sheet = pg.transform.smoothscale(image, (self.circum, self.radius * 2))
        try:
            self.color = pg.Color(color)
        except ValueError:
            self.color = pg.Color(*color)
        self.sheet.fill(self.color, None, pg.BLEND_RGB_ADD)
        self.make_cover()
        self.rotation_speed = (rpm / 60.) * self.circum / 1000.
        self.subsurf = pg.Surface((self.radius*2, self.radius*2))
        self.subsurf.set_colorkey(pg.Color("purple"))
        self.source_pos = (self.radius, self.radius)
        self.int_pos = (self.radius, self.radius)
        self.image = pg.Surface((radius * 2, radius * 2)).convert()
        self.image.set_colorkey(pg.Color("purple"))
        self.rect = self.image.get_rect(center=self.pos)
        self.make_image()
        
    def make_cover(self):
        r = self.radius
        self.cover = pg.Surface((r*2, r*2)).convert()
        self.cover.fill(pg.Color("purple"))
        self.cover.set_colorkey(pg.Color("black"))
        pg.draw.circle(self.cover, pg.Color("black"), (r, r), r)

    def update(self, dt):
        redraw = False
        x = (self.source_pos[0] + (self.rotation_speed * dt)) % self.circum                
        self.source_pos = (x, self.source_pos[1])
        if int(self.source_pos[0]) - self.radius > self.circum:
            self.source_pos = self.source_pos[0] - self.circum, self.source_pos[1]
        if (int(self.source_pos[0]), int(self.source_pos[1])) != self.int_pos:
            self.int_pos = int(self.source_pos[0]), int(self.source_pos[1])
            redraw = True
        if redraw:
            self.make_image()

    def make_image(self):
        rect = pg.Rect((0,0), (self.radius * 2, self.radius * 2))
        rect.center = self.int_pos
        if rect.right > self.circum:
            left = pg.Rect(rect.left, rect.top, self.circum - rect.left, self.radius * 2)
            right = pg.Rect(0, rect.top, rect.right - self.circum, self.radius * 2)
            self.subsurf.blit(self.sheet.subsurface(left), (0, 0))
            self.subsurf.blit(self.sheet.subsurface(right), (left.width, 0))       
        elif rect.left < 0:
            right = pg.Rect(0, 0, self.circum + rect.left, self.radius * 2)
            left = pg.Rect(self.circum + rect.left, 0, self.circum - right.w, self.radius * 2)
            self.subsurf.blit(self.sheet.subsurface(left), (0, 0))
            self.subsurf.blit(self.sheet.subsurface(right), (left.width, 0))
        else:    
            self.subsurf.blit(self.sheet.subsurface(rect), (0, 0))
        self.subsurf.blit(self.cover, (0, 0))
        self.image.fill(pg.Color("purple"))
        self.image.blit(self.subsurf, (0, 0))
    
    def get_info(self):
        info = {}
        info["pos"] = self.pos
        info["inventory"] = {k:v for k, v in self.inventory.items()}
        info["resource"] = self.resource
        info["consumption"] = {k: RESOURCES[k] * self.num_colonists for k in RESOURCES}
        info["num_colonists"] = self.num_colonists
        return info
            
    def show_info(self, surface):
        w, h  = 200, 220
        surf = pg.Surface((w, h))
        surf.fill(pg.Color("gray10"))
        pg.draw.rect(surf, pg.Color("gray5"), surf.get_rect(), 2)
        title = Label(self.name, {"midtop": (w//2, 0)}, text_color="gray80", font_size=20)
        title.draw(surf)
        res_label = Label(self.resource, {"midtop": (w//2, 25)}, text_color="gray75")
        res_label.draw(surf)
        col_label = Label("{} Colonists".format(self.num_colonists),
                                {"midtop": (w//2, 40)}, text_color="gray75")
        col_label.draw(surf)
        top = 70
        titles = "Prod.", "Cons.", "On Hand"
        lefts = 50, 90, 130
        for title, left in zip(titles, lefts):
            label = Label(title, {"topleft": (left, top)}, text_color="gray75")
            label.draw(surf)
        top += 20    
        for i in self.inventory:
            img = prepare.GFX[i.lower()]
            surf.blit(img, (5, top))
            prod = self.num_colonists if i == self.resource else 0
            lab2 = Label("{}".format(prod), {"topleft": (lefts[0], top)}, text_color="gray80")
            consumption = RESOURCES[i] * self.num_colonists 
            lab3 = Label("{}".format(consumption), {"topleft": (lefts[1], top)}, text_color="gray80")
            lab4 = Label("{}".format(self.inventory[i]), {"topleft": (lefts[2], top)}, text_color="gray80")
            for l in (lab2, lab3, lab4):
                l.draw(surf)
            top += 20    
        cx, cy = prepare.SCREEN_RECT.center        
        if self.rect.right < cx:
            left = self.rect.right
        elif self.rect.left > cx:
            left = self.rect.left - w
        else:
            left = self.rect.centerx - (w//2)
        if self.rect.bottom < cy:
            top = self.rect.bottom
        elif self.rect.top > cy:
            top = self.rect.top - h
        else:
            top = self.rect.centery - (h//2)
        rect = surf.get_rect(topleft=(left, top))
        surface.blit(surf, rect)
        
    def can_produce(self):
        deduct = {}
        for good in self.inventory:
            if good != "Food":
                need = RESOURCES[good]
                total_use = need * self.num_colonists
                on_hand = self.inventory[good]
                if on_hand < total_use:
                    return
                else:
                    deduct[good] = total_use
        return deduct        
    
    def daily_update(self):
        hunger = RESOURCES["Food"]
        eaten = self.num_colonists * hunger
        food = self.inventory["Food"]
        if food >= eaten:
            self.inventory["Food"] -= eaten
        else:
            portions = int(food / float(hunger))
            dead = self.num_colonists - portions
            self.num_colonists = portions
            self.inventory["Food"]  = 0
        deduct = self.can_produce()  
        if deduct:
            for good in deduct:
                self.inventory[good] -= deduct[good]
            self.inventory[self.resource] += self.num_colonists
       
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
