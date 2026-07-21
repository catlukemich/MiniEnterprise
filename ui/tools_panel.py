import globs
import gui


class ToolsPanel(gui.Frame, gui.WidgetListener):

  
    def __init__(self):
        super().__init__()
        panel_height = 120
        self.set_dimensions(32*32, panel_height)
        self.set_position(0, 16* 32 + 32 - panel_height)


        #---------- Container for horizontally aligning all the widget's: ------------#
        self.container = gui.Frame()
        self.container.set_borders(gui.EqualPad(0))
        self.container.set_layout(gui.HorizontalLayout())
        self.add_widget(self.container)
        #----------- End of container ------------------------------------------------#

        # Label for constructions chains:
        chains_label = gui.Label("Processing chains")
        chains_label.set_margins(gui.EqualPad(10))
        self.container.add_widget(chains_label)


        ### The actuall chains construction buttons ###
        self.constructions_listener = ConstructionsListner() # Used below when creating a button vvv

        # Steel production chain:
        steel_category_conainer = gui.LabelFrame("Steel")
        steel_category_conainer.set_layout(gui.HorizontalLayout())
        steel_category_conainer.set_margins(gui.EqualPad(10))
        steel_category_conainer.set_paddings(gui.Pad(4,4,7,7))
        self.create_button("assets/industries/coal_mine.png", steel_category_conainer)
        self.create_button("assets/industries/steel_mill.png", steel_category_conainer)
        self.create_button("assets/industries/metal_shop.png", steel_category_conainer)
        self.container.add_widget(steel_category_conainer)

        # Grain production chain:
        grain_category_container = gui.LabelFrame("Grain")
        grain_category_container.set_layout(gui.HorizontalLayout())
        grain_category_container.set_paddings(gui.Pad(4,4,10,10))
        grain_category_container.set_margins(gui.EqualPad(3))
        self.create_button("assets/industries/farm.png",   grain_category_container)
        self.create_button("assets/industries/grain_mill.png",    grain_category_container)
        self.create_button("assets/industries/market.png",  grain_category_container)
        self.container.add_widget(grain_category_container)

        # Oil production chain:
        oil_category_container = gui.LabelFrame("Oil")
        oil_category_container.set_layout(gui.HorizontalLayout())
        oil_category_container.set_paddings(gui.EqualPad(3))
        oil_category_container.set_margins(gui.EqualPad(10))
        self.create_button("assets/industries/rafinery.png",   oil_category_container)
        self.create_button("assets/industries/plastic_works.png",  oil_category_container)
        self.create_button("assets/industries/market.png",  oil_category_container)
        self.container.add_widget(oil_category_container)


    # Create a toolbar button that will be placed inside this toolbar container.    
    def create_button(self, image_path, category_conainer):
        image = gui.load_image(image_path)
        button = gui.ImageButton(image)
        button.set_paddings(gui.EqualPad(4))
        button.set_margins(gui.EqualPad(10))
        button.add_listener(self.constructions_listener)     # Created above in the constructor ^^^
        category_conainer.add_widget(button)




### Constructions listener - listener for when one of construction button is pressed ###
class ConstructionsListner(gui.WidgetListener):
    pass
    
    