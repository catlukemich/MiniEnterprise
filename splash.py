import pygame
import loader
import os
import sys
import time
import game as mgame

class SplashScreen:

    def __init__(self):
        pygame.init()
        surface = pygame.display.set_mode((878,326))
        splash  = pygame.image.load("assets/game/splash.png")
        surface.blit(splash)
        pygame.display.update()
        time.sleep(2.5)

        game = mgame.Game()

if __name__ == "__main__":
    SplashScreen()