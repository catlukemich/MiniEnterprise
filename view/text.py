import globs
import pygame
import view.sprite as sprite


class Text(sprite.Sprite):

    def __init__(self, content):
        super().__init__()
        self.content = content
        self.surface = None
        self.set_content(content)

    def set_content(self, content):
        self.content = content
        font = pygame.font.Font("assets/pixelated.ttf", 5)
        atext = font.render(self.content, color=(255,255,255), antialias=False)
        self.surface = pygame.transform.scale_by(atext, 2)


    def do_draw(self, blitfun=None):
        x, y = globs.Globals.view.project(self.location)
        globs.Globals.screen.blit(self.surface, (x, y))