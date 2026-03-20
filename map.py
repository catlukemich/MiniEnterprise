from random import randrange as random

import pygame

import constants
import globs
import tiles.grass
import tiles.tree

class Map:
    def __init__(self):
        globs.map = self
        self.tiles = []
        self.size = 40


    def do_init(self):
        x_coord = 0
        y_coord = 0
        for _ in range(self.size ** 2):
            arandom = random(0, 2)
            if arandom == 0:
                tile = tiles.grass.Grass()
            elif arandom == 1:
                tile = tiles.tree.Tree()
            else:
                tile = tiles.tree.Tree()
            tile.x_coord, tile.y_coord = x_coord, y_coord
            self.tiles.append(tile)
            
            x_coord = x_coord + 1
            if x_coord != 0 and x_coord % self.size == 0:
                x_coord = 0
                y_coord = y_coord + 1

            

    def do_draw(self):
        screen = pygame.display.get_surface()
        x = 512
        y = 0
        x += globs.view.offset_x
        y += globs.view.offset_y    
        for i in range(0, len(self.tiles)):
            tile = self.tiles[i]
            x = x + constants.tile_width / 2
            y = y + constants.tile_height / 2

            if i != 0 and i % self.size == 0:
                x = x - (constants.tile_width / 2) * self.size - constants.tile_width / 2 # tile width, map width, offset
                y = y - (constants.tile_height / 2) * self. size + constants.tile_height / 2
            screen.blit(tile.image, (x, y))

    def pick(self, pos):
        x = 512
        y = 0
        x += globs.view.offset_x
        y += globs.view.offset_y
        for i in range(0, len(self.tiles)):
            tile = self.tiles[i]
            x = x + constants.tile_width / 2
            y = y + constants.tile_height / 2
           
            if i != 0 and i % self.size == 0:
                x = x - (constants.tile_width / 2) * self.size - constants.tile_width / 2 # tile width, map width, offset
                y = y - (constants.tile_height / 2) * self. size + constants.tile_height / 2

            delta_x = int(pos[0] - x)
            delta_y = int(pos[1] - y)

            try :
                pixel = tile.image.get_at((delta_x, delta_y))
                if pixel[3] > 0:
                    return tile
            except IndexError: pass

        return None

    def get_tile():
        pass

    def replace_tile(self, old_tile, new_tile):
        if new_tile != None and old_tile != None:
            index = old_tile.y_coord * self.size + old_tile.x_coord
            self.tiles[index] = new_tile
        