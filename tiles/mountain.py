import pygame

import loader
import tiles.tile as tile


class Mountain(tile.Tile):
    def __init__(self):
        super().__init__()
        self.image = loader.load_image("assets/mountain.png")
