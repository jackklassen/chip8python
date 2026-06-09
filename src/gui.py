import time
from turtledemo.clock import hand

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

            #while running, if no keypress instruction was fired just call cycle (and that might decrement timer)
            #if there was a keypress pass that as some bool in cpu and pass a key_pressed into cpu to act acordingly.
            #cpu should have a handle key press depeding on what instruction started this keypress waiting thing.

            # x and y on emulator is just a line 64 to 32
            self.cpu.pressedKey = self.handle_keys()
            if self.cpu.wait_on_key:
                if self.cpu.neededKey == self.cpu.pressedKey:
                    self.cpu.wait_on_key = False
            else:
                self.cpu.cycle()

            pygame.display.flip()
            self.render()
            time.sleep(1/60)
        # Quit Pygame
        pygame.quit()

    def load_rom(self, filename):
        return self.cpu.load_rom(filename)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return 0x1
        elif keys[pygame.K_2]:
            return 0x2
        elif keys[pygame.K_3]:
            return 0x3
        elif keys[pygame.K_4]:
            return 0xC
        elif keys[pygame.K_q]:
            return 0x4
        elif keys[pygame.K_w]:
            return 0x5
        elif keys[pygame.K_e]:
            return 0x6
        elif keys[pygame.K_r]:
            return 0xD
        elif keys[pygame.K_a]:
            return 0x7
        elif keys[pygame.K_s]:
            return 0x8
        elif keys[pygame.K_d]:
            return 0x9
        elif keys[pygame.K_f]:
            return 0xE
        elif keys[pygame.K_z]:
            return 0xA
        elif keys[pygame.K_x]:
            return 0x0
        elif keys[pygame.K_c]:
            return 0xB
        elif keys[pygame.K_v]:
            return 0xF
        else:
            return None

    def render(self):
        self.screen.fill((0, 0, 0))
        for i, pixel in enumerate(self.cpu.video):
            if pixel:
                x = (i % 64) * SCALE
                y = (i // 64) * SCALE
                pygame.draw.rect(self.screen, WHITE, (x, y, SCALE, SCALE))
        pygame.display.flip()

