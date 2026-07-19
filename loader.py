import pygame

loaded_images = {}
def load_image(path):
    original = pygame.image.load(path).convert_alpha()
    scaled = pygame.transform.scale_by(original, 2)
    return scaled
