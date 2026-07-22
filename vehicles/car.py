import random

from tiles.road import Road
from view.sprite import Sprite
import globs
import math


#    o_______________}o{
#    |              |   \
#    |    911       |____\_____
#    | _____        |    |_o__ |
#    [/ ___ \       |   / ___ \|
#   []_/.-.\_\______|__/_/.-.\_[]
#      |(O)|             |(O)|
#       '-'   ScS         '-'
# ---   ---   ---   ---   ---   ---


INDEX_S = 0
INDEX_E = 1
INDEX_W = 2
INDEX_N = 3

dir_to_index = {
    "s": 0, "e": 1, "w": 2, "n": 3
}


offsets = [
    (-10, -10),     # When going SOUTH
    (0 , 0),        # When going EAST
    (5, -5),        # When going WEST
    (-3, -3)         # When going NORTH
]


class Car(Sprite):
    def __init__(self, image_atlas, road):
        super().__init__()
        self.direction = "s"  # <-- "s" or "w" or "e" - north, south or west or east
        self.road = road # <-- The road tile this car is placed on or is now on.
        self.location = (self.road.coords[0], self.road.coords[1], 0)
        self.find_new_target_road() # <-- The road tile this car is going to.
        self.image_atlas = image_atlas # <-- The image atlas containing a car in 4 direction (s,e,w,n)
        self.image_index = 0  # <-- image index on the atlas (0-3 inclusive)
        self.direction_offset = offsets[0] # <-- Offset from the original position for the car to drive right (or left) side of the road.
        self.layer = 1

    def do_draw(self, blitfun=None):
        return super().do_draw(self.blitfun)
    

    def set_direction(self, direction):
        self.image_index = dir_to_index[direction]
        self.direction = direction
        self.direction_offset = offsets[dir_to_index[direction]]


    def blitfun(self, x, y):
        w, h = self.image_atlas.get_size()
        col = self.image_index % 2
        row = self.image_index // 2
        atlas_x = col * w / 2
        atlas_y = row * h / 2
        globs.screen.blit(self.image_atlas, (x + self.direction_offset[0],y + self.direction_offset[1]), (atlas_x, atlas_y, atlas_x + w/ 2, atlas_y + h / 2))        


    def update(self, delta_time):

        if self.location[0] > self.target_road.coords[0] - 0.01 and \
           self.location[1] > self.target_road.coords[1] - 0.01 and \
           self.location[0] < self.target_road.coords[0] + 0.01 and \
           self.location[1] < self.target_road.coords[1] + 0.01:
            
            self.road = self.target_road
            self.location = (self.road.coords[0], self.road.coords[1], 0)
            self.find_new_target_road()
                
        if self.target_road != None:
            x,y = self.road.coords
            x2,y2 = self.target_road.coords
            dx = x2 - x
            dy = y2 - y

            car_delta_x = 0
            car_delta_y = 0
            epsilon = 0
            if dx < epsilon:
                car_delta_x = -1 * delta_time * 0.001
            elif dx > epsilon:
                car_delta_x = 1 * delta_time * 0.001
            elif dy < epsilon:
                car_delta_y = -1 * delta_time * 0.001
            elif dy > epsilon:
                car_delta_y = 1 * delta_time * 0.001

            loc_x, loc_y, loc_z = self.location
            self.location = (loc_x + car_delta_x, loc_y + car_delta_y, loc_z)

      


    def find_new_target_road(self):
        target_road = None

        x, y, z = self.location
        is_road_south = isinstance(globs.map.get_tile((round(x), round(y) + 1)), Road)
        is_road_east  = isinstance(globs.map.get_tile((round(x) + 1, round(y))), Road)
        is_road_west  = isinstance(globs.map.get_tile((round(x) - 1, round(y))), Road)
        is_road_north = isinstance(globs.map.get_tile((round(x), round(y) - 1)), Road)

        possible_roads = []

        if self.direction == "s":
            if is_road_south:
                possible_roads.append(globs.map.get_tile((round(x), round(y) + 1)))
            if is_road_east:
                possible_roads.append(globs.map.get_tile((round(x) + 1, round(y))))
            if is_road_west:
                possible_roads.append(globs.map.get_tile((round(x) - 1, round(y))))

        if self.direction == "e":
            if is_road_east:
                possible_roads.append(globs.map.get_tile((round(x) + 1, round(y))))
                print("road east")
            if is_road_south:
                possible_roads.append(globs.map.get_tile((round(x), round(y) + 1)))
            if is_road_north:
                possible_roads.append(globs.map.get_tile((round(x), round(y) - 1)))
                
        if self.direction == "w":
            if is_road_west:
                possible_roads.append(globs.map.get_tile((round(x) - 1, round(y))))
            if is_road_south:
                possible_roads.append(globs.map.get_tile((round(x), round(y) + 1)))
            if is_road_north:
                possible_roads.append(globs.map.get_tile((round(x), round(y) - 1)))

        if self.direction == "n":
            if is_road_north:
                possible_roads.append(globs.map.get_tile((round(x), round(y) - 1)))    
            if is_road_east:
                possible_roads.append(globs.map.get_tile((round(x) + 1, round(y))))
            if is_road_west:
                possible_roads.append(globs.map.get_tile((round(x) - 1, round(y))))

        
        if len(possible_roads) == 0:
            if self.direction == "s": # <-- If the car can't go SOUTH further and no other roads - reverse
                self.set_direction("n")
                self.target_road = globs.map.get_tile((round(x), round(y) - 1))
            elif self.direction == "e": # <-- If the car can't go EAST further and no other roads - reverse
                self.set_direction("w")
                self.target_road = globs.map.get_tile((round(x) - 1, round(y)))
            elif self.direction == "w": # <-- If the car can't go WEST further and no other roads - reverse
                self.set_direction("e")
                self.target_road = globs.map.get_tile((round(x) + 1, round(y)))
            elif self.direction == "n": # <-- If the car can't go NORTH further and no other roads - reverse
                self.set_direction("s")
                self.target_road = globs.map.get_tile((round(x), round(y) + 1))
            print("reversing")
        else:
            self.target_road = random.choice(possible_roads)
            
            # if self.target_road != None:
            x,y,z = self.location
            x2,y2 = self.target_road.coords
            dx = x2 - x
            dy = y2 - y
            zero = 0
            if dx < zero:
                self.set_direction("w")
            elif dx > zero:
                self.set_direction("e")
            elif dy < zero:
                self.set_direction("n")
            elif dy > zero:
                self.set_direction("s")
