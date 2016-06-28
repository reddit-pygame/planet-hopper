import pygame as pg

from .. import tools, prepare

class Gameplay(tools._State):
    def __init__(self):
        super(Gameplay, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))
        
        