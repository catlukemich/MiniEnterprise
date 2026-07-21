import globs
import pygame
import gui



''' 
Main class as the scaffold for all the game logic, for the game class itself
This class is responsible for initialization, event dispatching, update and 
delegating draw calls.
''' 
class Main():
    
    def __init__(self):
        ### System initialization ###
        pygame.init()
        globs.screen = pygame.display.set_mode((32 * 32,16*32 + 32))

        self.gui_input = gui.Input()
        globs.gui = gui.Gui(input)
        self.gui_input.add_mouse_listener(globs.gui)
        self.gui_input.add_keyboard_listener(globs.gui)

        label_img_button = gui.Label("Image button:")
        label_img_button.set_position(35, 15)
        globs.gui.add_widget(label_img_button)

        img_pressed = gui.load_image("res/aircraft.png")
        img_button = gui.ImageButton(img_pressed)
        img_button.set_position(20, 40)
        globs.gui.add_widget(img_button)
        img_button.set_dimensions(120, 100)

        clock = pygame.time.Clock()
        done = False

        # The main loop - loop 
        # EVENTS + UPDATE + DRAWING
        self.do_init()
        delta_time = 0
        while not done:
            for event in pygame.event.get(): # <-- 1 Events.
                event_consumed = self.gui_input.handle_event(event)
                if not event_consumed:
                    self.do_event(event) # <-- Handle game input events.
                if event.type == pygame.QUIT:
                    done = True

            self.do_updates(delta_time)  # <-- 2 Update.

            globs.screen.fill((0,78,198)) # <-- Blue-ish background.
            self.do_drawing()  # <-- 3 Drawing.
            globs.gui.draw(globs.screen) # <-- 4. Draw the GUI

            delta_time = clock.tick(30)
            pygame.display.update()


    #---------- Delegates to inheriting classes (derived in game.py) ----------#
    def do_init(self):
        pass


    def do_event(self, event):
        pass


    def do_updates(self, delta_time):
        pass


    def do_drawing(self):
        pass



if __name__ == "__main__":
    Main()
