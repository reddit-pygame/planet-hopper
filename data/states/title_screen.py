import pygame as pg

from .. import tools, prepare
from ..components.labels import Label


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = Label("Planet Hopper", {"midbottom": prepare.SCREEN_RECT.center})
        
    def startup(self, persistent):
        self.persist = persistent
        
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
            
    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))
        self.title.draw(surface)
        