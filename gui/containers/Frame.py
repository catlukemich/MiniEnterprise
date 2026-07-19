from .Container import *
from gui.drawers.BackgroundDrawer import *
from gui.drawers.BorderDrawer import *
from gui.layouts.AbsoluteLayout import *


class Frame(Container):
    def __init__(self):
        Container.__init__(self)

        self.layout = AbsoluteLayout()
        self.clipping_rectangle = Bounds()
        self.hover_rectangle = Bounds()

        self.set_background_drawer(BackgroundDrawer())
        self.set_border_drawer(BorderDrawer())

    def set_parent(self, parent):
        Container.set_parent(self, parent)
        self.recalculate_rectangles()
        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def set_dimensions(self, x, y=None):
        Container.set_dimensions(self, x, y)
        self.layout_widgets()
        self.recalculate_rectangles()
        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def set_position(self, x, y=None):
        Container.set_position(self, x, y)
        self.recalculate_rectangles()
        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def set_paddings(self, pad):
        Container.set_paddings(self, pad)
        self.recalculate_rectangles()
        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def set_margins(self, pad):
        Container.set_margins(self, pad)
        self.recalculate_rectangles()
        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def set_borders(self, pad):
        Container.set_borders(self, pad)
        self.recalculate_rectangles()
        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def recalculate_rectangles(self):
        clipping_rectangle = self.get_content_area()
        hover_rectangle = self.get_bordered_area()

        parent = self.get_parent()
        while parent != None:
            if isinstance(parent, Frame):
                parent_content_area = parent.get_content_area()
                clipping_rectangle = clipping_rectangle.intersection(parent_content_area)
                hover_rectangle = hover_rectangle.intersection(parent_content_area)

            parent = parent.get_parent()

        self.clipping_rectangle = clipping_rectangle
        self.hover_rectangle = hover_rectangle

        for widget in self.widgets:
            if isinstance(widget, Frame):
                widget.recalculate_rectangles()

    def get_clipping_rectangle(self):
        return self.clipping_rectangle

    def get_hover_rectangle(self):
        return self.hover_rectangle

    def set_layout(self, layout):
        self.layout = layout
        self.layout_widgets()

    def add_widget(self, widget):
        Container.add_widget(self, widget)
        self.layout.layout_widgets(self)
        self.resize_to_fit()
        parent = self.get_parent()
        if parent != None and isinstance(parent, Frame):
            parent.resize_to_fit()

    def remove_widget(self, widget):
        Container.remove_widget(self, widget)
        self.layout_widgets()

    def layout_widgets(self):
        self.layout.layout_widgets(self)

    def resize_to_fit(self):
        width = self.layout.get_width(self)
        height = self.layout.get_height(self)
        self.set_dimensions(width, height)
        parent = self.get_parent()
        if parent != None and isinstance(parent, Frame):
            parent.resize_to_fit()

    def draw(self, surface):
        abs_pos = self.calc_absolute_position()

        parent_clip = surface.get_clip()

        bg_drawer = self.get_background_drawer()
        if bg_drawer != None:
            bg_drawer.draw_background(self, surface)
        border_drawer = self.get_border_drawer()
        if border_drawer != None:
            border_drawer.draw_border(self, surface)

        # First draw the background and border:
        # Set the clipping rectangle so child controls wont draw outside the bounds:

        clipping_rectangle = self.clipping_rectangle
        clip_rect = pygame.Rect((
            clipping_rectangle.top_left.x, clipping_rectangle.top_left.y,
            clipping_rectangle.bottom_right.x - clipping_rectangle.top_left.x,
            clipping_rectangle.bottom_right.y - clipping_rectangle.top_left.y
        ))

        surface.set_clip(clip_rect)
        if self.clipping_rectangle.top_left.x == self.clipping_rectangle.bottom_right.x or self.clipping_rectangle.top_left.y == self.clipping_rectangle.bottom_right.y:
            pass
        else:
            Container.draw(self, surface)

        surface.set_clip(parent_clip)
