import pygame

from ..utils.Vector2D import Vector2D
from .Label import Label
from gui.drawers.BackgroundDrawer import BackgroundDrawer
from gui.drawers.BorderDrawer import BorderDrawer
from gui.containers.Frame import Frame


class TextInput(Label):
    def __init__(self, text="", line_width=40):
        Label.__init__(self, text)
        self.line_width = line_width
        self.set_width(line_width)
        self.set_height(self.font.size)

        self.caret_index = 0
        self.caret = self.create_caret()

        self.set_background_drawer(BackgroundDrawer())
        self.set_border_drawer(BorderDrawer())

        self.has_focus = False

    def create_caret(self):
        width = 2
        height = self.font.size
        caret = pygame.Surface((width, height))
        caret.fill((0, 0, 0, 255))
        return caret

    def on_mouse_button_down(self, event):
        if self.text.strip() == False:
            return

        mouse = Vector2D(event.pos[0], event.pos[1])
        content_area = self.get_content_area()
        offset_left = content_area.top_left.x
        current_x = 0

        for letter_index in range(0, len(self.text)):
            text_current = self.text[0:letter_index]
            width_current = self.get_text_width(text_current)
            text_next = self.text[0:letter_index + 1]
            width_next = self.get_text_width(text_next)
            if mouse.x >= width_current + offset_left and mouse.x <= width_next + offset_left:
                self.caret_index = letter_index
                break

    def on_key_down(self, event):
        if event.key < 256 and (chr(event.key).isalnum() or chr(event.key) == " "):
            char = chr(event.key)
            if event.key >= 96 and event.key <= 122:
                if event.mod == 2:
                    char = chr(event.key - 32)  # Big letter
            if event.key == 32: char = " "
            text_before = self.text[0:self.caret_index]
            text_before += char
            text_after = self.text[self.caret_index:]
            self.text = text_before + text_after

            self.text_surface = self.draw_text_surface()
            self.caret_index += 1

        else:
            if event.key == 276:  # Arrow left
                self.caret_index -= 1
            if event.key == 275:  # Arrow right
                self.caret_index += 1
            if event.key == 8:  # Backspace
                text_before = self.text[0:self.caret_index - 1]
                text_after = self.text[self.caret_index:]
                self.text = text_before + text_after
                self.text_surface = self.draw_text_surface()
                self.caret_index -= 1
            if event.key == 127:  # Delete
                text_before = self.text[0:self.caret_index]
                text_after = self.text[self.caret_index + 1:]
                self.text = text_before + text_after
                self.text_surface = self.draw_text_surface()

        if self.caret_index < 0:
            self.caret_index = 0
        if self.caret_index > len(self.text):
            self.caret_index = len(self.text)

        own_width = self.line_width
        text_width = self.get_text_width(self.text)
        if text_width > own_width: own_width = text_width
        self.set_width(own_width)

    def on_focus_gain(self, event):
        self.has_focus = True

    def on_focus_lost(self, event):
        self.has_focus = False

    def draw(self, surface):
        # Draw the background and the border:
        bg_drawer = self.get_background_drawer()
        border_drawer = self.get_border_drawer()
        bg_drawer.draw_background(self, surface)
        border_drawer.draw_border(self, surface)

        # Do the clipping of the text:
        orig_clip = surface.get_clip()
        clip = self.get_content_area()

        parent = self.get_parent()
        if (isinstance(parent, Frame)):
            parent_clip = parent.get_clipping_rectangle()
            clip = parent_clip.intersection(clip)

        surface.set_clip(pygame.Rect(
            clip.top_left.x, clip.top_left.y,
            clip.bottom_right.x - clip.top_left.x, clip.bottom_right.y - clip.top_left.y)
        )

        # Draw the text:
        content_area = self.get_content_area()
        surface.blit(self.text_surface, (content_area.top_left.x, content_area.top_left.y))

        # Draw the caret if the widget has focus:
        if self.has_focus:
            text_before = self.text[0:self.caret_index]
            content_area = self.get_content_area()
            caret_position_left = self.get_text_width(text_before) + content_area.top_left.x
            caret_position_top = content_area.top_left.y
            surface.blit(self.caret, (caret_position_left, caret_position_top))

        # Reset the clip:
        surface.set_clip(orig_clip)
