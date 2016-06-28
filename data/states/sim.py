import pygame as pg

from .. import tools, prepare
from ..components.world import World, Planet, Ship
from ..components.labels import Label


class UI(object):
    def __init__(self, world):
        self.world = world 
        self.make_dynamic_labels()
        
    def make_dynamic_labels(self):
        self.dynamic_labels = pg.sprite.Group()
        pop = sum((p.num_colonists for p in self.world.planets.values()))
        pop += self.world.ship.num_colonists
        names = ("Aluminum", "Gold", "Plastic", "Titanium", "Uranium")
        top = 0
        edge = prepare.SCREEN_RECT.right 
        left = edge - 110
        for n in names:
            amt = int(sum((x.inventory[n] for x in self.world.planet_group)))
            Label(n, {"topleft": (left, top)}, self.dynamic_labels)
            Label("{}".format(amt), {"topright": (edge, top)}, self.dynamic_labels)
            top += 20
        Label("Day {}".format(self.world.day), {"topleft": (0, 0)}, self.dynamic_labels)
        Label("Pop {}".format(pop), {"topleft": (0, 20)}, self.dynamic_labels)
        
    def update(self):
        self.make_dynamic_labels()
        
    def draw(self, surface):
        self.dynamic_labels.draw(surface)


class SpaceSim(tools._State):
    def __init__(self):
        super(SpaceSim, self).__init__()
        self.world = World()
        self.sim_timer = 0
        self.running_sim = True
        self.hovered = None
        self.ui = UI(self.world)
        self.tick_lengths = [1000, 500, 100, 50, 20, 10, 5, 1]
        self.tick_index = 0
        self.tick_length = self.tick_lengths[self.tick_index]
        
    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_SPACE:
                self.running_sim = not self.running_sim
            elif event.key == pg.K_UP:
                if self.tick_index < len(self.tick_lengths) - 1:
                    self.tick_index += 1
                    self.tick_length = self.tick_lengths[self.tick_index]
            elif event.key == pg.K_DOWN:
                if self.tick_index > 0:
                    self.tick_index -= 1
                    self.tick_length = self.tick_lengths[self.tick_index]
                
    def update(self, dt):
        if self.running_sim:
            self.sim_timer += dt
            
            while self.sim_timer >= self.tick_length:
                self.world.daily_update()
                self.world.ship.update()
                self.sim_timer -= self.tick_length
                    
        self.hovered = None
        mouse_pos = pg.mouse.get_pos()
        adj_dt = int(dt * (1000 / self.tick_length))
        for p in self.world.planets.values():
            p.update(adj_dt)
            if p.rect.collidepoint(mouse_pos):
                self.hovered = p
                break
        if self.world.ship.rect.collidepoint(mouse_pos):
            self.hovered = self.world.ship
        self.ui.update()
        
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.world.planet_group.draw(surface)
        self.world.ship.draw(surface)
        if self.hovered:
            self.hovered.show_info(surface)
        self.ui.draw(surface)