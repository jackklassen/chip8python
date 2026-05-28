import os
from typing import Any
import pygame


#TODO: possible issue 2, Font_set stuff is stored as ints (maybe just store incomeing bytes from rom as ints?)

#TODO: plan for running code, use swtich statments
START_ADDRESS = 0x200
WHITE = (255, 255, 255)
FONT_SET = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
    0xF0, 0x80, 0xF0, 0x80, 0x80 # F
    ]
class Chip8:

    registers = [0] * 16 #16 registers
    memory = [0] * 4096 #4096 bytes of memory
    index = 0 #16-bit index that points to location in memory
    pc = 0 #program counter, current instruction in memory
    stack = [0] * 16 #16 bytes of stack
    sp = 0 #address for stack pointer
    delayTimer = 0
    soundTimer = 0
    keypad = [0] * 16 #16 slots for the 16 possible keyinputs

    opcode = 0


    def __init__(self, romfile):
        self.registers = [0] * 16  # 16 registers
        self.pc = START_ADDRESS
        self.video = [0] * (64 * 32)  # 64 * 32 size video
        opcode = 0
        index = 0
        sp = 0
        self.memory = [0] * 4096


        for i in range(64):
            self.memory[i] = FONT_SET[i]

        self.load_rom(romfile)
        pygame.init()

        # Set up the game window
        self.screen = pygame.display.set_mode((64 * 10, 32 * 10))
        pygame.display.set_caption("Chip-8")

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



            # x and y on emulator is just a line 64 to 32

            pygame.display.flip()
            self.cycle()

        # Quit Pygame
        pygame.quit()


    def load_rom(self, file_name):
        buffer = []
        with open(file_name, 'rb') as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break
                buffer.append(byte)

        for i in range(len(buffer)):
            self.memory[i + START_ADDRESS] = buffer[i]


    def cycle(self):
       # self.pc = 0x200
        while(self.pc < 4096 and not isinstance(self.memory[self.pc] , int)):
        #Fetch
            # as in grab the first part move it to the left and add the second part
            #opcode = something
            #array is filled with ints, we feed it bytes

            opcode  = self.memory[self.pc].hex() + self.memory[self.pc + 1].hex()
        #pc must increment somewhere might as well be here
            self.pc += 2


        #Decode Execute
            if opcode[:1] == "0":
                self.opcode_0()
            elif opcode[:1] == "1":
                self.opcode_1(opcode)
            elif opcode[:1] == "6":
                self.opcode_6(opcode)
            elif opcode[:1] == "7":
                self.opcode_7(opcode)
            elif opcode[:1] == "a":
                self.opcode_A()
            elif opcode[:1] == "d":
                self.opcode_D()
            else:
                print("Unknown opcode")

            print(opcode)



    def opcode_0(self):
        print("0 was called")
        self.screen.fill((0,0,0))
        pygame.display.flip()

        for i in self.video:
            i = 0


    def opcode_1(self,opcode):
        print("1 was called")
        new_pc = int(opcode[1:])
        self.pc = new_pc


    def opcode_6(self,opcode):
        print("6 was called")
        self.registers[int(opcode[1],16)] = int(opcode[2:], 16)

    def opcode_7(self,opcode):
        print("7 was called")
        self.registers[int(opcode[1],16)] += int(opcode[2:],16)

    def opcode_A(self):
        print("A was called")

    def opcode_D(self):
        print("D was called")
        pygame.draw.rect(self.screen, WHITE, (0, 0, 10, 10))  # draw pixels with this.
