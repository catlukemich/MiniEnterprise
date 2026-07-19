import globs

import pygame
import interactors.router as router
import tiles.tile as tile

class Player():

    def __init__(self):
        globs.Globals.player = self
        self.name = "Player 1"


    def do_init(self):
        pass


    def do_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ### Building roads: (a) pick from view (b) place a road using router module (c) assign a owner to the road.
            atile : tile.Tile = globs.Globals.view.pick(event.pos)
            if atile:
                if atile.owner == None:
                    ########################## Do networked messageing (TODO)
                    # message = "<ROAD> " + globs.Globals.player.name + " " + str(atile.coords[0]) + " " + str(atile.coords[1])
                    # globs.Globals.endpoint.send(message) 
                    aroad = router.build_road(atile)
                    aroad.owner = self
                    