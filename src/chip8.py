import os
from typing import Any
START_ADDRESS = 0x200
FONT_SET = {
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
    }
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
    video = [0] * (64 * 32) #64 * 32 size video
    opcode = 0


    def __init__(self):
        pc = START_ADDRESS
        opcode = 0
        index = 0
        sp = 0
        self.memory = [0] * 4096


        for i in range(64):
            self.memory[i] = FONT_SET[i]



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

        