import globs
from functools import cmp_to_key
import pygame
from . import sprite
import constants


class View():
    def __init__(self):
        globs.view = self
        self.sprites : list[sprite.Sprite] = []
        self.offset_x = 0
        self.offset_y = 0
        self.scrolling = False

    def do_init(self):
        pass

    def do_event(self, event : pygame.Event):
        ''' Handle event - for scrolling'''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.scrolling = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.scrolling = False
        if event.type == pygame.MOUSEMOTION and self.scrolling:
            self.offset_x += event.rel[0]
            self.offset_y += event.rel[1]
    

    def project(self, location):
        ''' Project from isometric coordinates to screen coordinates (3D -> 2D)'''
        iso_x, iso_y, iso_z = location
        x = iso_x * (constants.tile_width / 2) - iso_y * (constants.tile_width / 2) + self.offset_x
        y = iso_x * (constants.tile_height / 2) + iso_y * (constants.tile_height / 2) + self.offset_y
        return (x, y)

    def do_update(self, delta_time):
        for sprite in self.sprites:
            sprite.update(delta_time)

    def do_draw(self):
        ''' Draw the view, the sprites within'''
        def sort_sprites(a, b):
            if a.layer != b.layer:
                return a.layer - b.layer
            else:
                ax, ay, az = a.location
                bx, by, bz = b.location
            return ax + ay + az - bx - by - bz
        self.sprites.sort(key=cmp_to_key(sort_sprites))
        for sprite in self.sprites:
            sprite.do_draw()


    def pick(self, pos):
        ''' Pick a sprite basing on the position on the screen '''
        pos_x, pos_y = pos

        for i in range(len(self.sprites)- 1, -1, -1):
            sprite = self.sprites[i]
            if not sprite.image: continue
            x, y = self.project(sprite.location)
            w, h = sprite.image.get_size()
            x -= w / 2
            y -= h / 2
            delta_x = pos_x - x
            delta_y = pos_y - y
            try :
                pixel = sprite.image.get_at((delta_x, delta_y))
                if pixel[3] > 0:
                    return sprite
            except IndexError: pass

        return None


    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def get_sprites(self):
        return self.sprites
    
    def remove_sprite(self, sprite):
        if sprite in self.sprites: self.sprites.remove(sprite)

    def replace_sprite(self, old_sprite, new_sprite):
        self.remove_sprite(old_sprite)
        self.add_sprite(new_sprite)