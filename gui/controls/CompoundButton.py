from .. import PressedBorderDrawer, PressedBackgroundDrawer, Color, BorderDrawer, BackgroundDrawer
from ..Widget import *
from ..utils.Orientation import Orientation
from ..utils.utils import *


# Compound button is a button that contains both image and text.
# Depending on the orientation the image is on the left of a text - in case
# the orientation is horizontall; or the image is above the text if the orientation
# is verticall.
class CompoundButton(Widget):

    def __init__(self, image, text, orientation=Orientation.HORIZONTAL):
        Widget.__init__(self)
        self.image = image
        self.font = load_font("gui/resources/arial.fnt", "gui/resources/arial.png")
        self.text = text
        self.color = Color(0, 0, 0)
        self.text_surface = self.draw_text_surface()
        self.orientation = orientation
        self.space = 4  # Space between the image and the text.
        self.update_dimensions()

        self.set_background_drawer(BackgroundDrawer())
        self.set_border_drawer(BorderDrawer())

        self.released_background_drawer = self.get_background_drawer()
        self.released_border_drawer = self.get_border_drawer()
        self.pressed_background_drawer = PressedBackgroundDrawer()
        self.pressed_border_drawer = PressedBorderDrawer()

    def draw(self, surface):
        content_area = self.get_content_area()
        x = content_area.top_left.x
        y = content_area.top_left.y
        width = content_area.bottom_right.x - x
        height = content_area.bottom_right.y - y

        image_dimensions = self.get_image_dimensions()
        image_width = image_dimensions[0]
        image_height = image_dimensions[1]
        text_dimensions = self.get_text_dimensions()
        text_width = text_dimensions[0]
        text_height = text_dimensions[1]

        bg_drawer = self.get_background_drawer()
        if bg_drawer != None:
            bg_drawer.draw_background(self, surface)

        border_drawer = self.get_border_drawer()
        if border_drawer != None:
            border_drawer.draw_border(self, surface)

        if self.orientation == Orientation.HORIZONTAL:
            image_x = x
            image_y = y + (height - image_height) / 2
            text_x = x + image_width + self.space
            text_y = y + (height - text_height) / 2
        elif self.orientation == Orientation.VERTICAL:
            image_x = x + (width - image_width) / 2
            image_y = y
            text_x = x + (width - text_width) / 2
            text_y = y + image_height + self.space

        surface.blit(self.image, (image_x, image_y))
        surface.blit(self.text_surface, (text_x, text_y))

    def set_orientation(self, orientation):
        self.orientation = orientation

    def draw_text_surface(self):
        width = self.calc_text_width()
        height = self.font.size

        text_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        current_width = 0
        for letter in self.text:
            id = ord(letter)
            glyph = self.font.get_glyph(id)
            top = 0
            area = pygame.Rect(glyph.x, glyph.y, glyph.width, glyph.height)
            text_surface.blit(self.font.atlas, (current_width + glyph.x_offset, top + glyph.y_offset), area)
            current_width += glyph.xadvance
        text_surface.fill((self.color.red, self.color.green, self.color.blue), None, pygame.BLEND_RGBA_MULT)

        return text_surface

    # Calculate the width of the text contents.
    def calc_text_width(self):
        width = 0
        for letter in self.text:
            id = ord(letter)
            glyph = self.font.get_glyph(id)
            width += int(glyph.xadvance)
        return width

    def update_dimensions(self):
        dimensions = self.calc_dimensions()
        self.set_dimensions(dimensions[0], dimensions[1])

    def calc_dimensions(self):
        image_dimensions = self.get_image_dimensions()
        image_width = image_dimensions[0]
        image_height = image_dimensions[1]
        text_dimensions = self.get_text_dimensions()
        text_width = text_dimensions[0]
        text_height = text_dimensions[1]

        if self.orientation == Orientation.HORIZONTAL:
            width = image_width + text_width + self.space
            height = max(image_height, text_height)
        elif self.orientation == Orientation.VERTICAL:
            width = max(image_width, text_width)
            height = image_height + text_height + self.space
        return (width, height)

    def get_image_dimensions(self):
        return self.image.get_size()

    def get_text_dimensions(self):
        return self.text_surface.get_size()

    def on_mouse_button_down(self, event):
        self.set_background_drawer(self.pressed_background_drawer)
        self.set_border_drawer(self.pressed_border_drawer)

    def on_mouse_button_up(self, event):
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)

    def on_mouse_out(self, event):
        self.set_background_drawer(self.released_background_drawer)
        self.set_border_drawer(self.released_border_drawer)
