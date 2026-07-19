from .Box import Box
from ..utils.Alignment import *
from ..utils.Color import Color
from ..utils.utils import *


class Line():
    def __init__(self, width, text):
        self.width = width
        self.text = text

    def __str__(self):
        return "Line: width: %d, contents: %s" % (self.width, self.text)


class Text(Box):
    # Defaults:
    FNT_PATH = "gui/resources/arial.fnt"
    ATLAS_PATH = "gui/resources/arial.png"

    def __init__(self, text="", line_width=9999999):
        Box.__init__(self)

        self.line_width = line_width

        self.font = load_font(Text.FNT_PATH, Text.ATLAS_PATH)
        self.text = text

        self.color = Color(0, 0, 0)

        # self.setBackgroundDrawer(None)
        # self.setBorderDrawer(None)

        self.text_align = Align.CENTER

        self.text_surface = self.draw_text_surface()

        size = self.text_surface.get_size()
        self.set_dimensions(size[0], size[1])

    def set_max_width(self, width):
        self.text_surface = self.draw_text_surface()
        size = self.text_surface.get_size()
        self.set_dimensions(size[0], size[1])

    def get_text_width(self, text):
        width = 0
        for letter in text:
            id = ord(letter)
            glyph = self.font.get_glyph(id)
            width += glyph.xadvance
        return width

    def set_text(self, text):
        self.text = text
        self.text_surface = self.draw_text_surface()
        size = self.text_surface.get_size()
        self.set_dimensions(size[0], size[1])

    def set_text_color(self, color):
        self.color = color
        self.text_surface = self.draw_text_surface()

    def set_text_align(self, align):
        self.text_align = align

    def draw_text_surface(self):
        lines = []
        words = self.text.split()

        current_x = 0
        current_y = 0

        current_text = ""

        for word_idx in range(0, len(words)):
            current_word = words[word_idx]
            current_word_width = self.get_text_width(current_word + " ")
            current_text += current_word + " "
            next_word = None
            next_word_width = 0
            current_x += current_word_width
            try:
                next_word = words[word_idx + 1]
                next_word_width = self.get_text_width(next_word)
            except:
                pass
            if current_x + next_word_width > self.line_width:
                lines.append(Line(current_x, current_text))
                current_x = 0
                current_text = ""
            current_y += self.font.size

        lines.append(Line(current_x, current_text))

        surf_width = 0
        surf_height = 0
        for line in lines:
            if line.width > surf_width: surf_width = line.width
            surf_height += self.font.size

        text_surface = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA, 32).convert_alpha()

        current_y = 0
        for line in lines:
            current_x = 0

            offset_vector = Aligner.get_alignment_offset(surf_width, 0, line.width, 0, self.text_align)
            for letter in line.text:
                id = ord(letter)
                glyph = self.font.get_glyph(id)

                text_surface.blit(self.font.atlas,
                                  (current_x + glyph.x_offset + offset_vector.x, current_y + glyph.y_offset),
                                  pygame.Rect(glyph.x, glyph.y, glyph.width, glyph.height)
                                  )
                current_x += glyph.xadvance

            current_x = 0
            current_y += self.font.size

        text_surface.fill(
            (self.color.red, self.color.green, self.color.blue),
            None, pygame.BLEND_RGBA_MULT
        )

        return text_surface

    def draw(self, surface):
        Box.draw(self, surface)

        dimensions = self.get_dimensions()
        surface_size = self.text_surface.get_size()
        surface_offset = Aligner.get_alignment_offset(dimensions.x, dimensions.y, surface_size[0], surface_size[1],
                                                      self.text_align)

        content_area = self.get_content_area()
        surface.blit(self.text_surface,
                     (content_area.top_left.x + surface_offset.x, content_area.top_left.y + surface_offset.y))
