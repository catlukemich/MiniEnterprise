import pygame 
import random
import json

import loader
from tiles import tile

class Building(tile.Tile):

    def __init__(self, image, name, population):
        ''' A building has it's image, name and population. '''
        super().__init__()
        self.image : pygame.Surface = image 
        self.name = name
        self.population = population
        self.layer = 1

    def copy(self):
        return Building(self.image, self.name, self.population)



buildings = [] # Buildings prototypes arrays, initialized below vvv
 
# Inititialize prototypes buildings list (above ^^^)
def init_buildings_prototypes():
    if len(buildings) == 0:
        load_buildings_prototypes()

def load_buildings_prototypes():
    global buildings
    with open("assets/buildings.json") as buildings_file:
        buildings_datas = json.load(buildings_file)
        for data in buildings_datas:
            building_image =  loader.load_image("assets/" + data["path"]) # Path to image with the building (png)
            abuilding = Building(
                building_image, data["name"], data["population"]
            )
            buildings.append(abuilding)

# BUILDING (RANDOM) - make a random building from a prototype.
def make_random_building():
    init_buildings_prototypes()
    building = random.choice(buildings).copy()
    return building
