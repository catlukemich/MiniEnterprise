import globs
import pygame
import interactors.picker as picker

class Highlighter():
    ''' Highlighter used to highlight tiles, where the cursor is currently '''

    def __init__(self):
        globs.highlighter = self

        self.previous_tile = None # Previous tile reference when restoring
        self.original_image = None # Original image of previous tile for restoration
        self.current_tile = None # Current tile for reference and usage elsewhere


    def do_init(self): 
        pass


    def do_event(self, event):
        ''' Highlight the new tile an un-highlight the previous '''
        if event.type == pygame.MOUSEMOTION:
            if self.previous_tile != None:
                self.previous_tile.image = self.original_image    
            self.current_tile = globs.view.pick(event.pos) # <-- The new tile to be highlighted.
            if self.current_tile != None:
                self.original_image = self.current_tile.image
                colored_image = self.current_tile.image.copy()
                colored_image.fill((255,0,0), None, pygame.BLEND_ADD)
                self.current_tile.image = colored_image
                self.previous_tile = self.current_tile



