import os
from random import randint
from typing import Any


START_ADDRESS = 0x200

FONT_SET = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]



class Chip8:
    #registers = [0] * 16  #16 registers
    #memory = [0] * 4096  #4096 bytes of memory
    #index = 0  #16-bit index that points to location in memory
    #pc = 0  #program counter, current instruction in memory
    #stack = [0] * 16  #16 bytes of stack
    #sp = 0  #address for stack pointer
    delayTimer = 0
    soundTimer = 0
    keypad = [0] * 16  #16 slots for the 16 possible keyinputs

    opcode = 0

    def __init__(self):
        self.registers = [0] * 16  # 16 registers
        self.pc = START_ADDRESS
        self.video = [0] * (64 * 32)  # 64 * 32 size video
        self.stack = [0] * 16  # 16 bytes of stack
        self.delayTimer = 0
        self.soundTimer = 0
        self.wait_on_key = False
        self.neededKey = None #connected to wait on key, when waiting, this holds a key we need.
        self.pressedKey = None #to be set when gui sends it to cpu
        opcode = 0
        self.index = 0
        self.memory = [0] * 4096

        for i in range(64):
            self.memory[i] = FONT_SET[i]

        #self.load_rom(romfile)

    def handleTimers(self):
        if self.delayTimer > 0:
            self.delayTimer -= 1
        if self.soundTimer > 0:
            self.soundTimer -= 1


    def load_rom(self, file_name):
        with open(file_name, 'rb') as f:
            buffer = f.read()

        for i, byte in enumerate(buffer):
            if START_ADDRESS + i < 4095:
                self.memory[i + START_ADDRESS] = byte

    def cycle(self):
        # self.pc = 0x200
        #while (self.pc < 4096):
            #Fetch
            # as in grab the first part move it to the left and add the second part
            #opcode = something
            #array is filled with ints, we feed it bytes

        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
            #pc must increment somewhere might as well be here
        self.pc += 2
        self.handleTimers()
        first_hexit = (opcode & 0xF000) >> 12

            #Decode Execute
        if first_hexit == 0x0:
            self.opcode_0(opcode)
        elif first_hexit == 0x1:
            self.opcode_1(opcode)
        elif first_hexit == 0x2:
            self.opcode_2(opcode)
        elif first_hexit == 0x3:
            self.opcode_3(opcode)
        elif first_hexit == 0x4:
            self.opcode_4(opcode)
        elif first_hexit == 0x5:
            self.opcode_5(opcode)
        elif first_hexit == 0x6:
            self.opcode_6(opcode)
        elif first_hexit == 0x7:
            self.opcode_7(opcode)
        elif first_hexit == 0x8:
            self.opcode_8(opcode)
        elif first_hexit == 0xA:
            self.opcode_A(opcode)
        elif first_hexit == 0xB:
            self.opcode_B(opcode)
        elif first_hexit == 0xC:
            self.opcode_C(opcode)
        elif first_hexit == 0xD:
            self.opcode_D(opcode)
        elif first_hexit == 0xE:
            self.opcode_E(opcode)
        elif first_hexit == 0xF:
            self.opcode_F(opcode)
        else:
            print("Unknown opcode")

        #print(hex(opcode))

    ## 00E0 and 00EE, Clear Screen and Pop pc from stack
    def opcode_0(self, opcode):
        if opcode == 0x00EE:
            print("00EE was called")
            self.pc = self.stack.pop()
        else:
            print("0 was called")
            #self.screen.fill((0, 0, 0))
            #pygame.display.flip()
            for i in self.video:
                self.video[i] = 0
    #1NNN, Jump to NNN
    def opcode_1(self, opcode):
        print("1 was called")
        new_pc = opcode & 0x0FFF
        print(new_pc)
        self.pc = new_pc

    #2NNN, Jump to NNN, store previous pc on stack.
    def opcode_2(self, opcode):
        print("2 was called")
        new_pc = opcode & 0x0FFF
        self.stack.append(self.pc)
        self.pc = new_pc

    #3XNN skip 1 instruction if reg[vx] == NN
    def opcode_3(self,opcode):
        print("3 was called")
        vx_reg = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)
        if self.registers[vx_reg] == nn_hexit:
            self.pc += 2


    #4XNN skip 1 instruction if reg[vx] =/= NN
    def opcode_4(self, opcode):
        print("4 was called")
        vx_reg = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)
        if not self.registers[vx_reg] == nn_hexit:
            self.pc += 2


    #5XY0 skip 1 instruction if reg[vx] == reg[vy]
    def opcode_5(self, opcode):
        print("5 was called")
        vx_reg = (opcode & 0x0F00) >> 8
        vy_reg = (opcode & 0x00F0) >> 4

        if self.registers[vx_reg] == self.registers[vy_reg]:
            self.pc += 2

    #6XNN, Set register vx to NN
    def opcode_6(self, opcode):
        print("6 was called")
        second_hexit = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)

        self.registers[second_hexit] = nn_hexit

    #7XNN, add NN to reg[vx]
    def opcode_7(self, opcode):
        print("7 was called")
        second_hexit = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)

        self.registers[second_hexit] = (self.registers[second_hexit] + nn_hexit) & 0xFF

    #8XYN, Logical and arithmetic  operations on registers
    def opcode_8(self,opcode):
        print("8 was called")

        vx_reg = (opcode & 0x0F00) >> 8
        vy_reg = (opcode & 0x00F0) >> 4
        n = opcode & 0x000F

        if n == 0x0:
            self.registers[vx_reg] = self.registers[vy_reg]
        elif n == 0x1:
            self.registers[vx_reg] = self.registers[vx_reg] | self.registers[vy_reg]
        elif n == 0x2:
            self.registers[vx_reg] = self.registers[vx_reg] & self.registers[vy_reg]
        elif n == 0x3:
            self.registers[vx_reg] = self.registers[vx_reg] ^ self.registers[vy_reg]
        elif n == 0x4:
            new_val = self.registers[vx_reg] + self.registers[vy_reg]
            self.registers[vx_reg] = new_val % 256

            if new_val > 255:
                self.registers[0xF] = 1 #set off carry flag
        elif n == 0x5:
            if self.registers[vx_reg] >= self.registers[vy_reg]:
                self.registers[0xF] = 1
                self.registers[vx_reg] = self.registers[vx_reg] - self.registers[vy_reg]
            else:
                self.registers[0xF] = 0
                self.registers[vx_reg] = 256 + self.registers[vx_reg] - self.registers[vy_reg]

        elif n==0x6:
            shifted_bit = self.registers[vx_reg] & 0x1

            self.registers[vx_reg] = self.registers[vx_reg] >> 1
            self.registers[0xF] = shifted_bit

        elif n == 0x7:
            if self.registers[vy_reg] >= self.registers[vx_reg]:
                self.registers[0xF] = 1
                self.registers[vx_reg] = self.registers[vy_reg] - self.registers[vx_reg]
            else:
                self.registers[0xF] = 0
                self.registers[vx_reg] = 256 + self.registers[vy_reg] - self.registers[vx_reg]

        elif n == 0xE:
            shifted_bit = self.registers[vx_reg] & 0x1
            self.registers[vx_reg] = self.registers[vx_reg] << 1
            self.registers[0xF] = shifted_bit

    #9XY0 skip 1 instruction if reg[vx] == reg[vy]
    def opcode_9(self, opcode):
        print("9 was called")
        vx_reg = (opcode & 0x0F00) >> 8
        vy_reg = (opcode & 0x00F0) >> 4

        if not self.registers[vx_reg] == self.registers[vy_reg]:
            self.pc += 2

    #ANNN, set the index regiseter to NNN
    def opcode_A(self, opcode):
        print("A was called")
        nnn_hexits = opcode & 0x0FFF
        self.index = nnn_hexits


    #BNNN, Jump with an offset
    def opcode_B(self, opcode):
        #todo: this
        pass

    #CXNN, put a random added with into vx
    def opcode_C(self,opcode):
        print("C was called")
        vx_reg = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)
        random = randint(0,255)
        self.registers[vx_reg] = random & nn_hexit


    #DXYN, display
    def opcode_D(self, opcode):
        print("D was called")
        vx_reg = (opcode & 0x0F00) >> 8
        vy_reg = (opcode & 0x00F0) >> 4
        n = opcode & 0x000F
        x_coord = self.registers[vx_reg] % 64
        y_coord = self.registers[vy_reg] % 32
        self.registers[0xF] = 0  #collision register off
        for row in range(n):
            sprite_byte = self.memory[self.index + row]
            for col in range(8):
                if sprite_byte & (0x80 >> col):
                    pixel_index = (((y_coord + row) % 32 * 64) + ((x_coord + col) % 64))
                    if self.video[pixel_index] == 1:
                        self.registers[0xF] = 1

                    self.video[pixel_index] ^= 1


    def opcode_E(self,opcode):
        print("E was called")
        vx_reg = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)

        if nn_hexit == 0x9E:
            if self.pressedKey == self.registers[vx_reg]:
                self.pc += 2
        if nn_hexit == 0xA1:
            if not self.pressedKey == self.registers[vx_reg]:
                self.pc += 2

    def opcode_F(self,opcode):
        print("F was called")
        vx_reg = (opcode & 0x0F00) >> 8
        nn_hexit = (opcode & 0x00FF)

        if nn_hexit == 0x07:
            self.registers[vx_reg] = self.delayTimer
        elif nn_hexit == 0x15:
            self.delayTimer = self.registers[vx_reg]
        elif nn_hexit == 0x18:
            self.soundTimer = self.registers[vx_reg]
        elif nn_hexit == 0x1E:
            self.index += self.registers[vx_reg]
        elif nn_hexit == 0x0A:
            self.wait_on_key = True
            self.neededKey = self.registers[vx_reg]
        elif nn_hexit == 0x29:
            self.index = self.memory[self.registers[vx_reg]] #point index to font char in mem, its first thing in mem
        elif nn_hexit == 0x33:
            pass
            #todo: this
            # Binary-coded decimal conversion
        elif nn_hexit == 0x55:
            for i in range(vx_reg + 1):
                self.memory[self.index + i] = self.registers[i]

            #store in mem
        elif nn_hexit == 0x65:
            for i in range(vx_reg + 1):
                self.registers[i] = self.memory[self.index + i]
            #load from mem