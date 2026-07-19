from .ImageWidget import *
from gui.drawers.PressedBackgroundDrawer import *
from gui.drawers.PressedBorderDrawer import *


class ImageButton(ImageWidget):

    def __init__(self, image):
        ImageWidget.__init__(self, image)
        self.released_background_drawer = self.get_background_drawer()
        self.released_border_drawer = self.get_border_drawer()
        self.pressed_background_drawer = PressedBackgroundDrawer()
        self.pressed_border_drawer = PressedBorderDrawer()

    def on_mouse_button_down(self, event):
        self.set_background_drawer(self.pressed_background_drawer)
        self.set_border_drawer(self.pressed_border_drawer)
        return True

    def on_mouse_button_up(self, event):
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)
        return True

    def on_mouse_out(self, event):
        ImageWidget.on_mouse_out(self, event)
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)
