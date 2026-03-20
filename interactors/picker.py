import globs
import pygame

class Picker():
    def __init__(self):
        globs.picker = self

    def do_init(self):
        pass

    def do_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            tile = globs.map.pick(event.pos)
            if tile != None:
                print(tile.x_coord, tile.y_coord)

  