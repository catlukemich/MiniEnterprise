import globs
import pygame
import main
import map
import interactors.picker as picker 
import interactors.highlighter as highlighter 
import interactors.router as router
import view 

''' Subclass of the main class '''
class Game(main.Main):
    def __init__(self):
        globs.game = self
        super().__init__()


    def do_init(self):

        the_map = map.Map() # Map
        the_picker = picker.Picker() # Picker
        the_highlighter = highlighter.Highlighter() # Highlighter
        the_view = view.View()
        the_router = router.Router()

        the_map.do_init()
        the_picker.do_init()
        the_highlighter.do_init()
        the_view.do_init()
        the_router.do_init()


    def do_event(self, event):
        globs.picker.do_event(event)
        globs.highlighter.do_event(event)
        globs.view.do_event(event)
        globs.router.do_event(event)



    def do_drawing(self):
        globs.map.do_draw()


if __name__ == "__main__":
    Game()
