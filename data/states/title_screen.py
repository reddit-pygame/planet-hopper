import pygame as pg
import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.world_generator import generate_worlds


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = Label("Planet Hopper", {"midbottom": prepare.SCREEN_RECT.center})
        self.worlds = self.load_worlds()
        self.make_world_buttons()
        
    def startup(self, persistent):
        self.persist = persistent
        
    def load_worlds(self):
        if not os.path.exists("worlds.json"):
            generate_worlds()
        with open("worlds.json", "r") as f:
            worlds = json.load(f)
        return worlds

    def load_world(self, num):
        self.persist["world"] = self.worlds[num]
        self.done = True
        
    def make_world_buttons(self):
        self.buttons = ButtonGroup()
        top = 50
        left = 100
        for w in self.worlds:
            text = "World {}".format(w)
            
            Button((left, top), self.buttons, text=text, fill_color=pg.Color("gray20"), call=self.load_world, args=w)
            top += 50
            
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            else:
                self.done = True
                self.next = "SIM"                
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next = "SIM"
        self.buttons.get_event(event)
        
    def update(self, dt):
        self.buttons.update(pg.mouse.get_pos())

    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))
        self.title.draw(surface)
        self.buttons.draw(surface)