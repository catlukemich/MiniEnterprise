from gui.drawers.BackgroundDrawer import *
from gui.drawers.BorderDrawer import *
from gui.drawers.PressedBackgroundDrawer import PressedBackgroundDrawer
from gui.drawers.PressedBorderDrawer import PressedBorderDrawer
from .Label import Label


class TextButton(Label):
    def __init__(self, text=""):
        Label.__init__(self, text)

        self.released_background_drawer = BackgroundDrawer()
        self.released_border_drawer = BorderDrawer()
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)

        self.pressed_background_drawer = PressedBackgroundDrawer()
        self.pressed_border_drawer = PressedBorderDrawer()

    def on_mouse_button_down(self, event):
        Label.on_mouse_button_down(self, event)
        self.set_background_drawer(self.pressed_background_drawer)
        self.set_border_drawer(self.pressed_border_drawer)
        return True

    def on_mouse_button_up(self, event):
        Label.on_mouse_button_up(self, event)
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)
        return True

    def on_mouse_out(self, event):
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)

    def set_pressed_background_drawer(self, bg_drawer):
        self.pressed_background_drawer = bg_drawer

    def set_pressed_border_drawer(self, border_drawer):
        self.pressed_border_drawer = border_drawer
