import pygame
from .utils.Bounds import *
from .utils.Pad import Pad
from .utils.Pad import EqualPad
from .utils.Alignment import Align


# Base class for all the controls.
# A widget occupies an area that consists of content, padding around the content
# borders, and margin 
# The position of a widget is where the top left corner of the whole area of the widget is. 
class Widget():
    def __init__(self):

        self.parent = None  # The parent widget of this widget

        self.background_drawer = None
        self.border_drawer = None

        self.position = Vector2D()  # Where the top right corner of the widget is relative to its parent
        self.dimensions = Vector2D(20, 20)  # The inner size of the widget
        self.paddings = Pad(0)  # The space around the content
        self.borders = EqualPad(1)  # Border around content with padding
        self.margins = Pad()  # The margin around the content with padding and borders

        self.align = Align.CENTER
        self.listeners = []
        self.data = None

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    # Calculate the absolute_position on the screen of a widget.
    def calc_absolute_position(self):
        absolute_position = Vector2D(self.position)
        parent = self.parent

        while parent != None:
            absolute_position += parent.get_position()

            borders = parent.get_borders()
            absolute_position.x += borders.left
            absolute_position.y += borders.top

            margins = parent.get_margins()
            absolute_position.x += margins.left
            absolute_position.y += margins.top

            paddings = parent.get_paddings()
            absolute_position.x += paddings.left
            absolute_position.y += paddings.top

            parent = parent.get_parent()

        return absolute_position

    def get_position(self):
        return self.position

    def set_position(self, x, y=None):
        if isinstance(x, Vector2D):
            self.position = x
        else:
            self.position.x = x
            self.position.y = y

    def set_dimensions(self, x, y=None):
        if isinstance(x, Vector2D):
            self.dimensions = x
        else:
            self.dimensions.x = x
            self.dimensions.y = y
        from gui.containers.Frame import Frame
        if self.parent != None and isinstance(self.parent, Frame):
            self.parent.layout_widgets()

    def get_dimensions(self):
        return self.dimensions

    def set_paddings(self, paddings):
        self.paddings = paddings
        from gui.containers.Frame import Frame
        if self.parent != None and isinstance(self.parent, Frame):
            self.parent.layout_widgets()

    def get_paddings(self):
        return self.paddings

    def set_borders(self, borders):
        self.borders = borders
        from gui.containers.Frame import Frame
        if self.parent != None and isinstance(self.parent, Frame):
            self.parent.layout_widgets()

    def get_borders(self):
        return self.borders

    def set_margins(self, margins):
        self.margins = margins
        from gui.containers.Frame import Frame
        if self.parent != None and isinstance(self.parent, Frame):
            self.parent.layout_widgets()

    def get_margins(self):
        return self.margins

    def set_width(self, width):
        dims = Vector2D(self.get_dimensions())
        dims.x = width
        self.set_dimensions(dims)

    def get_width(self):
        return self.dimensions.x

    def set_height(self, height):
        dims = Vector2D(self.get_dimensions())
        dims.y = height
        self.set_dimensions(dims)

    def get_height(self):
        return self.dimensions.y

    def set_align(self, align):
        self.align = align

    def get_align(self):
        return self.align

    def get_padded_width(self):
        return self.paddings.left + self.dimensions.x + self.paddings.right

    def get_bordered_width(self):
        padded_width = self.get_padded_width()
        bordered_width = self.borders.left + padded_width + self.borders.right
        return bordered_width

    def get_whole_width(self):
        bordered_width = self.get_bordered_width()
        whole_width = self.margins.left + bordered_width + self.margins.right
        return whole_width

    def get_padded_height(self):
        return self.paddings.top + self.dimensions.y + self.paddings.bottom

    def get_bordered_height(self):
        padded_height = self.get_padded_height()
        bordered_height = self.borders.top + padded_height + self.borders.bottom
        return bordered_height

    def get_whole_height(self):
        bordered_height = self.get_bordered_height()
        whole_height = self.margins.top + bordered_height + self.margins.bottom
        return whole_height

    def get_content_area(self):
        absolute_position = self.calc_absolute_position()
        width = self.dimensions.x
        height = self.dimensions.y

        top_left = Vector2D(
            absolute_position.x + self.margins.left + self.borders.left + self.paddings.left,
            absolute_position.y + self.margins.top + self.borders.top + self.paddings.top
        )

        bottom_right = top_left + Vector2D(width, height)
        return Bounds(top_left, bottom_right)

    def get_padded_area(self):
        absolute_position = self.calc_absolute_position()
        width = self.paddings.left + self.dimensions.x + self.paddings.right
        height = self.paddings.top + self.dimensions.y + self.paddings.bottom

        top_left = Vector2D(
            absolute_position.x + self.margins.left + self.borders.left,
            absolute_position.y + self.margins.top + self.borders.top
        )

        bottom_right = top_left + Vector2D(width, height)
        return Bounds(top_left, bottom_right)

    def get_bordered_area(self):
        absolute_position = self.calc_absolute_position()
        width = self.get_bordered_width()
        height = self.get_bordered_height()

        top_left = Vector2D(
            absolute_position.x + self.margins.left,
            absolute_position.y + self.margins.top
        )

        bottom_right = top_left + Vector2D(width, height)
        return Bounds(top_left, bottom_right)

    # Get the whole area of a widget. This includes the content dimensions, the padding
    # borders and margin. Returns new bounds
    def get_whole_area(self):
        absolute_position = self.calc_absolute_position()
        width = self.get_whole_width()
        height = self.get_whole_height()

        top_left = absolute_position
        bottom_right = Vector2D(absolute_position.x + width, absolute_position.y + height)
        return Bounds(top_left, bottom_right)

    def get_content_size(self):
        return self.dimensions

    def get_padded_size(self):
        width = self.paddings.left + self.dimensions.x + self.paddings.right
        height = self.paddings.top + self.dimensions.y + self.paddings.bottom
        return Vector2D(width, height)

    def get_bordered_size(self):
        padded_size = self.get_padded_size()
        width = self.borders.left + padded_size.x + self.borders.right
        height = self.borders.top + padded_size.y + self.borders.bottom
        return Vector2D(width, height)

    def get_whole_size(self):
        bordered_size = self.get_bordered_size()
        width = self.margins.left + bordered_size.x + self.margins.right
        height = self.margins.top + bordered_size.y + self.margins.bottom
        return Vector2D(width, height)

    def set_background_drawer(self, background_drawer):
        self.background_drawer = background_drawer

    def get_background_drawer(self):
        return self.background_drawer

    def set_border_drawer(self, border_drawer):
        self.border_drawer = border_drawer

    def get_border_drawer(self):
        return self.border_drawer

    def set_background_color(self, color):
        if self.background_drawer != None:
            self.background_drawer.set_color(color)

    def set_border_color(self, color):
        if self.border_drawer != None:
            self.border_drawer.set_color(color)

    def center(self):
        self.center_horizontally()
        self.center_vertically()

    def center_horizontally(self):
        if self.parent == None:
            w, h = pygame.display.get_surface().get_size()
        else:
            w = self.parent.dimensions.x
        x =  w / 2 - self.dimensions.x / 2
        y = self.position.y
        new_position = Vector2D(x, y)
        self.set_position(new_position)

    def center_vertically(self):
        if self.parent == None:
            w, h = pygame.display.get_surface().get_size()
        else:
            h = self.parent.dimensions.y
        x = self.position.x
        y = h / 2 - self.dimensions.y / 2
        new_position = Vector2D(x, y)
        self.set_position(new_position)

    def on_mouse_over(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_mouse_over(self, event)
            if consumed: break
        return consumed

    def on_mouse_move(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_mouse_move(self, event)
            if consumed: break
        return consumed

    def on_mouse_out(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_mouse_out(self, event)
            if consumed: break
        return consumed

    def on_key_down(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_key_down(self, event)
            if consumed: break
        return consumed

    def on_mouse_button_down(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_mouse_button_down(self, event)
            if consumed: break
        return consumed

    def on_mouse_button_up(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_mouse_button_up(self, event)
            if consumed: break
        return consumed

    def on_drag(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_drag(self, event)
            if consumed: break
        return consumed

    def on_click(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_click(self, event)
            if consumed: break
        return consumed

    def on_focus_gain(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_focus_gain(self, event)
            if consumed: break
        return consumed

    def on_focus_lost(self, event):
        consumed = False
        for listener in self.listeners:
            consumed = listener.on_focus_lost(self, event)
            if consumed: break
        return consumed

    def on_window_resize(self, event):
        pass

    # Draw the widget
    def draw(self, surface):
        pass

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)
