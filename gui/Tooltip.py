from .containers.LabelFrame import LabelFrame


class Tooltip(LabelFrame):

    def __init__(self):
        super().__init__()
        self.text = ""
        self.visible = True

    
    def set_text(self, text):
        self.text = text

    def draw(self, surface):
        super().draw(surface)
    
