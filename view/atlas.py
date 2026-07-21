import pygame

class Atlas:

    def __init__(self, atlas_image, num_images, image_width, image_height):
        ''' Create an atlas provided the atlas image, image width and image height in the atlas. '''
        self.atlas_image = atlas_image # <-- The image of the atlas itself.
        self.num_images  = num_images  # <-- Number of images in the atlas.
        self.image_width  = image_width  # <-- The width of a single image in the atlas.
        self.image_height = image_height # <-- The height of a single image in the atlas.


    def blit(self, surface, image_index, x, y):
        ''' Blit the part of atlas by a given image index in the atlas onto a surface. '''
        column = image_index % self.num_images
        row = image_index // 2
        area = pygame.Rect(
            left= column * self.image_width, top = row * self.image_height, 
            width = self.image_width, height = self.image_height
        )
