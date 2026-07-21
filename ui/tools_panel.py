import globs
import gui


class ToolsPanel(gui.Frame):

  
    def __init__(self):
        super().__init__()
        self.set_dimensions(32*32,96)
        self.set_position(0, 16* 32 + 32 - 96)


    
    def create_button(image_path, listener):
        image = gui.load_image(image_path)
        button = gui.ImageButton(image)
        button.add_listener(listener)
