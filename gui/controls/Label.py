from .Box import Box
from gui.utils.Color import Color
from gui.utils.utils import *


class Label(Box):
    # Defaults:
    FNT_PATH = "gui/resources/arial.fnt"
    ATLAS_PATH = "gui/resources/arial.png"

    def __init__(self, text=""):
        Box.__init__(self)
        self.font = load_font(Label.FNT_PATH, Label.ATLAS_PATH)
        self.text = text

        self.color = Color(0, 0, 0)

        self.text_surface = self.draw_text_surface()
        size = self.text_surface.get_size()
        self.set_dimensions(size[0], size[1])

        self.set_border_drawer(None)
        self.set_background_drawer(None)

    def set_text(self, text):
        self.text = text
        self.text_surface = self.draw_text_surface()
        size = self.text_surface.get_size()
        self.set_dimensions(size[0], size[1])

    def set_text_color(self, color):
        self.color = color
        self.text_surface = self.draw_text_surface()

    def get_text(self):
        return self.text

    def get_text_width(self, text):
        width = 0
        for letter in text:
            id = ord(letter)
            glyph = self.font.get_glyph(id)
            width += int(glyph.xadvance)
        return width

    def draw_text_surface(self):
        height = self.font.size
        width = self.get_text_width(self.text)

        text_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()

        current_width = 0
        for letter in self.text:
            id = ord(letter)
            glyph = self.font.get_glyph(id)
            top = 0

            area = pygame.Rect(glyph.x, glyph.y, glyph.width, glyph.height)
            text_surface.blit(self.font.atlas,
                              (current_width + glyph.x_offset, top + glyph.y_offset),
                              area
                              )

            current_width += glyph.xadvance

        text_surface.fill(
            (self.color.red, self.color.green, self.color.blue),
            None, pygame.BLEND_RGBA_MULT
        )

        return text_surface

    def draw(self, surface):
        Box.draw(self, surface)
        content_area = self.get_content_area()
        surface.blit(self.text_surface, (content_area.top_left.x, content_area.top_left.y))
