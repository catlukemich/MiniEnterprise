import globs
import pygame

class Picker():
    ''' A simple picker, might be overriden in future'''
    def __init__(self):
        globs.Globals.picker = self

    def do_init(self):
        pass

    def do_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            tile = globs.Globals.view.pick(event.pos)
            if tile != None:    
                pass
  