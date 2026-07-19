from .Frame import Frame
from gui.controls.Label import Label
from gui.layouts.VerticalLayout import VerticalLayout
from gui.drawers.BackgroundDrawer import BackgroundDrawer
from gui.drawers.BorderDrawer import BorderDrawer
from gui.utils.Color import Color
from gui.utils.Pad import Pad


class LabelFrame(Frame):
    def __init__(self, label_text=""):
        Frame.__init__(self)
        Frame.set_layout(self, VerticalLayout())

        self.label = Label(label_text)
        self.label.set_text_color(Color(255, 255, 255))
        self.label.set_background_drawer(BackgroundDrawer())
        self.label.set_background_color(Color(0, 0, 0))
        self.label.set_border_drawer(BorderDrawer())
        self.label.set_borders(Pad(0, 0, 0, 1))
        self.label.set_paddings(Pad(2, 2, 0, 0))

        self.inner_frame = Frame()
        self.inner_frame.set_borders(Pad(0, 0, 0, 0))
        self.inner_frame.set_background_drawer(None)
        self.inner_frame.set_border_drawer(None)

        Frame.add_widget(self, self.label)
        Frame.add_widget(self, self.inner_frame)

    def set_layout(self, layout):
        self.inner_frame.set_layout(layout)
        self.resize_label()

    def set_paddings(self, paddings):
        self.inner_frame.set_paddings(paddings)
        self.resize_label()

    def setLabelText(self, text):
        self.label.set_text(text)
        self.resize_label()

    def add_widget(self, widget):
        self.inner_frame.add_widget(widget)
        self.resize_label()

    def remove_widget(self, widget):
        self.inner_frame.remove_widget(widget)
        self.resize_label()

    def resize_label(self):
        paddings = self.label.get_paddings()
        width = self.layout.get_width(self) - paddings.left - paddings.right
        self.label.set_width(width)
