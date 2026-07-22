import random

import pygame
import globs
import loader
from vehicles.car import Car
from tiles.road import Road

RESPAWN_TIME = 10000000

possible_cars = [
    "assets/vehicles/car1.png",
    "assets/vehicles/car2.png",
    "assets/vehicles/car3.png",
    "assets/vehicles/car4.png",
    "assets/vehicles/car5.png",
    "assets/vehicles/car6.png",
    "assets/vehicles/car7.png",
]

class CarSpawner():

    def __init__(self):
        self.time = RESPAWN_TIME # <-- So a car spawns immadiatelly at game start.
        pass


    def update(self, delta_ms):
        self.time += delta_ms
        if self.time > RESPAWN_TIME: # <-- At this point the car get's spawned.
            self.time = self.time - RESPAWN_TIME 
            road = self.search_for_road()
            car_image  = loader.load_image(random.choice(possible_cars))
            car = Car(car_image, road)
            
            globs.view.add_sprite(car)

    def search_for_road(self) -> Road:
        tiles = globs.view.get_sprites() 
        for tile in tiles:
            if isinstance(tile, Road):
                return tile