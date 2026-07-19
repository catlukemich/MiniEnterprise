import pygame

from gui.layouts.GridLayout import GridLayout
from gui.containers.Frame import Frame
from .Box import Box
from .Label import Label
from gui.Style import *


class Radio(Frame):
    def __init__(self, font):
        Frame.__init__(self)
        self.font = font
        self.set_layout(GridLayout(2, 2))
        self.options = {}

        self.set_background_drawer(None)
        self.set_border_drawer(None)

    def add_option(self, value, text):
        label = Label(text)
        label.set_margins(Style.radiolabel_margins)
        label.set_paddings(Style.radiolabel_paddings)

        radiobutton = RadioButton(self)
        self.options[value] = (radiobutton, label)

        rows = len(self.options)
        self.set_layout(GridLayout(2, rows))

        self.add_widget(radiobutton)
        self.add_widget(label)

    def deselect_all(self):
        for value in self.options:
            radio_tuple = self.options[value]
            radiobutton = radio_tuple[0]
            radiobutton.set_selected(False)

    def get_selected(self):
        selected = None
        for value in self.options:
            radio_tuple = self.options[value]
            radiobutton = radio_tuple[0]
            is_selected = radiobutton.is_selected()
            if is_selected: selected = value

        return selected

    def add_listener(self, listener):
        for value in self.options:
            radio_tuple = self.options[value]
            radiobutton = radio_tuple[0]
            radiobutton.add_listener(listener)

    def remove_listener(self, listener):
        for value in self.options:
            radio_tuple = self.options[value]
            radiobutton = radio_tuple[0]
            radiobutton.remove_listener(listener)


class RadioButton(Box):
    def __init__(self, radio):
        Box.__init__(self)

        self.margins = Style.radiobutton_margins
        self.paddings = Style.radiobutton_paddings

        self.radio = radio
        self.selected = False

        self.set_dimensions(10, 10)

        self.set_background_drawer(None)
        self.set_border_drawer(None)

    def set_selected(self, selected):
        self.selected = selected

    def is_selected(self):
        return self.selected

    def on_click(self, event):
        self.radio.deselect_all()
        self.set_selected(True)
        Box.on_click(self, event)

    def draw(self, surface):
        content_area = self.get_content_area()
        center_x = int(content_area.top_left.x + 5)
        center_y = int(content_area.top_left.y + 5)

        # Draw the outer circle:
        pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y), 5, 1)

        # Draw the inner circle if selected:
        if self.selected:
            pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y), 2)
