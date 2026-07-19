import tiles.tile as tile


class Industry(tile.Tile):

    def __init__(self):
        super().__init__()
        self.cargo_type = None
        self.cargo_amount = 0

    def update(self, delta_time):
        return super().update(delta_time)

    