import globs
import pygame


''' 
Main class as the scaffold for all the game logic, for the game class itself
This class is responsible for initialization, event dispatching, update and 
delegating draw calls.
''' 
class Main():
    def __init__(self):
        pygame.init()
        globs.screen = pygame.display.set_mode((32 * 32,16*32 + 32))

        clock = pygame.time.Clock()
        done = False

        self.do_init()
        while not done:
            for event in pygame.event.get():
                self.do_event(event)
                if event.type == pygame.QUIT:
                    done = True

            self.do_updates()

            globs.screen.fill((10,40,230))
            self.do_drawing()

            clock.tick(30)
            pygame.display.update()


    def do_init(self):
        pass


    def do_event(self, event):
        pass


    def do_updates(self):
        pass


    def do_drawing(self):
        pass



if __name__ == "__main__":
    Main()
