import random
import globs
import pygame
import main
import map
import inet.server as server
import inet.client as client
import inet.null_endpoint as null_endpoint
import interactors.picker as picker 
import interactors.highlighter as highlighter 
import interactors.router as router
import player.player as player
import view.view as view 
import vehicles.car_spawner as car_spawner
import ui.ui as ui

''' Subclass of the main class '''
class Game(main.Main):
    def __init__(self):
        globs.game = self
        super().__init__()

        random.seed(1)

        the_view = view.View()
        the_map = map.Map() # Map

        
        # Interactors - elements that interact with the world
        the_picker = picker.Picker() # Picker
        the_highlighter = highlighter.Highlighter() # Highlighter
        the_player = player.Player()
        ################## Instancing client and server (TODO)
        # the_server = server.Server()
        # the_client = client.Client()

        # Initialization 
        the_map.do_init()
        the_picker.do_init()
        the_highlighter.do_init()
        the_view.do_init()
        the_player.do_init()
        
        # Spawners
        self.the_car_spawner = car_spawner.CarSpawner()

        # UI initialization:
        the_ui = ui.UI()
        the_ui.show()



        ################# Network initialization (TODO):
        # server_running = False
        # client_running = False
        # try:
        #     server_running = the_server.do_init(0.2) # <-- If the server waits for 2 secs(debugging purposes) go to single player mode.
        #     if not server_running:
        #         client_running = the_client.do_init()
        # except TimeoutError:
        #     pass # <-- Will be single player mode vvvvv.
        
        # if server_running:
        #     globs.endpoint = the_server
        #     the_player.name = "Player1"
        # if client_running:
        #     globs.endpoint = the_client
        #     the_player.name = "Player2"

        # if not server_running and not client_running:
        #     globs.endpoint = null_endpoint.NullEndpoint()


    def do_updates(self, delta_time):
        globs.view.do_update(delta_time)
        self.the_car_spawner.update(delta_time)


    def do_event(self, event):
        ''' Pass events to the interactors'''
        globs.picker.do_event(event)
        globs.highlighter.do_event(event)
        globs.view.do_event(event)
        globs.player.do_event(event)
        
        self.handle_network()


    def handle_network(self):
        if globs.endpoint is not None:
            messages = globs.endpoint.recv()
            router.on_network(messages)


    def do_drawing(self):
        globs.view.do_draw()


if __name__ == "__main__":
    Game().run()
