# Global variables for the game
class Globals:


    ### Imports here with m-prefix indicate that the import is a module and
    ### is present here to avoid naming collisions.

    #------- In-game part -------#
    import pygame
    screen : pygame.Surface = None  # <-- The main screen where everything id drawn into.
    
    import game as mgame
    game : mgame.Game = None # <-- Reference to the global game instance.

    import ui.gui as mgui
    gui : mgui.GUI = None

    import view.view as mview
    view : mview.View = None # <-- View - the isometric projection takes place here.

    import map as mmap
    map : mmap.Map = None # <-- The map, where all the tiles reside.

    import interactors.picker as mpicker
    picker : mpicker.Picker = None # <-- Picker (unused).

    import player.player as mplayer 
    player : mplayer.Player = None # <-- Player instance indicating player's name and other characteristics.
    
    #------ Networked part -------#
    import inet.server as mserver 
    server : mserver.Server = None

    import inet.client as mclient
    client : mclient.Client = None

    import inet.endpoint as mnetwork_agent
    endpoint : mnetwork_agent.Endpoint = None

