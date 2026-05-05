import pygame
from pygame.locals import *

#catch key inputs, and send them off to game
#draw pixels as rectangles.

class GUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        screen = pygame.display.set_mode((64*10, 32 * 10))
        pygame.display.set_caption("Hello Pygame")

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Quit Pygame
        pygame.quit()
