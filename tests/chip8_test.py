"""
Copyright Jack Klassen

CHIP-8 emulator/interpreter

See License and ReadMe for more info
"""

import unittest

from src import cpu
START_ADDRESS = 0x200


class chip8_test(unittest.TestCase):

    def setUp(self):
        self.cpu_test = cpu.Chip8()


    def test_clear(self):
        self.cpu_test.video[0] = 0x1
        self.assertEqual(self.cpu_test.video[0], 1)  # add assertion here

        opcode = 0x00E0
        self.cpu_test.opcode_0(opcode)
        self.assertEqual(self.cpu_test.video[0], 0x0)  # add assertion here


    def test_pc_1(self):

        self.assertEqual(self.cpu_test.pc, START_ADDRESS)
        self.cpu_test.opcode_1(0x1201)
        self.assertEqual(self.cpu_test.pc, 0x201)

    def test_pc_2(self):
        self.assertEqual(self.cpu_test.pc, START_ADDRESS)
        self.cpu_test.opcode_2(0x1202)
        self.assertEqual(self.cpu_test.pc, 0x202)

        self.cpu_test.opcode_0(0x00EE)
        self.assertEqual(self.cpu_test.pc, START_ADDRESS)


    #opcode_3
    def test_opcode_3_pos(self):
        opcode = 0x3101
        self.cpu_test.registers[0x1] = 0x1
        self.cpu_test.opcode_3(opcode)
        assert(self.cpu_test.pc == START_ADDRESS + 2)

    def test_opcode_3_neg(self):
        opcode = 0x3101
        self.cpu_test.registers[0x1] = 0x2
        self.cpu_test.opcode_3(opcode)
        assert(self.cpu_test.pc == START_ADDRESS)
        assert(self.cpu_test.pc != START_ADDRESS + 2)

    #opcode 4
    def test_opcode_4_pos(self):
        opcode = 0x4101
        self.cpu_test.registers[0x1] = 0x1
        self.cpu_test.opcode_4(opcode)
        assert (self.cpu_test.pc == START_ADDRESS)
        assert (self.cpu_test.pc != START_ADDRESS + 2)

    def test_opcode_4_neg(self):
        opcode = 0x4101
        self.cpu_test.registers[0x1] = 0x2
        self.cpu_test.opcode_4(opcode)
        assert (self.cpu_test.pc == START_ADDRESS + 2)

    #opcode 5
    def test_opcode_5_pos(self):
        opcode = 0x5100
        self.cpu_test.registers[0x1] = 0x1
        self.cpu_test.registers[0x0] = 0x1
        self.cpu_test.opcode_5(opcode)
        assert (self.cpu_test.pc == START_ADDRESS + 2)


    def test_opcode_5_neg(self):
        opcode = 0x5100
        self.cpu_test.registers[0x1] = 0x2
        self.cpu_test.registers[0x0] = 0x1
        self.cpu_test.opcode_5(opcode)
        assert (self.cpu_test.pc == START_ADDRESS)


    #opcode 6
    def test_set_reg_normal(self):
        opcode = 0x6111
        self.cpu_test.opcode_6(opcode)
        self.assertEqual(self.cpu_test.registers[0x1], 0x11)

    def test_set_reg_high(self):
        opcode = 0x61FF
        self.cpu_test.opcode_6(opcode)
        self.assertEqual(self.cpu_test.registers[0x1], 0xFF)

    def test_set_reg_low(self):
        opcode = 0x6000
        self.cpu_test.opcode_6(opcode)
        self.assertEqual(self.cpu_test.registers[0x0], 0)



    #negative test
    def test_pop_from_empty_stack(self):
        opcode = 0x00EE
        self.assertEqual(self.cpu_test.pc, START_ADDRESS) #without calling cycle pc doesnt move
        self.cpu_test.opcode_0(opcode)
        self.assertEqual(self.cpu_test.pc, START_ADDRESS) #and with nothing on the stack pc should not change



    #timers


    #postive test
    def test_timer_pos(self):
        self.cpu_test.soundTimer = 2
        self.cpu_test.delayTimer = 2

        self.cpu_test.handle_timers()
        assert(self.cpu_test.delayTimer == 1)
        assert (self.cpu_test.soundTimer == 1)


    #negative test

    def test_timer_neg(self):
        self.cpu_test.soundTimer = -1
        self.cpu_test.delayTimer = -1
        assert (self.cpu_test.delayTimer == -1)
        assert (self.cpu_test.soundTimer == -1)
        self.cpu_test.handle_timers()
        assert(self.cpu_test.delayTimer == 0)
        assert (self.cpu_test.soundTimer == 0)


    #boundry test

    def test_timer_zero(self):
        self.cpu_test.soundTimer = 0
        self.cpu_test.delayTimer = 0
        self.cpu_test.handle_timers()
        assert (self.cpu_test.delayTimer == 0)
        assert (self.cpu_test.soundTimer == 0)


    #load rom

    #postive test
    def test_load_rom_nothing(self):
        assert(self.cpu_test.load_rom("test_rom.ch8") == 1)

        assert (self.cpu_test.memory[START_ADDRESS] != 0x0)
        assert (self.cpu_test.memory[START_ADDRESS + 1] != 0x0)


    #negative test
    def test_load_rom_nothing(self):
        assert(self.cpu_test.load_rom("") == 0)

        assert(self.cpu_test.memory[START_ADDRESS] == 0x0)
        assert(self.cpu_test.memory[START_ADDRESS + 1] == 0x0)


    #opcode_C (random)

    #postive test
    def test_opcode_C_pos(self):
        opcode = 0xC111
        self.cpu_test.opcode_C(opcode)
        assert(self.cpu_test.registers[0x1] | 0x11 == 0x11)

    #negative test
    def test_opcode_C_negative(self):
        opcode = 0xC122
        self.cpu_test.opcode_C(opcode)
        assert(self.cpu_test.registers[0x1] | 0x11 != 0x11)
    #boundry test
    def test_opcode_C_zero(self):
        opcode = 0xC100
        self.cpu_test.opcode_C(opcode)
        assert(self.cpu_test.registers[0x1] == 0x0)

    #opcode_7 (add to register, make sure register doesn't overload)

    #postive test
    def test_opcode_7_pos(self):
        opcode = 0x7101
        assert(self.cpu_test.registers[0x1] == 0x0)
        self.cpu_test.opcode_7(opcode)
        assert (self.cpu_test.registers[0x1] == 0x1)
        self.cpu_test.opcode_7(opcode)
        assert (self.cpu_test.registers[0x1] == 0x2)

    #negative test
    def test_opcode_7_negative(self):
        opcode = 0x7101
        self.cpu_test.registers[0x1] = 0xFF
        assert (self.cpu_test.registers[0x1] == 0xFF)
        self.cpu_test.opcode_7(opcode)
        assert (self.cpu_test.registers[0x1] == 0x0) #overflow makes register = 0
        assert (self.cpu_test.registers[0xF] == 0x0) #should not change

    #DXYN tests

    #postive (normal)

    #negative an imgage of nothing

    #boundry go off the map


    #opcode 8 tests

    # opcode 9
    def test_opcode_9_pos(self):
        opcode = 0x9100
        self.cpu_test.registers[0x1] = 0x1
        self.cpu_test.registers[0x0] = 0x1
        self.cpu_test.opcode_9(opcode)
        assert (self.cpu_test.pc == START_ADDRESS)

    def test_opcode_9_neg(self):
        opcode = 0x9100
        self.cpu_test.registers[0x1] = 0x2
        self.cpu_test.registers[0x0] = 0x1
        self.cpu_test.opcode_9(opcode)
        assert (self.cpu_test.pc == START_ADDRESS + 2)

    #opcdode_A tests
    #postive
    def test_opcode_A_pos(self):
        opcode = 0xA111
        self.cpu_test.opcode_A(opcode)
        assert(self.cpu_test.index == 0x111)
    #boundry
    def test_opcode_A_FFF(self):
        opcode = 0xAFFF
        self.cpu_test.opcode_A(opcode)
        assert(self.cpu_test.index == 0xFFF)

    def test_opcode_A_0(self):
        opcode = 0xA000
        self.cpu_test.opcode_A(opcode)
        assert(self.cpu_test.index == 0x0)


    #opcode_B tests

    #positive
    def test_opcode_B_pos(self):
        opcode = 0xB111
        self.cpu_test.registers[0x0] = 0x01
        self.cpu_test.opcode_B(opcode)
        self.assertEqual(self.cpu_test.pc, (0x1 + 0x0111))
    #boundry

    def test_opcode_B_FFF(self):
        opcode = 0xBFFF
        self.cpu_test.registers[0x0] = 0xFF
        self.cpu_test.opcode_B(opcode)
        self.assertEqual(self.cpu_test.pc, (0xFF + 0xFFF))

    def test_opcode_B_0(self):
        opcode = 0xB000
        self.cpu_test.registers[0x0] = 0x00
        self.cpu_test.opcode_B(opcode)
        self.assertEqual(self.cpu_test.pc, 0)
    #opcode F tests

if __name__ == '__main__':
    unittest.main()
