import game
import globs
from interactors import router


class TestCar():

    def __init__(self):
        self.g = game.Game()

        globs.view.offset_x = 200
        globs.view.offset_y = 200

        tiles = [
            (0,0), (1,0), (2,0), (3,0), (4,0),
            (0,1),        (2,1),        (4,1),
            (0,2), (1,2), (2,2), (3,2), (4,2)
        ]

        for tile_coord in tiles:
            tile = globs.map.get_tile((tile_coord[0], tile_coord[1]))
            router.build_road(tile)
        
    def run(self):
        self.g.run()

if __name__ == "__main__":
    TestCar().run()