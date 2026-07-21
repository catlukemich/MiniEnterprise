import pygame
import globs
import loader
from vehicles.car import Car
from tiles.road import Road

RESPAWN_TIME = 40000

class CarSpawner():

    def __init__(self):
        self.time = RESPAWN_TIME
        pass


    def update(self, delta_ms):
        self.time += delta_ms
        if self.time > RESPAWN_TIME:
            print("SPAWN!")
            self.time = self.time - RESPAWN_TIME
            road = self.search_for_road()
            x, y, z = road.location
            print(x,y,z)
            car_image  = loader.load_image("assets/vehicles/car1.png")
            car = Car(car_image, road)
            car.location = (x, y, z)
            car.layer = 3
            globs.view.add_sprite(car)

    def search_for_road(self) -> Road:
        tiles = globs.view.get_sprites() 
        for tile in tiles:
            if isinstance(tile, Road):
                return tile