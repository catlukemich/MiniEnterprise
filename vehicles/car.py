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

class Car(Sprite):
    def __init__(self, image_atlas, road):
        super().__init__()
        self.road = road # <-- The road tile this car is placed on or is now on.
        self.target_road = self.find_new_target_road() # <-- The road tile this car is going to.
        self.image_atlas = image_atlas # <-- The image atlas containing a car in 4 direction (s,e,w,n)
        self.direction = "s"  # <-- "s" or "w" or "e" - north, south or west or east
        self.image_index = 0  # <-- image index on the atlas (0-3 inclusive)

    def do_draw(self, blitfun=None):
        return super().do_draw(self.blitfun)
    

    def set_direction(self, direction):
        self.image_index = dir_to_index[direction]
        print(self.image_index)
        self.direction = direction


    def blitfun(self, x, y):
        w, h = self.image_atlas.get_size()
        col = self.image_index % 2
        row = self.image_index // 2
        atlas_x = col * w / 2
        atlas_y = row * h / 2
    
    
        globs.screen.blit(self.image_atlas, (x,y), (atlas_x, atlas_y, atlas_x + w/ 2, atlas_y + h / 2))        


    def update(self, delta_time):

        at_target_road = False
        if self.target_road != None:
            if self.location[0] > self.target_road.coords[0] - 0.2 and \
               self.location[1] > self.target_road.coords[1] - 0.2 and \
               self.location[0] < self.target_road.coords[0] + 0.2 and \
               self.location[1] < self.target_road.coords[1] + 0.2:
                at_target_road = True
                self.road = self.target_road
                self.target_road = self.find_new_target_road()

        
        if not at_target_road and self.target_road != None:
            x,y,z = self.location
            x2,y2 = self.target_road.coords
            dx = x2 - x
            dy = y2 - y

            car_delta_x = 0
            car_delta_y = 0
            epsilon = 0
            if dx < epsilon:
                car_delta_x = -1 * delta_time * 0.001
                self.set_direction("w")
            elif dx > epsilon:
                car_delta_x = 1 * delta_time * 0.001
                self.set_direction("e")
            elif dy < epsilon:
                car_delta_y = -1 * delta_time * 0.001
                self.set_direction("n")
            elif dy > epsilon:
                car_delta_y = 1 * delta_time * 0.001
                self.set_direction("s")

            self.location = (x + car_delta_x, y + car_delta_y, z)


    def find_new_target_road(self):
        target_road = None

        x, y = self.road.coords
        is_road_south = isinstance(globs.map.get_tile((x, y + 1)), Road)
        is_road_east  = isinstance(globs.map.get_tile((x + 1, y)), Road)
        is_road_west  = isinstance(globs.map.get_tile((x - 1, y)), Road)
        is_road_north = isinstance(globs.map.get_tile((x, y - 1)), Road)

        if is_road_south:
            target_road = globs.map.get_tile((round(x), round(y) + 1))
        elif is_road_east:
            target_road = globs.map.get_tile((round(x) + 1, round(y)))
        elif is_road_west:
            target_road = globs.map.get_tile((round(x) - 1, round(y)))
        elif is_road_north:
            target_road = globs.map.get_tile((round(x), round(y) - 1))
        return target_road