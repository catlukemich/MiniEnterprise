import random
import json

import loader
from . import tile

class Building(tile.Tile):

    def __init__(self, path, name, population):
        super().__init__()
        self.path = path # Path to image with the building (png)
        self.image = loader.load_image(path)
        self.name = name
        self.population = population

    def copy(self):
        return Building(self.path, self.name, self.population)



buildings = []

# BUILDING (? RANDOM ?) - choose a random building 
def make():
    init_buildings_prototypes()
    building = random.choice(buildings).copy()
    return building
 

def init_buildings_prototypes():
    if len(buildings) == 0:
        load_buildings_prototypes()

def load_buildings_prototypes():
    global buildings
    with open("assets/buildings.json") as buildings_file:
        buildings_datas = json.load(buildings_file)
        for data in buildings_datas:
            abuilding = Building(
                data["path"], data["name"], data["population"]
            )
            buildings.append(abuilding)


