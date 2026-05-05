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
        pass

