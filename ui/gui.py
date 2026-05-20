import pygame
from pygame.locals import *

#catch key inputs, and send them off to game
#draw pixels as rectangles.

class GUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        WHITE = (255, 255, 255)
        # Set up the game window
        screen = pygame.display.set_mode((64*10, 32 * 10))
        pygame.display.set_caption("Chip-8")

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.draw.rect(screen, WHITE, (0, 0, 10, 10)) #draw pixels with this.
            
            #x and y on emulator is just a line 64 to 32

            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
