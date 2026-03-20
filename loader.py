import pygame

loaded_images = {}
def load_image(path):
    original = pygame.image.load(path).convert_alpha()
    scaled = pygame.transform.scale2x(original)
    return scaled
