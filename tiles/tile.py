import view.sprite as sprite


class Tile(sprite.Sprite):
    ''' Abstract class for tiles in the world. '''
    def __init__(self):
        super().__init__()
        self.coords = (0, 0)

        # TILE OWNER, possible choices:
        # - player
        # - city
        # - nobody (None)
        self.owner = None 
