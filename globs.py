# Global variables for the game



### Imports here with m-prefix indicate that the import is a module and
### is present here to avoid naming collisions.

#------- In-game part -------#
game = None # <-- Reference to the global game instance.

screen = None  # <-- The main screen where everything id drawn into.

gui = None

view = None # <-- View - the isometric projection takes place here.

map = None # <-- The map, where all the tiles reside.

picker = None # <-- Picker (unused).

player = None # <-- Player instance indicating player's name and other characteristics.

#------ Networked part -------#
server = None

client = None

endpoint = None

