import globs

class GUI:

    def __init__(self):
        globs.Globals.gui = self
        self.widgets = []

    def draw(self, surface):
        for widget in self.widgets:
            self.widget.draw(surface)