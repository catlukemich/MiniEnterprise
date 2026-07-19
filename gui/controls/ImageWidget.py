from .Box import *
import pygame


class ImageWidget(Box):

    def __init__(self, image):
        Box.__init__(self)
        self.dimensions.x = image.get_size()[0]
        self.dimensions.y = image.get_size()[1]
        self.image = image

    def set_image(self, image):
        self.image = image

    def draw(self, surface):
        Box.draw(self, surface)
        content_area = self.get_content_area()
        surface.blit(self.image, (content_area.top_left.x, content_area.top_left.y))

    def set_dimensions(self, x, y=None):
        Box.set_dimensions(self, x, y)
        dimensions = self.dimensions
        self.image = pygame.transform.scale(self.image, (dimensions.x, dimensions.y))
