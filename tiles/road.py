from tiles import tile
import loader


class Road(tile.Tile):

    def __init__(self):
        super().__init__()
        self.image = loader.load_image("assets/road-ew.png")
       