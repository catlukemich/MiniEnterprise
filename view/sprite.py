import pygame

import globs


class Sprite():
    ''' Normal isometric Sprite - a static image with no animation. '''

    def __init__(self, location = (0,0,0), image = None):
        self.image = image # Image of the sprite
        self.location = location # The location of the sprite in isometric coordinates
        self.blit_function = None # A function that takes image, x and y coordinate - used for custom blitting
        self.layer = 0 # The higher layer the more on-top the sprite will be drawn
        pass


    def update(self, clock):
        pass

    def do_draw(self, blitfun = None):
        ''' Draw the sprite onto the screen '''
        x, y = globs.Globals.view.project(self.location)
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2
        if self.image != None:
            if blitfun: blitfun(x, y)
            else: globs.Globals.screen.blit(self.image, (x, y))


    def update(self, delta_time):
        pass


class AnimatedSprite(Sprite):
    ''' Animated sprite - pass array of images to constructor that comprise of animation frames. '''

    def __init__(self, location=(0, 0, 0), frames = []):
        super().__init__(location, frames[0])
        self.frames = frames
        self.play_time = 0
    
    def do_draw(self, blitfun=None):
        return super().do_draw(blitfun)
    
    def update(self, clock: pygame.time.Clock, blitfun = None):
        self.play_time += clock.get_time()
        frame_idx = self.play_time // (len(self.frames) * 250)
        self.image = self.frames[frame_idx]
        self.do_draw(blitfun)
