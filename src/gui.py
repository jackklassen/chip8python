import pygame

from src import chip8
WHITE = (255, 255, 255)
SCALE = 10

class Gui:
    def __init__(self):
        self.cpu = chip8.Chip8()
        self.screen = pygame.display.set_mode((64 * 10, 32 * 10))
        pygame.init()
        pygame.display.set_caption("Chip-8")

    def run(self):
        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # x and y on emulator is just a line 64 to 32

            pygame.display.flip()
            self.cpu.cycle()
            self.render()
        # Quit Pygame
        pygame.quit()

    def load_rom(self, filename):
        return self.cpu.load_rom(filename)

    def render(self):
        self.screen.fill((0, 0, 0))
        for i, pixel in enumerate(self.cpu.video):
            if pixel:
                x = (i % 64) * SCALE
                y = (i // 64) * SCALE
                pygame.draw.rect(self.screen, WHITE, (x, y, SCALE, SCALE))
        pygame.display.flip()

