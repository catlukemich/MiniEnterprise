from .widget import Widget

class Button(Widget):

    def __init__(self, image):
        super().__init__()
        self.image = image
    
    def draw(self, surface):
        return super().draw()