import globs

from random import randrange as random
import random
import opensimplex
import pygame

import constants
import tiles.mountain, tiles.grass, tiles.tree, tiles.tile
import city.city as city

class Map:
    def __init__(self):
        globs.map = self
        self.size = 50
        self.tiles = []
        self.cities = []

    def do_init(self):
        ''' Initialize and generate the map with randomness using simplex noise'''
        opensimplex.seed(1234)
        for y in range(0, self.size):
            row = []
            self.tiles.append(row)
            for x in range(0, self.size):
                iso_x, iso_y, iso_z = x, y, 0
                x_coord, y_coord = iso_x, iso_y
                s = int(opensimplex.noise2(iso_x / 5, iso_y / 5) * 3)
                
                if s == 0:
                    tile = tiles.grass.Grass()
                elif s == 1:
                    tile = tiles.tree.Tree()
                else:
                    tile = tiles.mountain.Mountain()
                row.append(tile)
                tile.location = (iso_x, iso_y, iso_z)
                tile.coords = (x_coord, y_coord)
                globs.view.add_sprite(tile)
            

        # Create cities:
        n_cities_generated = 0
        random.seed(1)
        for i in range(0,1000):
            x_coord = random.randint(0, self.size)
            y_coord = random.randint(0, self.size)
            do_continue = False
            for j in range(0,len(self.cities)):
                other_city = self.cities[j]
                delta_x_coord = other_city.x_coord - x_coord
                delta_y_coord = other_city.y_coord - y_coord
                if abs(delta_x_coord) < other_city.size or abs(delta_y_coord) < other_city.size:
                    do_continue = True
            if do_continue: continue
            else: n_cities_generated += 1

            acity = city.City()
            acity.place(x_coord, y_coord)
            acity.create()
            self.cities.append(acity)


    def get_tile(self, coords) -> tiles.tile.Tile:
        try:
            coord_x, coord_y = coords
            if coord_x < 0: return None
            if coord_y < 0: return None
            if coord_x >= self.size: return None
            if coord_y >= self.size: return None
            return self.tiles[coord_y][coord_x]
        except IndexError: return None

    def get_tiles(self):
        return self.tiles

    def set_tile_coords(self, coords, tile):
        ''' Set the tile replacing old tile with new tile using coordinates '''
        old_tile = self.get_tile(coords)
        self.set_tile(old_tile, tile)


    def set_tile(self, old_tile, new_tile):
        ''' Set the tile, replacing old_tile with new tile '''
        new_tile.location = old_tile.location
        new_tile.coords = old_tile.coords
        coords = old_tile.coords
        if coords[0] < self.size and coords[1] < self.size:
            if coords[0] >= 0 and coords[1] >= 0:
                self.tiles[coords[1]][coords[0]] = new_tile
        globs.view.replace_sprite(old_tile, new_tile)