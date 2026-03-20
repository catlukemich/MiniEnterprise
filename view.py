import globs
import pygame


class View():
    def __init__(self):
        globs.view = self
        self.offset_x = 0
        self.offset_y = 0
        self.scrolling = False

    def do_init(self):
        pass

    def do_event(self, event : pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.scrolling = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.scrolling = False
        if event.type == pygame.MOUSEMOTION and self.scrolling:
            self.offset_x += event.rel[0]
            self.offset_y += event.rel[1]
    

