from gui.Widget import *
from gui.drawers.BackgroundDrawer import *
from gui.drawers.BorderDrawer import *


# A simple box widget
class Box(Widget):
    def __init__(self):
        Widget.__init__(self)

        self.set_background_drawer(BackgroundDrawer())
        self.set_border_drawer(BorderDrawer())

    def draw(self, surface):
        bg_drawer = self.get_background_drawer()
        if bg_drawer != None:
            bg_drawer.draw_background(self, surface)

        border_drawer = self.get_border_drawer()
        if border_drawer != None:
            border_drawer.draw_border(self, surface)
