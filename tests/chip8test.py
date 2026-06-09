"""
Copyright Jack Klassen

CHIP-8 emulator/interpretor

See License and ReadMe for more info
"""

import unittest

from src import cpu
START_ADDRESS = 0x200


class MyTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
