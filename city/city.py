import globs
import random
import pygame
import tiles.road as road
import interactors.router as router
import view.text as text
import tiles.building as building

sizes = {"small": 7, "medium": 13, "big": 19, "huge": 25}
#                            
#                            | |   
#                            |'|            _____
#           *        __*..* |  |     :      |.   |' .---"|
#            _*   .-'   '-. |  |     .--'|  ||   | _|    |
#         .-'|  _.|  |    ||   '-__  |   |  |    ||      |
#         |' | |.    |    ||       | |   |  |    ||      |
#      ___|  '-'     '    ""       '-'   '-.'    '`      |____
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class City():

    def __init__(self):
        self.name = get_random_city_name() # The name must be random
        self.x_coord = 0
        self.y_coord = 0
        self.sign = None

        sizes_list = [sizes["small"], sizes["medium"], sizes["big"]]

        self.size = random.choice(sizes_list)


    def create(self):
        self.make_sign()


    def make_sign(self):
        sign = text.Text(self.name)
        sign.layer = 1
        sign.location = (self.x_coord, self.y_coord, 0)
        globs.Globals.view.add_sprite(sign)


    def place(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.generate()

    def do_draw(self):
        x, y = globs.Globals.view.project((self.x_coord, self.y_coord, 0))
        globs.Globals.screen.blit(self.sign, (x, y))


    def generate(self):
        ''' Generate the city - it's roads and buildings '''
        nw_x_coord = self.x_coord - (self.size - 1) // 2
        nw_y_coord = self.y_coord - (self.size - 1) // 2

        y = 0
        for y_coord in range(nw_y_coord, nw_y_coord + self.size):
            x = 0
            for x_coord in range(nw_x_coord, nw_x_coord + self.size):
                if x % 3 == 0 or y % 3 == 0:
                    tile = globs.Globals.map.get_tile((x_coord, y_coord))
                    if tile:
                        # Make a road around the city or block
                        aroad = router.build_road(tile)
                        if aroad:
                            aroad.owner = self
                else:    
                    # Else make a buildings inside the block
                    tile = globs.Globals.map.get_tile((x_coord, y_coord))
                    if tile:
                        abuilding = building.make()
                        globs.Globals.map.set_tile(tile, abuilding)
                        abuilding.owner = self
                        


                x += 1
            y+= 1


######################
#     _______            
#    /\       \           
#   /()\   ()  \          
#  /    \_______\  random CITY NAME       
#  \    /()     /         
#   \()/   ()  /          
#    \/_____()/
#
#######################
def get_random_city_name():
    f = open("assets/cities.txt")
    names = f.readlines()
    name = random.choice(names)
    return name


# Test
if __name__ == "__main__":
    c = City()