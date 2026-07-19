import pygame
import loader
import tiles.tile as tile


#################
#     ____      #
#    / o  \     #
#    |  o |     #
#    \____/     #
#      ||       #
#      ||       #
# _____/\ ______#
#################

class Tree(tile.Tile):
    def __init__(self):
        super().__init__()
        self.image = loader.load_image("assets/tree.png")

