import globs
import tiles.road as road
import pygame

class Router():

    def __init__(self):
        globs.router = self

    def do_init(self):
        pass

    def do_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tile = globs.map.pick(event.pos)
            self.build_road(tile)

    def build_road(self, tile):
        if not isinstance(tile, road.Road):
            aroad = road.Road()
            globs.map.replace_tile(tile, aroad)
