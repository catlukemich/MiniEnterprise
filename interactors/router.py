import globs
import loader
import tiles.road as road

''' Functions responsible for building roads and other communication routes on the map ''' 

def build_road(tile) -> road.Road:
    if not isinstance(tile, road.Road):
        new_road = road.Road()
        globs.Globals.map.set_tile(tile, new_road)
        realign_roads(new_road, True)
        return new_road
    else:
        existing_road = tile
        return existing_road


def realign_roads(atile, surrounding = False):
    # alignement = [False, False, False, False] # n, s, e, w

    # Helper functions
    t = globs.Globals.map.get_tile
    ir = lambda tile: isinstance(tile, road.Road)
    
    if not ir(atile) and not surrounding: return

    # Coordinates of tile
    iso = atile.location
    coords = atile.coords
    
    x, y = coords

    tile_n, tile_s, tile_e, tile_w = t((x, y - 1)), t((x, y + 1)), t((x + 1, y)), t((x - 1, y))
    astring = ""
    astring += "n" if ir(tile_n) else ""
    astring += "s" if ir(tile_s) else ""
    astring += "e" if ir(tile_e) else ""
    astring += "w" if ir(tile_w) else ""

    aroad = road.Road()
    aroad.location = iso
    aroad.coords = coords
    path = f"assets/road-{astring}.png"
    aroad.image = loader.load_image(path)
        
    globs.Globals.map.set_tile_coords(coords, aroad)
    globs.Globals.view.replace_sprite(atile, aroad)

    if surrounding:
        realign_roads(tile_n)
        realign_roads(tile_s)
        realign_roads(tile_e)
        realign_roads(tile_w)


def on_network(messages : list[str]):
    for message in messages:
        if message.startswith("<ROAD>"):
            ### We got road built by the other player =====ROAD====== #<# #
            player = message.split(" ")[1]
            x_coord = int(message.split(" ")[2])
            y_coord = int(message.split(" ")[3])

            tile = globs.Globals.map.get_tile((x_coord, y_coord))
            if tile.owner == None:
                road = build_road(globs.Globals.map.get_tile((x_coord, y_coord)))
                road.owner = player

